# Money conventions — full reference

The third progressive-disclosure layer for `billing-money-rules`. Loaded only
when a billing change is non-trivial.

## Why integer cents

Floating-point dollars accumulate rounding error. `0.1 + 0.2 != 0.3`. At scale,
a tenth of a cent per invoice becomes a real reconciliation problem. Integer
cents are exact. The `_cents` suffix is a naming contract — if you see a money
value without it, treat that as a bug.

## Worked example — adding a plan

To add a `STARTER` plan at $9/seat, 10 seats max:

1. Add `STARTER = "starter"` to `core.models.Plan`.
2. Add `Plan.STARTER: 10` to `_SEAT_LIMITS` in `subscriptions.py`.
3. Add `Plan.STARTER: 900` to `_PRICE_PER_SEAT_CENTS` (900 = $9.00).
4. Nothing else changes — `create_subscription`, `monthly_total_cents`, and
   `generate_invoice` all read from those two dicts.

## Edge cases

- **Zero seats** → `BillingError` ("at least one seat"). Never allow a 0-seat
  subscription.
- **Downgrade below current usage** is a product decision, not a billing one —
  raise `BillingError` and let the caller handle it.
- **Proration** is not implemented. If asked to add it, flag that it needs a
  design decision; do not improvise partial-month math.
