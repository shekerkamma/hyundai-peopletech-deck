"""Cross-service tests for the billing service."""

import pytest

from billing.invoices import generate_invoice, mark_paid
from billing.subscriptions import create_subscription, monthly_total_cents
from core.errors import BillingError
from core.models import Plan


def test_team_plan_pricing() -> None:
    sub = create_subscription("org_1", Plan.TEAM, seats=10)
    assert monthly_total_cents(sub) == 29_000


def test_seat_limit_enforced() -> None:
    with pytest.raises(BillingError):
        create_subscription("org_1", Plan.FREE, seats=99)


def test_invoice_lifecycle() -> None:
    sub = create_subscription("org_1", Plan.ENTERPRISE, seats=100)
    invoice = generate_invoice(sub)
    assert invoice.amount_cents == 500_000
    assert not invoice.paid
    assert mark_paid(invoice).paid
