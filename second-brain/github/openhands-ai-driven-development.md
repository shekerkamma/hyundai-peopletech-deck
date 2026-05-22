---
title: "OpenHands"
source: https://github.com/shekerkamma/OpenHands
source_type: github-repo
owner: OpenHands (fork by shekerkamma)
stars: 0 (fork) | upstream ~65k+
language: Python
license: MIT (core) + Enterprise license (enterprise/)
date_watched: 2026-05-21
tags: [content-research, github, python, typescript, ai-coding, ai-agent, devtools, #source/github]
---

# OpenHands/OpenHands

## TL;DR
OpenHands is a leading open-source AI-driven software development platform (formerly OpenDevin). It provides a full stack — SDK, CLI, local GUI, cloud, and enterprise — for building and running AI coding agents. It scores **77.6% on SWE-Bench**, making it one of the top-performing AI coding systems. Trusted by engineers at Apple, Google, NVIDIA, Amazon, Netflix, and more.

## What It Does
OpenHands is a complete ecosystem for AI-powered software development:

- **Software Agent SDK** — Composable Python library for defining and running AI agents. Scale from local to 1000s of agents in the cloud.
- **CLI** — Terminal-based coding assistant (comparable to [[Claude Code]] or [[Codex]]). Works with Claude, GPT, or any LLM.
- **Local GUI** — REST API + React SPA for running agents on your laptop (comparable to [[Devin]] or [[Jules]]).
- **Cloud** — Hosted version at app.all-hands.dev with free tier (Minimax model). Includes Slack, Jira, Linear integrations, RBAC, and collaboration features.
- **Enterprise** — Self-hosted in customer VPC via Kubernetes. Source-available with paid licensing.

## Tech Stack
- **Primary Language**: Python (6.6M lines) — core agent runtime, SDK, server
- **Frontend**: TypeScript (3.8M lines) — React SPA
- **Infrastructure**: Docker, Docker Compose, Kubernetes (enterprise)
- **Templates**: Go Template (91k), Jinja (22k)
- **Build**: Makefile, Shell scripts
- **Package Management**: Poetry + UV (Python), npm (frontend)
- **Config**: TOML-based (`config.template.toml`)
- **Testing**: pytest

## Traction
- **Stars**: ~65k+ (upstream OpenHands/OpenHands — this is a personal fork with 0 stars)
- **Forks**: Heavily forked (this repo is itself a fork)
- **Contributors**: 600+ (upstream), top contributors include xingyaoww (626), tofarr (570), rbren (478)
- **Age**: Active since 2024 (originally OpenDevin, rebranded to OpenHands)
- **Recent activity**: Very active — multiple commits daily (last commit May 21, 2026)
- **SWE-Bench score**: 77.6% — competitive with top commercial tools
- **Trusted by**: TikTok, VMware, Roche, Amazon, C3 AI, Netflix, Mastercard, Red Hat, MongoDB, Apple, NVIDIA, Google

## Architecture
```
OpenHands/
├── openhands/              # Core Python package
│   ├── __init__.py
│   ├── analytics/          # Usage analytics
│   ├── app_server/         # Application server
│   ├── server/             # API server
│   └── version.py
├── enterprise/             # Enterprise features (separate license)
│   ├── integrations/       # Slack, Jira, Linear
│   ├── server/             # Enterprise server
│   ├── storage/            # Enterprise storage layer
│   ├── sync/               # Sync capabilities
│   ├── migrations/         # DB migrations (Alembic)
│   └── tests/
├── frontend/               # React SPA (TypeScript)
├── containers/             # Docker configs
├── kind/                   # Kubernetes configs
├── scripts/                # Build & utility scripts
├── tests/                  # Test suite
├── skills/                 # Agent skill definitions
├── .agents/                # Agent configurations
└── docker-compose.yml      # Local dev orchestration
```

## Key Design Decisions
- **Modular product surface**: SDK / CLI / GUI / Cloud / Enterprise are separate but share the same core engine
- **LLM-agnostic**: Works with Claude, GPT, or any LLM — not locked to one provider
- **MIT + Enterprise dual license**: Core is fully open-source MIT; enterprise/ directory has separate commercial license
- **SWE-Bench as north star**: 77.6% score signals serious investment in agent quality
- **Docker-native**: Agents run in containers for isolation and reproducibility
- **Community-driven**: Active Slack, 600+ contributors, public roadmap on GitHub Projects

## Integration Potential
- **Use case for us**: Could serve as the backbone for AI-driven development workflows in manufacturing/plant operations — agent SDK for automating repetitive coding tasks, CLI for developer productivity
- **Relevance to Hyundai**: The enterprise self-hosted model (VPC + K8s) aligns with manufacturing security requirements. The agent SDK could power custom automation agents for plant operations software
- **Effort to integrate**: Medium — well-documented, Docker-based, but would need LLM API access and infrastructure
- **License**: MIT for core (fully permissive), enterprise features require commercial license

## Competitive Landscape
| Tool | Type | Key Differentiator |
|------|------|--------------------|
| **OpenHands** | Open-source platform | Full stack (SDK → Enterprise), 77.6% SWE-Bench |
| [[Claude Code]] | CLI | Anthropic-native, deep Claude integration |
| [[Codex]] | CLI | OpenAI-native, GPT integration |
| [[Devin]] | Cloud GUI | First AI software engineer, commercial |
| [[Jules]] | Cloud GUI | Google-backed, Gemini-native |
| [[Cursor]] | IDE | AI-augmented IDE, not agent-based |

## Steal-Worthy Elements
- **Dual-license model** (MIT core + Enterprise) — great template for open-source commercialization
- **Product ladder**: SDK → CLI → GUI → Cloud → Enterprise, each step adds value
- **SWE-Bench benchmarking** as a credibility signal — hard metrics build trust
- **Multi-LLM support** — avoids vendor lock-in, broadens market
- **Enterprise self-hosting via K8s** — critical for regulated industries
- **"Trusted by" social proof** with major tech logos — powerful for enterprise sales

## Backlinks
- [[Claude Code]] — competitor in AI coding CLI space
- [[Codex]] — competitor in AI coding CLI space  
- [[Devin]] — competitor in AI coding agent space
- [[Jules]] — competitor in AI coding agent space
- [[SWE-Bench]] — primary benchmark for evaluation
- [[AI Coding Agents]] — broader category
- [[Software Agent SDK]] — OpenHands' core composable library
