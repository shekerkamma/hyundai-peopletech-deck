"""Query layer over the ticket index. Supports multi-word AND queries."""

from __future__ import annotations

from search.indexer import TicketIndex


def search(index: TicketIndex, query: str) -> list[str]:
    """Return ticket ids matching every word in the query (AND semantics)."""
    tokens = [w.lower() for w in query.split() if w]
    if not tokens:
        return []
    matches = index.lookup(tokens[0])
    for token in tokens[1:]:
        matches &= index.lookup(token)
    return sorted(matches)
