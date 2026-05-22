"""In-memory stand-in for the real Postgres pool. Demo only — no I/O."""

from __future__ import annotations

from typing import Any


class Connection:
    """A toy connection backed by a dict of tables. Mimics a pool handle."""

    def __init__(self) -> None:
        self._tables: dict[str, dict[str, Any]] = {
            "users": {},
            "tickets": {},
            "invoices": {},
        }

    def table(self, name: str) -> dict[str, Any]:
        if name not in self._tables:
            raise KeyError(f"unknown table: {name}")
        return self._tables[name]


_SHARED = Connection()


def get_connection() -> Connection:
    """Return the process-wide connection. Real impl would pull from a pool."""
    return _SHARED
