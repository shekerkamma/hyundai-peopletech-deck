---
title: "OpenHands/OpenHands"
source: https://github.com/OpenHands/OpenHands
source_type: github-repo
owner: OpenHands
stars: 74522
forks: 9440
language: Python
license: MIT (core) + Enterprise license (enterprise/)
date_watched: 2026-05-22
tags: [content-research, github, python, ai-agent, software-engineering, developer-tools, #source/github]
---

# OpenHands/OpenHands

## TL;DR
The leading open-source AI-driven development platform (74.5K stars). Provides a composable Python SDK, CLI, GUI, and Enterprise tier for building AI agents that write, test, and deploy code. Powers both individual developer tools and enterprise-scale multi-agent systems. SWE-Bench score: 77.6% — near top of competitive leaderboards.

## What It Does
OpenHands is a community-focused platform for AI-driven software development. It provides multiple interfaces to AI coding agents:

1. **Software Agent SDK** — Composable Python library. Define agents in code, run locally or scale to 1000s in the cloud. The engine powering everything else.
2. **CLI** — Terminal-based coding agent (like Claude Code or Codex). Works with Claude, GPT, or any LLM.
3. **Local GUI** — REST API + React single-page app (like Devin or Jules). For running agents on your laptop.
4. **OpenHands Cloud** — Hosted deployment with Slack/Jira/Linear integrations, multi-user support, RBAC, collaboration.
5. **OpenHands Enterprise** — Self-hosted in customer VPC via Kubernetes. Source-available. Extended support + research team access.

### Core Agent Architecture
- **CodeAct Agent** — Default generalist. Executes bash commands, Python code, browser interactions. Based on [[CodeAct]] framework.
- **Browsing Agent** — Generalist web agent for information gathering.
- **Micro Agents / Skills** — Specialized agents for specific domains (GitHub, Docker, Kubernetes, code review, security, SSH, etc.).
- **Multi-agent delegation** — Specialized agents can work together on complex tasks.

### Key Technical Features
- Sandboxed execution in Docker containers (IPythonRunCellAction, CmdRunAction)
- File editing and creation tools
- Web browsing capabilities
- MCP (Model Context Protocol) integration
- Task planning and decomposition
- Automatic context compression
- Security analysis
- Conversation save/restore for long-running workflows

## Tech Stack
- **Language**: Python (65.2%), TypeScript (33.1%), Go Template (0.9%)
- **Backend**: Python, Poetry, FastAPI
- **Frontend**: React, TypeScript
- **Agent SDK**: Separate repo — [[OpenHands/software-agent-sdk]] (741 stars)
- **Containerization**: Docker, Docker Compose, Kubernetes
- **CI/CD**: GitHub Actions
- **Testing**: pytest, Playwright (browser tests)
- **Pre-commit**: Ruff (formatting), Mypy (types)
- **LLM Support**: Claude, GPT, Qwen, Devstral, any LLM via API

## Traction
- **Stars**: 74,522 | **Forks**: 9,440 | **Watchers**: 444
- **Age**: 26 months (created March 2024)
- **Star velocity**: ~2,866 stars/month (explosive growth)
- **Contributors**: 470+
- **Open issues**: 399
- **Releases**: 101 (latest: v1.7.0, May 1 2026)
- **Release cadence**: Monthly (v1.3 Feb → v1.4 Feb → v1.5 Mar → v1.6 Mar → v1.7 May)
- **Recent activity**: Multiple commits daily, including self-authored commits by OpenHands agents
- **Trusted by**: TikTok, VMware, Roche, Amazon, C3.ai, Netflix, Mastercard, Red Hat, MongoDB, Apple, NVIDIA, Google

## Architecture
```
OpenHands/
├── .agents/           # Agent definitions
├── .openhands/        # Self-referential config (OpenHands developing itself)
├── openhands/         # Core Python package
│   ├── analytics/     # Usage tracking
│   ├── app_server/    # REST API server
│   ├── server/        # WebSocket server
│   └── version.py
├── frontend/          # React GUI
├── enterprise/        # Enterprise tier (separate license)
│   ├── integrations/  # Slack, Jira, GitHub, GitLab, Bitbucket, Bitbucket DC
│   ├── server/        # SaaS server
│   ├── storage/       # Persistent storage
│   ├── sync/          # Data synchronization
│   └── migrations/    # Database migrations (Alembic)
├── skills/            # Shareable knowledge agents
│   ├── github.md      # GitHub operations
│   ├── docker.md      # Docker guidelines
│   ├── kubernetes.md  # K8s setup
│   ├── code-review.md # Code review process
│   ├── security.md    # Security best practices
│   └── 25+ more...
├── containers/        # Docker build definitions
├── tests/             # Test suite
├── scripts/           # Build/deploy scripts
└── AGENTS.md          # Self-developing guide (OpenHands uses itself)
```

## Key Design Decisions
1. **SDK-first architecture**: The Software Agent SDK is the core engine. CLI, GUI, Cloud, and Enterprise are all built on top of it. This means any improvement to the SDK benefits all deployment modes.

2. **Skills system (formerly Microagents)**: Domain knowledge is injected via markdown files with YAML frontmatter. Two tiers: public shareable skills (in `skills/`) and private repo-specific skills (in `.openhands/skills/`). Keyword-triggered activation.

3. **Docker sandbox by default**: All agent execution happens in isolated Docker containers. This is critical for security (agents execute arbitrary code) and reproducibility.

4. **Model-agnostic**: Works with any LLM — Claude, GPT, Qwen, Devstral, open-source models. Not locked to one provider. This is a key differentiator vs. Claude Code (Anthropic-only) or Copilot (OpenAI-only).

5. **Self-developing**: OpenHands literally develops itself — AGENTS.md contains instructions for OpenHands agents working on the OpenHands codebase. Recent commits are co-authored by `openhands@all-hands.dev`.

6. **Enterprise as source-available**: Enterprise code is visible in the repo (`enterprise/` directory) but requires a paid license for production use beyond one month. Integrations include Slack, Jira, GitHub, GitLab, Bitbucket, Bitbucket Data Center.

## Enterprise Integrations
- **GitHub** — PR automation, code review, issue triage
- **GitLab** — same capabilities
- **Bitbucket / Bitbucket Data Center** — same capabilities
- **Slack** — agent interactions via Slack
- **Jira / Jira DC** — ticket-driven agent workflows
- **Stripe** — billing/subscription management (SaaS)

## Integration Potential for PeopleTech

### Use Case Realization (Hyundai ML Pipeline)
OpenHands can accelerate development of the 8 AI use cases:

| Use Case | OpenHands Component | Acceleration |
|----------|-------------------|-------------|
| UC05 Predictive Quality | CodeAct Agent + Skills | Agent writes PyTorch training code from data schema |
| UC04 SOP Compliance | Multi-agent delegation | Parallel pose estimation models per station type |
| UC07 Safety Monitoring | Agent Server (K8s) | Production inference scaling across camera fleet |
| UC01 Visual Inspection | Skills system | Domain knowledge: defect taxonomy per model variant |
| UC02 Variant Confirmation | CodeAct + MCP | BOM validation logic with MES integration via MCP |
| UC08 Digital Traceability | Docker Workspace | Isolated graph DB dev + IATF compliance tests |

### Enterprise Deployment Model
- Self-hosted in Hyundai VPC via Kubernetes
- Per-plant isolation via multi-user workspaces
- GitHub Actions for ML pipeline CI/CD
- Skills inject manufacturing domain expertise

### Development Velocity Claim
- Traditional ML dev: 3-6 months per use case
- With OpenHands agents: 2-4 weeks per use case (10x claim)
- Basis: agents write boilerplate training code, test suites, CI/CD configs, deployment scripts

## Competitor Comparison
| Platform | Focus | LLM Support | Enterprise | Open Source |
|----------|-------|-------------|-----------|-------------|
| **OpenHands** | AI-driven development | Any LLM | Self-hosted K8s | MIT (core) |
| Claude Code | CLI coding | Anthropic only | No | No |
| GitHub Copilot | IDE assistant | OpenAI | Yes | No |
| Cursor | IDE | Multi-model | No | No |
| Devin | Autonomous agent | Proprietary | Yes | No |
| Windsurf | IDE | Multi-model | No | No |

**OpenHands advantage**: Only platform that is open-source, model-agnostic, self-hostable, AND provides a composable SDK for building custom agent workflows.

## Steal-Worthy Elements
- **AGENTS.md pattern**: Self-referential development guide that lets agents work on the codebase itself. We use CLAUDE.md similarly.
- **Skills system**: Keyword-triggered domain knowledge injection via markdown files. Directly maps to our skills architecture.
- **Docker sandbox**: Agent execution in isolated containers. Critical for manufacturing AI where you can't risk production data leaks.
- **Self-developing commits**: Bot commits co-authored by agents. Shows confidence in the tool.
- **SWE-Bench 77.6%**: Quantified benchmark score gives credibility. We should benchmark our own agent capabilities.

## Quotable
- "Define agents in code, then run them locally, or scale to 1000s of agents in the cloud."
- "While other agent SDKs (e.g. LangChain) are focused on more general use cases, OpenHands is purpose-built for software engineering."
- "OpenHands is the foundation for secure, transparent, model-agnostic coding agents — empowering every software team to build faster with full control."
