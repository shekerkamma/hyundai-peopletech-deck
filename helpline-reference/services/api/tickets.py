"""Ticket endpoints. Thin layer: validate input, call repos, shape response."""

from __future__ import annotations

import uuid
from typing import Any

from core.errors import ValidationError
from core.models import Ticket
from db import TicketRepo, get_connection


def create_ticket(request: dict[str, Any]) -> dict[str, Any]:
    org_id = request.get("org_id")
    subject = request.get("subject")
    if not org_id or not subject:
        raise ValidationError("org_id and subject are required")
    ticket = Ticket(
        id=f"tkt_{uuid.uuid4().hex[:10]}",
        org_id=str(org_id),
        subject=str(subject),
        body=str(request.get("body", "")),
    )
    TicketRepo(get_connection()).add(ticket)
    return {"id": ticket.id, "status": ticket.status.value}


def list_tickets(request: dict[str, Any]) -> dict[str, Any]:
    org_id = request.get("org_id")
    if not org_id:
        raise ValidationError("org_id is required")
    tickets = TicketRepo(get_connection()).for_org(str(org_id))
    return {"tickets": [t.id for t in tickets], "count": len(tickets)}
