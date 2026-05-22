# Helpline — Codebase Map

A lightweight map of the repo so an agent can find where a feature lives
*before* it starts reading files. Layered: top-level groups first, then the
modules inside each. Keep this current when you add or move a service.

## Top level

| Path | What it is |
|------|------------|
| `services/` | The five runnable services. Each is independently testable. |
| `packages/` | Shared libraries imported by services. Changes here are repo-wide. |
| `tests/` | Cross-service integration tests. Per-service tests live beside the service. |
| `infra/` | Local-dev infrastructure (`docker-compose.yml`: Postgres + Redis). |
| `scripts/` | One-off operational scripts (`seed_data.py`). |

## services/

| Service | Entry points | Responsibility |
|---------|--------------|----------------|
| `api` | `routes.py` (route table), `app.py` (dispatch) | HTTP gateway. Validate → call service/repo → shape response. |
| `auth` | `tokens.py`, `passwords.py` | Session tokens (HMAC) + password hashing (PBKDF2). |
| `billing` | `subscriptions.py`, `invoices.py` | Plans, seat limits, invoice generation. Money in cents. |
| `notifications` | `email.py`, `templates.py` | Outbound email; all copy via named templates. |
| `search` | `indexer.py`, `query.py` | In-memory inverted index over tickets; AND queries. |

## packages/

| Package | Entry points | Responsibility |
|---------|--------------|----------------|
| `core` | `models.py`, `errors.py` | Domain dataclasses + the error hierarchy (HTTP contract). |
| `db` | `connection.py`, `repositories.py` | Connection stub + typed repositories. Services use repos only. |

## Finding a feature

- **A route / endpoint** → `services/api/routes.py`, then the handler module.
- **Pricing or seat rules** → `services/billing/subscriptions.py`.
- **A domain model field** → `packages/core/models.py`.
- **How data is read/written** → `packages/db/repositories.py`.
