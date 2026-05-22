# Helpline

Helpline is a B2B helpdesk and customer-support platform — an internal monorepo
where five services (`api`, `auth`, `billing`, `notifications`, `search`) talk
over HTTP and share two internal packages (`core`, `db`). It's the kind of
mid-sized, multi-service codebase where an AI coding agent either pays for
itself or quietly makes a mess: shared packages that everything imports, money
rules that must never silently regress, a request gateway with its own
conventions, and tests scattered across services.

## Quick start

**What this repo actually is.** Helpline is a *demonstration codebase*, built
for the YouTube video **"The AI Layer: How to Make Claude Code Work in Large
Codebases."** It is a deliberately realistic — but compact — complex codebase,
used to show *concretely* how to build an **AI Layer** — our name for the
harness of configuration and tooling that Anthropic's article describes in
[*How Claude Code works in large codebases*](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start).
(The article describes the harness and its components; "AI Layer" is our term
for it, not Anthropic's.)
That article is the *what* and the *why*, and it is excellent — but it stays
high-level. Helpline is the *how*: every component from the article, built and
validated on a real codebase. The rest of this repo is written as if Helpline
were a live product, because that is exactly how you should treat your own
codebase when you give it an AI Layer.

**Run it:**

```bash
git clone https://github.com/coleam00/helpline.git
cd helpline
uv sync --extra dev
uv run pytest                 # the application's own test suite
```

**See the AI Layer:** read **[`AI-LAYER.md`](AI-LAYER.md)** — it maps every
component to the article and to where it lives in this repo. Then run the
validator, which proves every piece works end to end:

```bash
uv run --extra dev python tooling/validate/validate_all.py   # 13/13
```

## The AI Layer, concretely

Every codebase you ship with an AI agent has three parts: **code**, **tests**,
and — the new one — the **AI Layer**: the configuration, context, and reusable
workflows that make an agent productive in *your* codebase. Helpline builds
every component the article names:

| Component (from the article) | Built here | Where |
|-------------------------------|------------|-------|
| **CLAUDE.md hierarchy** | lean root `CLAUDE.md` + one per service/package, loaded additively | `CLAUDE.md`, `*/CLAUDE.md` |
| **Hooks** | a `SessionStart` orientation hook + a self-improving `Stop` hook that reflects on the session and proposes concrete `CLAUDE.md` edits | `.claude/hooks/` |
| **Skills** | `billing-money-rules`, `api-add-route`, `scoped-tests` — glob-scoped with the `paths:` field, progressive disclosure into `references/` | `.claude/skills/` |
| **Subagent** | a genuinely read-only `explorer` (no write tools) that maps a subsystem and reports back | `.claude/agents/explorer.md` |
| **LSP** | pyright + `pyright-langserver` for symbol-level navigation | `docs/lsp-setup.md` |
| **MCP** | `codebase-search` — AST-based `where_is` / `find_references` / `outline` | `tooling/mcp/` |
| **Plugin** | `helpline-ai-layer` — bundles the portable pieces for one-command install | `tooling/helpline-ai-layer/` |

The git history is the before/after, on purpose: **commit 1** is Helpline with
*no* AI Layer; **commit 2** adds *the entire layer*.

## Take this to your own codebase

Helpline is not just something to read — it is something to *reuse*. There are
two ways, and both matter more than the codebase itself.

### 1. Install the plugin — the fastest path

The portable, repo-agnostic pieces of the AI Layer are bundled as a Claude Code
plugin at `tooling/helpline-ai-layer/`. From your own project:

```
/plugin marketplace add /path/to/helpline/tooling
/plugin install helpline-ai-layer@helpline-tooling
```

That one install gives *your* repo:

- the **self-improving Stop hook** — reflects on each session and proposes
  `CLAUDE.md` updates, so your layer never silently rots;
- the **read-only `explorer` subagent** — maps a subsystem without burning your
  main session's context;
- the **`codebase-search` MCP** — AST-based structured search;
- a generic **`scoped-tests`** skill.

These are deliberately layout-agnostic: the hooks follow *your* `CLAUDE.md`
hierarchy, and the MCP discovers *your* source by walking the repo. Nothing is
tied to Helpline's directory names.

### 2. Point your coding agent at this repo

You don't have to copy anything by hand. Clone Helpline, open it alongside your
project, and tell your agent something like:

> Read `AI-LAYER.md` and the `.claude/` folder in the Helpline repo. It is a
> worked example of the AI Layer from Anthropic's large-codebases article.
> Build a comparable AI Layer for *this* codebase — a CLAUDE.md hierarchy,
> hooks, skills, an MCP, a subagent — adapted to our structure and conventions.

`AI-LAYER.md` exists for exactly this. It is an agent-readable map from each
article concept to the artifact that implements it, plus the proof that it
works. The repo is a reference implementation your agent can learn the *pattern*
from — not boilerplate to clone blindly.

### What travels, and what you rebuild

| Generalizable — works in any repo | Repo-specific — rebuild for yours |
|-----------------------------------|------------------------------------|
| the `Stop` / `SessionStart` hooks (CLAUDE.md-hierarchy based) | the `CLAUDE.md` files (your conventions) |
| the `explorer` subagent | `billing-money-rules`, `api-add-route` (your domain skills) |
| the `codebase-search` MCP | — |
| the generic `scoped-tests` skill | — |

The repo-specific pieces aren't reusable *content* — but they are reusable
*templates*. Copy the shape, change the substance.

## Layout

```
services/
  api/            HTTP gateway — routes, request handling
  auth/           authentication — tokens, password hashing
  billing/        subscriptions + invoicing
  notifications/  outbound email + templating
  search/         ticket search indexing + queries
packages/
  core/           shared domain models + error types
  db/             database connection + repositories
infra/            docker-compose for local dev
scripts/          one-off operational scripts
tests/            cross-service integration tests
tooling/          the AI Layer's MCP server, the plugin, and the validators
```

Each service owns its own area. `packages/core` and `packages/db` are imported
by every service — change them carefully.

## Dev

```bash
uv sync --extra dev      # install
uv run pytest            # full test suite
uv run pyright           # type-check
```
