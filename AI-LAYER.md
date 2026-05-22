# PeopleTech Deck AI Layer — Architecture & Alignment

Built following Anthropic's article *"How Claude Code works in large codebases:
best practices and where to start"* using [coleam00/helpline](https://github.com/coleam00/helpline)
as the reference implementation.

Article thesis: **the harness — the ecosystem built around the model —
determines how Claude Code performs more than the model alone.**

---

## The extension points — what was built

| Extension point | What the article says | Built here |
|---|---|---|
| **CLAUDE.md files** | Lean root, subdirectory files load additively | `CLAUDE.md` (lean root) + `second-brain/CLAUDE.md` + `CODEBASE_MAP.md` |
| **Hooks** | Self-improving setup, not just prevention | `SessionStart` hook loads git orientation + active work areas. `Stop` hook triggers background reflector proposing CLAUDE.md updates |
| **Skills** | On-demand expertise, path-scoped progressive disclosure | `deck-builder`, `architecture-diagram`, `content-research-ingest`, `customer-facing-review` — each scoped with `paths:` globs |
| **LSP / MCP** | Symbol-level precision, structured search as callable tools | `codebase-search` MCP server with AST-based `where_is`, `find_references`, `outline`, `search_content` |
| **Subagents** | Split exploration from editing | `explorer` agent — genuinely read-only (`tools: Read, Grep, Glob`), maps workspace areas |
| **Plugins** | Bundle into installable packages | `tooling/peopletech-ai-layer/` — portable plugin with hooks, skills, MCP, and agent |

---

## The 3 configuration patterns

### Pattern 1 — Make the workspace navigable at scale
- **Lean, layered CLAUDE.md** — root holds repo-wide truths; `second-brain/` carries its own
- **`CODEBASE_MAP.md`** — find which build script produces which deliverable
- **`.claudeignore`** — generated binaries (.pptx, .png), node_modules, graphify-out excluded
- **Path-scoped skills** — deck conventions load only when editing build scripts
- **MCP** — AST-based search instead of grep false-positives

### Pattern 2 — Actively maintain CLAUDE.md as models evolve
- **`Stop` hook** — `propose_claude_md.py` detects changed areas, spawns `reflect_claude_md.py`
  in background. Reflector asks headless `claude -p` to review conventions and writes
  `.claude/claude-md-review.md`. Recursion guard + dedup fingerprint + deterministic fallback.
- **Review cadence:** full CLAUDE.md / skills / hooks review every 3-6 months and after
  major model releases.

### Pattern 3 — Assign ownership
- The **plugin** (`tooling/peopletech-ai-layer/`) is the distribution mechanism.
  New workspace or new team member installs once and gets the baseline AI Layer.

---

## File inventory

```
CLAUDE.md                           # Root — lean, repo-wide truths
CODEBASE_MAP.md                     # Navigational map of all deliverables
.claudeignore                       # Exclude generated binaries + caches
.mcp.json                           # MCP server wiring
second-brain/CLAUDE.md              # Research notes conventions

.claude/
  settings.json                     # Permissions + hook wiring
  hooks/
    session_start_context.py        # SessionStart — git orientation
    propose_claude_md.py            # Stop — trigger (cheap, deterministic)
    reflect_claude_md.py            # Stop — reflector (LLM call, background)
  skills/
    deck-builder/
      SKILL.md                      # Build script conventions
      references/deck-conventions.md
    architecture-diagram/
      SKILL.md                      # Draw.io diagram conventions
      references/use-case-index.md
    content-research-ingest/
      SKILL.md                      # Research note ingest rules
    customer-facing-review/
      SKILL.md                      # Pre-ship review checklist
  agents/
    explorer.md                     # Read-only workspace explorer

tooling/
  mcp/
    codebase_search.py              # AST-based search MCP server
  peopletech-ai-layer/              # Distributable plugin bundle
    .claude-plugin/plugin.json
    hooks/hooks.json
    hooks/propose_claude_md.py
    hooks/reflect_claude_md.py
    skills/customer-facing-review/SKILL.md
    agents/explorer.md
    mcp/codebase_search.py
  .claude-plugin/
    marketplace.json                # Plugin marketplace manifest

helpline-reference/                 # Reference codebase (coleam00/helpline)
```

---

## Getting started

### For this workspace
Everything is already wired. Start a new Claude Code session and the
`SessionStart` hook will orient you automatically.

### For a new workspace
Install the portable plugin:
```bash
/plugin marketplace add /path/to/this/repo/tooling
/plugin install peopletech-ai-layer
```

### Reference
The `helpline-reference/` directory contains the full helpline codebase by
coleam00 — the worked example from Anthropic's article. Compare any component
here against its helpline counterpart to understand the pattern.
