# services/notifications — outbound email

## Conventions

- **All outbound copy goes through `templates.py`.** Never inline an email
  string in a handler — add a named template and render it. This keeps copy
  reviewable and translatable.
- A missing template or a missing placeholder field raises `NotFoundError` —
  callers should treat that as a bug, not a user error.
- **`outbox()` is an in-memory list.** It persists for the life of the process.
  Tests that assert on sent mail must account for that (clear or count deltas).

## Tests

```bash
uv run pytest services/notifications
```
