"""Inverted-index builder for tickets. Token = lowercased word."""

from __future__ import annotations

from collections import defaultdict

from core.models import Ticket


def _tokenize(text: str) -> list[str]:
    return [w.strip(".,!?").lower() for w in text.split() if w.strip(".,!?")]


class TicketIndex:
    """Maps a token to the set of ticket ids whose subject/body contain it."""

    def __init__(self) -> None:
        self._index: dict[str, set[str]] = defaultdict(set)

    def add(self, ticket: Ticket) -> None:
        for token in _tokenize(f"{ticket.subject} {ticket.body}"):
            self._index[token].add(ticket.id)

    def lookup(self, token: str) -> set[str]:
        return set(self._index.get(token.lower(), set()))

    def size(self) -> int:
        return len(self._index)
