# services/search — ticket indexing + queries

## Conventions

- **The index is in-memory and per-process** (`TicketIndex`). It is not
  persisted — it's rebuilt from tickets on startup. Don't assume durability.
- **Tokenization is centralized** in `indexer._tokenize` (lowercase, strip
  basic punctuation). If you change it, the index and queries must use the
  *same* function — never tokenize differently on the query side.
- **Multi-word queries are AND**, not OR — see `query.search`. Changing this
  changes the product behavior; flag it.

## Tests

```bash
uv run pytest services/search
```
