# LSP setup — pyright

The article calls out Language Server Protocol integration as the way to give
Claude **symbol-level** precision — "go to definition" and "find all
references" — instead of text-pattern matching that produces thousands of false
grep hits.

## What's wired

- **pyright** is a dev dependency (`pyproject.toml` → `[project.optional-dependencies].dev`).
- The type-check config lives in `pyproject.toml` → `[tool.pyright]`:
  `extraPaths` makes the flat `core.*` / `db.*` / service imports resolve, and
  `venvPath`/`venv` point pyright at `.venv` so installed packages resolve.
- The language server binary is `pyright-langserver` (ships with the `pyright`
  package). Claude Code speaks LSP to it over stdio.
- The **navigation rule** lives in the root `CLAUDE.md` gotchas — *navigate by
  symbol, not by grep*. Installing the server isn't enough; that rule is what
  makes the agent actually reach for go-to-definition over text search.

## Verify it

```bash
uv sync --extra dev
uv run pyright                                          # type-check, expect 0 errors
uv run python tooling/validate/check_lsp.py             # real LSP initialize handshake
uv run python tooling/validate/check_lsp_navigation.py  # real go-to-definition + grep contrast
```

- `check_lsp.py` spawns `pyright-langserver --stdio`, sends an `initialize`
  request with proper `Content-Length` framing, and confirms the server
  returns its capabilities — proof the LSP path works end to end.
- `check_lsp_navigation.py` goes further: it asks pyright to resolve a real
  symbol to its definition via `textDocument/definition` and confirms the
  answer is the *correct* file — then contrasts it with a plain grep, which
  returns every textual mention. This is the proof the navigation rule
  actually helps, not just that the server is installed.
