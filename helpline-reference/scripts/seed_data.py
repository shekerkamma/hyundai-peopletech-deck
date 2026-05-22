"""Seed the in-memory store with demo orgs, users, and tickets.

Run directly: `uv run python scripts/seed_data.py`. Scripts live outside the
package dirs, so they bootstrap `packages/` and `services/` onto sys.path —
the same paths pytest and pyright get from pyproject.toml.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for _name in ("packages", "services"):
    _entry = str(_ROOT / _name)
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

from core.models import Ticket, User  # noqa: E402  (after sys.path bootstrap)
from db import TicketRepo, UserRepo, get_connection  # noqa: E402


def seed() -> None:
    conn = get_connection()
    users = UserRepo(conn)
    tickets = TicketRepo(conn)

    users.add(User(id="usr_1", email="agent@acme.test", org_id="org_acme", is_agent=True))
    tickets.add(Ticket(id="tkt_1", org_id="org_acme", subject="Login broken", body="cannot sign in"))
    tickets.add(Ticket(id="tkt_2", org_id="org_acme", subject="Billing question", body="invoice wrong"))
    print("seeded 1 user, 2 tickets")


if __name__ == "__main__":
    seed()
