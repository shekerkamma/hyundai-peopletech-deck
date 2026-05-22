# Helpline AI Layer — Article Alignment & Video Map

This repo is a worked, **fully validated** example of Anthropic's article
*"How Claude Code works in large codebases: best practices and where to start."*
Helpline shipped with **no AI Layer**; every piece below was built on top of it
and tested end to end (`VALIDATION.md` — 13/13).

Article thesis: **the harness — the ecosystem built around the model —
determines how Claude Code performs more than the model alone.**

> *"AI Layer" is our name for that harness. Anthropic's article describes the
> harness and its components; it does not use the phrase "AI Layer."*

---

## The extension points — article → artifact → proof

| Extension point | What the article says | Built here | Proof |
|---|---|---|---|
| **CLAUDE.md files** | Loaded first; lean root, subdirectory files load additively as Claude walks the tree | `CLAUDE.md` (lean root) + 7 subdirectory files in each service/package | `validate_all.py` → "CLAUDE.md hierarchy" |
| **Hooks** | Best use is *self-improving* setup, not just prevention. "A start hook can load team-specific context dynamically." "A stop hook can reflect on what happened during a session and propose CLAUDE.md updates while the context is fresh." | `SessionStart` hook loads dynamic orientation (active areas + recent commits). `Stop` hook = a deterministic trigger (`propose_claude_md.py`) that spawns a background reflector (`reflect_claude_md.py`); the reflector calls headless `claude -p` to reflect on the session diff and write concrete proposed `CLAUDE.md` edits — with a deterministic fallback if `claude` is unavailable | `validate_all.py` → "Hook — Stop": both files compile, recursion guard holds, a real end-to-end reflection writes `.claude/claude-md-review.md` |
| **Skills** | On-demand expertise, progressive disclosure, scoped to specific paths | `billing-money-rules`, `api-add-route` (both with `references/`), `scoped-tests` — each scoped with the `paths:` glob frontmatter field, so a skill auto-loads only when the agent works in its part of the repo | `validate_all.py` → "Skills": frontmatter + `paths:` scoping |
| **Plugins** | Bundle skills/hooks/MCP into installable packages, distribute via a marketplace | `tooling/helpline-ai-layer/` plugin + `tooling/.claude-plugin/marketplace.json`; bundles only the repo-agnostic pieces (generic `scoped-tests`, hooks, explorer, MCP) | "Plugin" check — 8 files, all JSON valid |
| **LSP** | Symbol-level precision instead of text-pattern false positives | pyright + `pyright-langserver`, configured in `[tool.pyright]` | `check_lsp.py` — real `initialize` handshake, 16 capabilities |
| **MCP servers** | Expose structured search as a callable tool | `codebase-search` server — `where_is`, `find_references`, `outline`, all **AST-based** (parses every module; never substring-matches), wired via `.mcp.json` | `check_mcp.py` — real handshake + all three tools called |
| **Subagents** | Split exploration from editing — read-only mapper, separate context window | `.claude/agents/explorer.md` — **genuinely read-only** (`tools: Read, Grep, Glob` — no Write/Edit), returns findings as its report to the parent | "Subagent" check asserts no write tools are granted |

---

## The 3 configuration patterns

### Pattern 1 — Make the codebase navigable at scale
- **Lean, layered CLAUDE.md** — root holds only repo-wide truths; each service
  and package carries its own conventions.
- **Initialized in subdirectories**, not just the root — Claude walks up the
  tree, so local context is never lost.
- **`CODEBASE_MAP.md`** — find where a feature lives before exploring.
- **`.claudeignore`** — generated files, caches, `uv.lock` excluded.
- **Scoped test commands** — every service `CLAUDE.md` and the `scoped-tests`
  skill say "run *your* service's tests, not the full suite."
- **LSP** — symbol search instead of grep false-positives.

### Pattern 2 — Actively maintain CLAUDE.md as models evolve
- The **`Stop` hook** is the proactive half, split in two so the turn never
  blocks on a model call: `propose_claude_md.py` cheaply detects which areas
  changed and spawns `reflect_claude_md.py` in the background; the reflector
  asks headless `claude -p` to reflect on the session's diff and draft concrete
  `CLAUDE.md` edits into `.claude/claude-md-review.md`. The AI Layer proposes
  its own updates instead of rotting silently. A recursion guard stops the
  nested `claude` from re-triggering the hook; a deterministic fallback flags
  the touched areas if `claude` is unavailable.
- **Review cadence:** a full `CLAUDE.md` / skills / hooks review every **3–6
  months**, and after any major model release. Rules written for an older
  model's limits (e.g. "refactor one file at a time") become a drag once newer
  models can do coordinated cross-file edits — delete them when that happens.

### Pattern 3 — Assign ownership
- The **Platform Team** owns `tooling/` and `.claude/` — one DRI for
  configuration, the plugin marketplace, and `CLAUDE.md` conventions.
- The **plugin is the distribution mechanism**: a new repo or new engineer runs
  one install and gets the team's baseline layer on day one, instead of
  bottoms-up fragmentation.

---

## Getting started — the article's 4 phases

| Phase | Article | In this repo |
|---|---|---|
| Foundation | CLAUDE.md hierarchy, ignore rules, LSP | `CLAUDE.md` ×8, `.claudeignore`, pyright |
| Infrastructure | skills, MCP, plugin distribution | 3 skills, `codebase-search` MCP, `helpline-ai-layer` plugin |
| Governance | review requirements, DRI, approvals | *Partial by nature* — version-controlled `.claude/settings.json` permissions is the one concrete artifact; the DRI, approved-skills list, and review process are organizational and live outside any single repo (Pattern 3 documents the intent) |
| Scale | expand skills/plugins, iterate CLAUDE.md, periodic review | the `Stop` hook + the 3–6 month cadence above |

---

## Validation

Everything above is verified by `tooling/validate/validate_all.py` →
`VALIDATION.md` (**13/13**). Re-run any time:

```bash
uv run --extra dev python tooling/validate/validate_all.py
```

---

## Video map — "How Claude Code Works in Large Codebases" (May 20)

Demo-by-demo structure. Each demo is a real artifact in this repo, already
tested — nothing is faked.

1. **Cold open** — the article on screen: *"the harness matters as much as the
   model."* Open `helpline/` cold — no AI Layer. This is every real codebase.
2. **CLAUDE.md hierarchy** — show the lean root vs a subdirectory file; explain
   additive directory-walk loading. *Article: load first.*
3. **Codebase map + `.claudeignore`** — how Claude finds a feature without
   reading everything.
4. **Hooks** — run the `SessionStart` orientation hook live (active areas +
   recent commits). Then make a real change in a service and end the turn: the
   `Stop` hook spawns the reflector, `claude -p` reflects on the diff, and a
   concrete proposed `CLAUDE.md` edit lands in `.claude/claude-md-review.md`.
   *Article: a stop hook can reflect on a session and propose CLAUDE.md updates.*
5. **Skills** — edit a file in `services/billing`: `billing-money-rules`
   auto-loads because its `paths:` glob matches; show progressive disclosure
   into `references/`, then edit elsewhere and show it does *not* load.
   *Article: skills scoped to specific paths.*
6. **LSP** — `check_lsp.py` handshake; symbol search vs grep.
7. **MCP** — call the `codebase-search` server live: `where_is`,
   `find_references`, `outline` — AST-based, structurally precise where grep
   guesses. *Article: structured search as a callable tool.*
8. **Subagent** — dispatch the genuinely read-only `explorer` (no write tools)
   to map a service; it returns a report, the main agent edits.
9. **Plugin** — install `helpline-ai-layer` from the marketplace; everything
   above lands in one command. *Article: distribute what works.*
10. **The 3 patterns + the 3–6 month review** — close on Pattern 2's
    model-evolution point and the ownership/DRI pattern.
11. **Outro** — run `validate_all.py`: 13/13. Tease the May 27 kickoff-skills
    video as the how-to that comes next.
