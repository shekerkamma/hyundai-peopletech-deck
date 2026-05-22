"""Outbound email. Demo impl records sends in memory instead of an SMTP call."""

from __future__ import annotations

from dataclasses import dataclass

from notifications.templates import render

_SENT: list["SentEmail"] = []


@dataclass
class SentEmail:
    to: str
    body: str


def send_templated(to: str, template_name: str, **fields: str) -> SentEmail:
    body = render(template_name, **fields)
    email = SentEmail(to=to, body=body)
    _SENT.append(email)
    return email


def outbox() -> list[SentEmail]:
    """Return everything sent this process — used by tests and the demo."""
    return list(_SENT)
