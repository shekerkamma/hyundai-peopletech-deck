# packages/db — database layer

**Imported by every service.** Like `core`, a change here is repo-wide.

## Conventions

- **Services use repositories, never the raw `Connection`.** `UserRepo`,
  `TicketRepo`, `InvoiceRepo` are the only sanctioned entry points. A handler
  importing `Connection` directly is a smell.
- **A missing row raises `NotFoundError`** — repos never return `None` for a
  lookup miss. Keep that invariant.
- The connection is a **shared in-memory stub** (`get_connection()` returns one
  instance). The real implementation would pull from a pool; the repo API is
  designed so swapping it changes nothing for callers.
- After any change here, run the **full** suite.
