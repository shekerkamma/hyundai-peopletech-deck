"""Named message templates with simple ``{placeholder}`` substitution."""

from __future__ import annotations

from core.errors import NotFoundError

_TEMPLATES: dict[str, str] = {
    "ticket_opened": "Hi {name}, ticket {ticket_id} is now open.",
    "ticket_resolved": "Hi {name}, ticket {ticket_id} has been resolved.",
    "invoice_due": "Hi {name}, invoice {invoice_id} for ${amount} is due.",
}


def render(template_name: str, **fields: str) -> str:
    template = _TEMPLATES.get(template_name)
    if template is None:
        raise NotFoundError(f"no template named {template_name}")
    try:
        return template.format(**fields)
    except KeyError as exc:
        raise NotFoundError(f"template {template_name} missing field {exc}") from exc
