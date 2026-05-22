# services/billing — subscriptions + invoicing

## Conventions

- **Money is always integer cents.** Never floats, never dollars. Field names
  end in `_cents` to make this unmissable.
- **Seat limits and per-seat prices live in `subscriptions.py`** (`_SEAT_LIMITS`,
  `_PRICE_PER_SEAT_CENTS`). Change plan economics there, nowhere else.
- **Any money or plan-rule violation raises `BillingError`** (HTTP 402). Don't
  silently clamp seats or skip a charge.
- An inactive subscription cannot be invoiced — `generate_invoice` enforces it.

## Tests

```bash
uv run pytest services/billing
```
