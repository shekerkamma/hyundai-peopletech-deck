"""Typed repositories. Services never touch the connection directly."""

from __future__ import annotations

from core.errors import NotFoundError
from core.models import Invoice, Ticket, User
from db.connection import Connection


class UserRepo:
    def __init__(self, conn: Connection) -> None:
        self._t = conn.table("users")

    def add(self, user: User) -> User:
        self._t[user.id] = user
        return user

    def get(self, user_id: str) -> User:
        user = self._t.get(user_id)
        if user is None:
            raise NotFoundError(f"user {user_id} not found")
        return user


class TicketRepo:
    def __init__(self, conn: Connection) -> None:
        self._t = conn.table("tickets")

    def add(self, ticket: Ticket) -> Ticket:
        self._t[ticket.id] = ticket
        return ticket

    def get(self, ticket_id: str) -> Ticket:
        ticket = self._t.get(ticket_id)
        if ticket is None:
            raise NotFoundError(f"ticket {ticket_id} not found")
        return ticket

    def for_org(self, org_id: str) -> list[Ticket]:
        return [t for t in self._t.values() if t.org_id == org_id]


class InvoiceRepo:
    def __init__(self, conn: Connection) -> None:
        self._t = conn.table("invoices")

    def add(self, invoice: Invoice) -> Invoice:
        self._t[invoice.id] = invoice
        return invoice

    def unpaid_for_org(self, org_id: str) -> list[Invoice]:
        return [i for i in self._t.values() if i.org_id == org_id and not i.paid]
