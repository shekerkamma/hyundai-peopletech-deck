# packages/core — shared domain models + errors

**Imported by every service.** Treat this as a public contract — a change here
can break all five services at once.

## Conventions

- **No service-specific logic.** If something only `billing` needs, it belongs
  in `billing`, not here. `core` is models and errors only.
- **Models are plain dataclasses.** No DB access, no I/O, no network — pure
  data. The `db` package handles persistence.
- **Error `status_code` values are the HTTP contract.** `api` maps them
  directly to responses. Changing a code is an API-visible change.
- After any change here, run the **full** suite — `uv run pytest -q` — not a
  scoped one.
