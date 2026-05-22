"""Subscription plan logic — seat limits and plan pricing."""

from __future__ import annotations

from core.errors import BillingError
from core.models import Plan, Subscription

_SEAT_LIMITS: dict[Plan, int] = {
    Plan.FREE: 3,
    Plan.TEAM: 25,
    Plan.ENTERPRISE: 1000,
}

_PRICE_PER_SEAT_CENTS: dict[Plan, int] = {
    Plan.FREE: 0,
    Plan.TEAM: 2900,
    Plan.ENTERPRISE: 5000,
}


def create_subscription(org_id: str, plan: Plan, seats: int) -> Subscription:
    limit = _SEAT_LIMITS[plan]
    if seats > limit:
        raise BillingError(f"{plan.value} plan allows at most {limit} seats")
    if seats < 1:
        raise BillingError("a subscription needs at least one seat")
    return Subscription(org_id=org_id, plan=plan, seats=seats)


def monthly_total_cents(sub: Subscription) -> int:
    return _PRICE_PER_SEAT_CENTS[sub.plan] * sub.seats
