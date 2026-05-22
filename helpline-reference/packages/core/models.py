"""Core domain models. Every service imports from here — change with care."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


def _now() -> datetime:
    return datetime.now(timezone.utc)


class TicketStatus(str, Enum):
    OPEN = "open"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Plan(str, Enum):
    FREE = "free"
    TEAM = "team"
    ENTERPRISE = "enterprise"


@dataclass
class User:
    id: str
    email: str
    org_id: str
    is_agent: bool = False
    created_at: datetime = field(default_factory=_now)


@dataclass
class Ticket:
    id: str
    org_id: str
    subject: str
    body: str
    status: TicketStatus = TicketStatus.OPEN
    assignee_id: str | None = None
    created_at: datetime = field(default_factory=_now)

    def is_active(self) -> bool:
        return self.status in (TicketStatus.OPEN, TicketStatus.PENDING)


@dataclass
class Subscription:
    org_id: str
    plan: Plan
    seats: int
    active: bool = True


@dataclass
class Invoice:
    id: str
    org_id: str
    amount_cents: int
    paid: bool = False
    created_at: datetime = field(default_factory=_now)
