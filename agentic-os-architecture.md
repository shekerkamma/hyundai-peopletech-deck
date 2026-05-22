# Agentic OS — Architecture Guide

## What is Agentic OS?

Agentic OS is an operating system architecture for AI-powered work. It organizes how an AI agent (like Claude Code) inherits shared knowledge, adapts to individual clients or projects, remembers context across sessions, and executes multi-step workflows autonomously. Think of it as the difference between a single chatbot conversation and a fully staffed, always-on AI department that knows your brand, your clients, and your history.

---

## Architecture Overview

The system has four layers, each with a distinct responsibility:

1. **Shared Context** — Universal knowledge, skills, and brand standards available to every project
2. **Client/Project Context** — Isolated, per-client configuration that overrides shared defaults
3. **Memory Layer** — Persistent recall split into always-loaded and on-demand retrieval
4. **Execution Layer** — Runtime infrastructure: chained workflows, scheduled jobs, always-on availability, and multi-channel access

---

## Component: Shared Context

The foundation layer. Everything here applies to every project and every client unless explicitly overridden.

### What it contains:

- **Work Preferences** (`CLAUDE.md`, `SOUL.md`, `user.md`) — How you like to work, your non-negotiables, tone and style rules. These are the "brand manual" of the operation.
- **Skills** — Reusable capabilities: research, copywriting, video production, cron automation, and more. Each skill is a structured instruction set the AI follows when invoked via `/skill-name`.
- **Global Brand Context** — Your voice profile (`voice-profile.md`), ideal customer profile (`icp.md`), positioning statement (`positioning.md`), asset library (`assets.md`). These ensure consistent messaging regardless of which project is active.
- **Planning Frameworks** — Three tiers of task complexity: quick task (do it now), planned project (multi-step with milestones), full business plan (strategic with dependencies). The AI selects the appropriate framework based on the scope of the request.
- **Output Storage** — Standardized output structure: `projects/ > category/ > date/`. Every deliverable lands in a predictable location.
- **Shared Files** — Team and relationship context (`team-and-relationships.md`), goals and priorities (`goals-and-priorities.md`), and any additional shared documents.

### Directory structure:

```
agentic-os/
├── CLAUDE.md              # Root rules — loaded every session
├── clients/               # Per-client isolated contexts
├── context/               # Shared context files
│   ├── brand_context/     # Voice, ICP, positioning
│   ├── learnings.md       # Accumulated insights
│   └── memory/            # Dated memory entries
├── projects/              # Output storage
└── .claude/skills/        # Skill definitions
```

---

## Component: Client/Project Context

Each client or project gets an isolated workspace that inherits from Shared Context but can override any part of it.

### What it contains:

- **Client CLAUDE.md** — Overrides the root CLAUDE.md. If Client 3 says "our design language is unique," that instruction takes precedence over shared design rules for all work within that client's scope.
- **Client Brand Context** — A separate brand identity per client. Client 1 might be luxury hospitality, Client 2 corporate finance. Each gets its own voice, assets, and positioning.
- **Client Skills** — Skills scoped to a specific client. Client 1 might have a `landing-page` skill tailored to their CMS. Client 3 might have a `taste-skill` that encodes their aesthetic preferences.
- **Project Plans** — Active plans, briefs, and deliverable trackers scoped to the client.
- **Context Overwrites** — The overwrite mechanism: when a client-level file exists with the same name as a shared-level file, the client version wins. This applies to CLAUDE.md, skills, brand context, project plans, and outputs.

### Key design decision: Isolation over inheritance

Each client directory is fully self-contained. You can delete a client folder without affecting any other client or the shared context. This prevents cross-contamination of brand voice, confidential information, or project state between clients.

---

## Component: Memory Layer

Persistent recall that survives across sessions, split into two tiers based on retrieval cost.

### Fed Every Time (always loaded)

These files are read at the start of every session, regardless of context:

- **learnings.md** — Accumulated insights and feedback. "Client A prefers bullet points over prose." "The Hyundai team responds better to ROI-first framing."
- **memory/** — Dated memory entries (e.g., `2026-05-01.md`, `2026-05-15.md`). Chronological record of decisions, outcomes, and context that might be relevant.
- **hooks** — SessionStart and SessionStop hooks that automatically orient the AI and capture learnings at the end of each session.

### Retrieved When Needed (on-demand)

These systems are queried only when the AI needs deeper context:

- **MCP-SEARCH** — Semantic search across all stored content. "Find everything related to pricing objections."
- **MEMHULCE** — Word-for-word retrieval. Exact quotes, specific numbers, precise contract terms.
- **LLM Wiki / Obsidian** — Relational knowledge. "What connects Client A's Q3 goals to the product roadmap?"
- **Cross-tool / OpenBrain** — Cross-application retrieval. Search across Notion, Slack, email, and local files simultaneously.

### Key design decision: Two-tier retrieval

Loading everything into every session would be slow and noisy. The two-tier split ensures the AI always has recent, high-signal context (tier 1) while keeping deep archives accessible but not cluttering the working memory (tier 2).

---

## Component: Execution Layer

The runtime infrastructure that makes the system operational beyond a single chat session.

### Sub-components:

- **Skill Systems** — Multi-step workflows where multiple skills chain together in sequence to achieve a "job to be done." Example: `/architecture-presentation` chains draw.io diagram → markdown doc → pptx deck → NotebookLM notebook.
- **Cron Jobs** — Scheduled tasks that run without manual invocation. Morning briefings, weekly retros, daily data pulls. These run on a schedule or in response to events.
- **UPS / Always On** — No dependency on your laptop being open. The system runs 24/7 on cloud infrastructure, processing queued tasks, monitoring dashboards, and responding to triggers.
- **Channels** — Multi-channel access: desktop CLI, mobile app, web interface, Slack integration. The same AI, same context, same skills — accessible from anywhere.

### Key design decision: Modular execution

Each execution mechanism is independent. You can use skill chains without cron. You can use cron without always-on. You can access from mobile without changing anything about how skills or memory work. This modularity means teams adopt what they need without committing to the full stack.

---

## Key Data Flows

### A typical client interaction

1. **Session starts** → Hooks fire: `SessionStart` loads learnings.md, recent memory entries, and orients the AI to the current project state
2. **Shared context loads** → CLAUDE.md, SOUL.md, user.md set the baseline rules and preferences
3. **Client context overrides** → If working in `clients/client-one/`, the client's CLAUDE.md and brand context override shared defaults
4. **User invokes a skill** → e.g., `/content-research` — the AI follows the skill's structured instructions
5. **Memory consulted** → If the skill needs historical context, tier-1 memory is already loaded; tier-2 is queried on demand via MCP-SEARCH or MEMHULCE
6. **Output generated** → Deliverable saved to `projects/ > category/ > date/`
7. **Session ends** → `SessionStop` hook fires: captures learnings, proposes CLAUDE.md updates, writes memory entries

### A scheduled workflow

1. **Cron trigger fires** → e.g., "Every Monday 9 AM"
2. **Skill chain executes** → Morning briefing skill reads news feeds, checks project status, scans Slack
3. **Memory updated** → New learnings written to dated memory file
4. **Output delivered** → Briefing sent via Slack channel
5. **No human intervention** → Runs on UPS infrastructure, laptop can be closed

---

## Design Decisions

- **Files over databases**: All context is stored as markdown files in a directory tree. This makes the system inspectable (you can `cat` any file), versionable (git tracks everything), and portable (copy the folder to move the system). The tradeoff is query performance, which the memory frameworks compensate for.

- **Override over merge**: Client context doesn't merge with shared context — it overwrites. This prevents subtle bugs where a client inherits an unwanted shared rule. If you want shared behavior, don't override. If you want custom behavior, replace the file entirely.

- **Skills over prompts**: Instead of long, fragile system prompts, each capability is packaged as a skill with structured instructions, triggers, and output formats. Skills are versioned, testable, and composable. A prompt is a one-shot instruction; a skill is a reusable unit of work.

- **Two-tier memory over flat recall**: Loading all memory into every session is wasteful and creates noise. The always-loaded tier (learnings, recent memories, hooks) covers 90% of cases. The on-demand tier (semantic search, relational lookup) handles the long tail without cluttering context.

- **Isolation per client**: Each client gets a fully isolated directory. No shared state, no cross-contamination. This is critical for agencies and consultancies serving multiple clients with different brand guidelines, confidential information, and project timelines.
