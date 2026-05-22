"""Invoice generation from a subscription's monthly total."""

from __future__ import annotations

import uuid

from core.errors import BillingError
from core.models import Invoice, Subscription
from billing.subscriptions import monthly_total_cents


def generate_invoice(sub: Subscription) -> Invoice:
    if not sub.active:
        raise BillingError("cannot invoice an inactive subscription")
    amount = monthly_total_cents(sub)
    return Invoice(
        id=f"inv_{uuid.uuid4().hex[:10]}",
        org_id=sub.org_id,
        amount_cents=amount,
    )


def mark_paid(invoice: Invoice) -> Invoice:
    invoice.paid = True
    return invoice
