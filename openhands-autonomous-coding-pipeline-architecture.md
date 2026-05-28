# OpenHands Autonomous Coding Pipeline — Architecture Guide

## What is the OpenHands Autonomous Coding Pipeline?

An end-to-end platform that turns GitHub issues into merged pull requests autonomously. An AI agent reads the issue, understands the codebase, writes code and tests inside a sandboxed Docker container, opens a PR, and either auto-merges (if confidence is high) or escalates to a human reviewer. Every action is logged in an append-only event store for full auditability.

---

## Architecture Overview

The system has five layers plus a cross-cutting observability/security column:

| Layer | Components |
|-------|-----------|
| **Trigger** | GitHub Issue, Webhook Listener, Agent Server |
| **Agent Core** | CodeAct Agent, LLM Router (LiteLLM), Claude 4.5 Opus / GPT-5.2 Codex |
| **Execution** | Docker Sandbox, Bash + Python shells, Chromium browser, VS Code, Overlay FS |
| **Tools** | Native Tools (file ops, shell, git), MCP Tools (JSON-RPC 2.0) |
| **Output** | Git Operations, PR Generator, CI/CD Pipeline, Review Gate, Auto-Merge / Human Review |
| **Cross-cutting** | Event Store, SecurityAnalyzer, Condenser, Secret Registry, Audit Logger, Multi-Agent |

---

## Component: GitHub Webhook Listener

Receives issue and pull request events from GitHub. Filters for trigger labels (`fix-me`, `openhands`) or `@openhands` mentions in PR comments. Routes events to the Agent Server via HTTP POST.

- Supports GitHub Apps and personal access tokens
- Rate-limited to avoid GitHub API throttling
- Event payload validated and normalized before forwarding

---

## Component: Agent Server

A production FastAPI server with REST endpoints and WebSocket event streaming. Manages agent sessions, routes requests, and serves the web UI.

- **REST API**: session CRUD, file upload/download, status polling
- **WebSocket**: real-time event streaming to clients
- **Docker orchestration**: spins up one sandbox container per agent session
- **Official Docker images** bundle API server, VS Code Web, VNC desktop, and Chromium

---

## Component: CodeAct Agent

The core reasoning engine. A stateless event processor that unifies all actions into a single code-based action space. Two interaction modes:

- **Natural language**: conversation with users for clarification
- **Code execution**: bash and Python commands dispatched to the sandbox

Key properties:
- Contains LLM settings, tool specs, security policies, and context (skills, prompts)
- Emits structured events through callbacks
- Supports **sub-agent delegation**: parent agents spawn independent conversations that inherit model config and workspace context
- **CodeAct 2.1**: uses function calling for precise tool specification

---

## Component: LLM Router (LiteLLM)

A unified interface to 100+ LLM providers. No vendor lock-in — swap models without code changes.

- **Primary**: Claude 4.5 Opus (top SWE-Bench performance, fastest completion)
- **Secondary**: GPT-5.2 Codex (best at long-horizon greenfield tasks)
- **Cost-effective**: Gemini 3 Flash, DeepSeek-v3.2 (strongest open-weight)
- Native reasoning support for Anthropic extended thinking and OpenAI reasoning
- `NonNativeToolCallingMixin` enables tool use on models that lack native function calling

---

## Component: Docker Sandbox Runtime

Every agent runs in an isolated Docker container with its own filesystem, shell, browser, and editor. The agent cannot access the host system.

**Capabilities inside the sandbox:**
- Linux bash command execution
- Python code via interactive interpreter
- File operations (read/write/upload/download)
- Web browsing via Chromium
- VS Code editing
- Plugin system (Jupyter, VS Code, Agent Skills extensions)

**Image management** uses a three-tier tagging system (versioned, lock, source) for intelligent incremental builds.

**Storage modes:**
- Bind mounts (direct host directory)
- Named Docker volumes
- Overlay (copy-on-write) for non-destructive modifications

---

## Component: Tool Registry

A unified registry for both native and MCP (Model Context Protocol) tools.

- **Native tools**: file operations, shell commands, git operations — executed directly in sandbox
- **MCP tools**: JSON-RPC 2.0 protocol, connecting to external systems (Jira, Slack, Linear, databases)
- **Action-Execution-Observation pattern**: Actions validated via Pydantic, executed by ToolExecutors, observations returned in LLM-compatible format
- Tools are typed with schemas and input validation

---

## Component: Git Operations + PR Generator

Handles the full git workflow inside the sandbox:

- Branch creation from latest main
- Incremental commits with meaningful messages
- Push to remote with proper authentication
- PR creation with auto-generated summary, linked to the original issue
- CI/CD pipeline trigger on PR creation

---

## Component: Review Gate

A confidence-based decision point:

- **Auto-merge** (confidence >= 0.7): CI passes, security scan clean, tests green → merge without human intervention
- **Human review** (confidence < 0.7): flagged for manual review with agent's reasoning and confidence score attached
- Configurable thresholds per repository or organization

---

## Component: Event Store

An append-only immutable event log. The single source of truth for all agent activity.

- Every interaction is an immutable event
- Enables **deterministic replay**: re-run any session from its event log
- Session recovery: pick up where an agent left off after interruption
- Full audit trail for compliance

---

## Component: SecurityAnalyzer

Rates every tool call as LOW, MEDIUM, or HIGH risk.

- **ConfirmationPolicy** determines whether user approval is required
- **LLMSecurityAnalyzer** appends `security_risk` fields to tool calls
- Bash tool scans commands for secret keys, exports as env vars, replaces values with `<secret-hidden>`
- Secret Registry provides per-conversation isolation; secrets masked in all outputs

---

## Component: Condenser

Manages the LLM's context window to reduce costs and prevent context overflow.

- Drops old events and replaces with summaries
- Reduces costs by up to 2x with no performance degradation
- Configurable compression strategies per model

---

## Key Data Flows

### A typical issue-to-PR flow

1. **Issue created** — developer labels a GitHub issue with `fix-me`
2. **Webhook fires** — GitHub sends event to the Webhook Listener
3. **Session spawned** — Agent Server creates a new session, spins up Docker sandbox
4. **Agent reads codebase** — CodeAct Agent analyzes repo structure, relevant files, and issue description
5. **LLM reasoning** — Agent queries Claude 4.5 Opus via LiteLLM for a plan of attack
6. **Code execution** — Agent writes code, runs tests, and iterates inside the sandbox
7. **Tool invocation** — Agent uses native tools (file ops, shell) and MCP tools as needed
8. **Git commit** — Changes committed to a new branch
9. **PR generated** — Pull request opened with summary and linked to original issue
10. **CI/CD runs** — Automated tests, SAST scan, and lint checks execute
11. **Confidence scored** — Review gate evaluates test results and agent confidence
12. **Merge or review** — Auto-merged if >= 0.7 confidence, else queued for human review

---

## Design Decisions

- **Event sourcing over state mutation**: Every action is an immutable event. This enables deterministic replay, session recovery, and a complete audit trail — critical for enterprise compliance. Trade-off: higher storage cost, but the auditability payoff is worth it.

- **One Docker container per agent**: Complete isolation prevents cross-contamination between sessions. The agent cannot access the host or other containers. Trade-off: container spin-up latency (~2-5 seconds), mitigated by pre-warming pools.

- **Model-agnostic via LiteLLM**: No vendor lock-in. If Claude pricing changes or GPT releases a better model, swap in 48 hours via config change. Trade-off: slight abstraction overhead, but negligible vs. API latency.

- **Confidence-based review gate**: High-confidence fixes merge automatically (saving human time), while edge cases get human review (maintaining quality). The 0.7 threshold is tunable per org. Trade-off: requires initial calibration to find the right threshold for each team's risk tolerance.

- **MCP for external integrations**: Model Context Protocol provides a standard interface for connecting to any external system. New integrations are config, not code. Trade-off: JSON-RPC overhead, but the standardization dramatically reduces integration time.

---

## Key Metrics

| Metric | Value | Source |
|--------|-------|--------|
| SWE-Bench Verified resolve rate | 77.6% | OpenHands Index, May 2026 |
| Cost per generated PR | ~$3 | Real-world Go microservice upgrades |
| Self-written commits | 37% | OpenHands GitHub Resolver dogfooding |
| GitHub stars | 74.6k | github.com/All-Hands-AI/OpenHands |
| LLM providers supported | 100+ | Via LiteLLM integration |
| Container isolation | Full | Docker per agent, no host access |
