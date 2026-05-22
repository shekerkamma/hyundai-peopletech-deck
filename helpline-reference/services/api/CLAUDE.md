# services/api — HTTP gateway

The only service exposed to the public internet. Thin layer: validate, call a
repo or another service, shape the response.

## Conventions

- **Every route is registered in `routes.py`.** `build_app()` is the single
  source of truth for the API surface — if a route isn't there, it doesn't
  exist.
- **Handlers raise, they don't return errors.** Raise a `HelplineError`
  subclass (`ValidationError`, `NotFoundError`, …). `App.dispatch` catches it
  and maps `.status_code` to the response. Never hand-build `{"status": 404}`.
- **No business logic here.** Pricing, hashing, indexing belong in their
  services. `api` only orchestrates.

## Tests

```bash
uv run pytest services/api
```
