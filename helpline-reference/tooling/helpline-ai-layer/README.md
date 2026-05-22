# helpline-ai-layer (plugin)

The article's "distribute what works" pattern: bundle the parts of an AI Layer
that aren't repo-specific into one installable package, so a new repo or a new
engineer gets the team's baseline Claude Code setup immediately — no manual
copying of hooks and skills.

## What's bundled

| Component | File | What it does |
|-----------|------|--------------|
| Skill | `skills/scoped-tests/` | Picks the correctly scoped test command instead of the full suite. |
| Hook (trigger) | `hooks/hooks.json` + `hooks/propose_claude_md.py` | Stop hook — detects which areas changed and spawns the reflector in the background (self-improving). |
| Hook (reflector) | `hooks/reflect_claude_md.py` | Calls headless `claude -p` to reflect on the session diff and propose concrete `CLAUDE.md` edits. Falls back to a deterministic note if `claude` is unavailable. |
| Subagent | `agents/explorer.md` | Genuinely read-only explorer (`Read, Grep, Glob` — no write tools) — maps a subsystem and returns a report; the main agent edits. |
| MCP server | `mcp/codebase_search.py` | AST-based structured search — `where_is`, `find_references`, `outline`. Parses the code; never substring-matches. |

The bundled hooks and MCP server resolve paths from `${CLAUDE_PLUGIN_ROOT}` and
`CLAUDE_PROJECT_DIR`, so they work in whatever repo the plugin is installed
into — they are not tied to Helpline. The Stop hook spawns `reflect_claude_md.py`
from its own directory, so both files travel together.

## Install

```bash
# add the marketplace (the parent tooling/ directory), then install
/plugin marketplace add ./tooling
/plugin install helpline-ai-layer@helpline-tooling
```

Repo-specific pieces — the `CLAUDE.md` hierarchy, the `billing-money-rules` and
`api-add-route` skills, the `SessionStart` orientation hook — intentionally stay
in the repo's own `.claude/`. They describe *this* codebase and don't travel.
