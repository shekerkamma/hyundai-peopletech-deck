# Helpline AI Layer — Validation Report

_Generated 2026-05-20T07:48:49 by `tooling/validate/validate_all.py`._

**13/13 checks passed.**

| Check | Result | Detail |
|-------|--------|--------|
| App — test suite | ✅ PASS | pytest: 9 passed in 0.18s |
| App — type check | ✅ PASS | pyright: 0 errors, 0 warnings, 0 informations |
| App — runtime smoke | ✅ PASS | app smoke: seeded 1 user, 2 tickets |
| CLAUDE.md hierarchy | ✅ PASS | 8 CLAUDE.md files present |
| Hook — SessionStart | ✅ PASS | SessionStart hook ran and emitted orientation context |
| Hook — Stop (self-improving) | ✅ PASS | trigger + reflector compile, recursion guard holds, end-to-end reflection wrote claude-md-review.md (LLM reflection) |
| Skills (path-scoped) | ✅ PASS | 3 skills valid (frontmatter + paths-scoped + progressive disclosure) |
| Subagent (explorer) | ✅ PASS | explorer subagent is genuinely read-only (tools: ['Glob', 'Grep', 'Read']) |
| LSP (pyright handshake) | ✅ PASS | PASS: pyright language server initialized (16 capabilities) |
| LSP navigation (go-to-definition) | ✅ PASS | PASS: LSP go-to-definition resolved 'monthly_total_cents' to the real definition — subscriptions.py:30 |
| MCP server (handshake + calls) | ✅ PASS | PASS: MCP server 'helpline-codebase-search' — handshake ok, tools ['where_is', 'find_references', 'outline']; where_is + find_references + outline returned real AST results |
| Plugin (bundle + marketplace) | ✅ PASS | plugin: 8 bundled files present, all JSON valid |
| .claudeignore + settings.json | ✅ PASS | .claudeignore present, settings.json valid (incl. hooks block) |

Re-run any time with `uv run --extra dev python tooling/validate/validate_all.py`.
