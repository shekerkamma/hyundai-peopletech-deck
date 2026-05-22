# Route checklist — full reference

## Worked example — `GET /tickets/{id}`

```python
# services/api/tickets.py
def get_ticket(request: dict[str, Any]) -> dict[str, Any]:
    ticket_id = request.get("ticket_id")
    if not ticket_id:
        raise ValidationError("ticket_id is required")
    ticket = TicketRepo(get_connection()).get(str(ticket_id))  # raises NotFoundError
    return {"id": ticket.id, "status": ticket.status.value, "subject": ticket.subject}
```

```python
# services/api/routes.py — inside build_app()
app.route("GET /tickets/{id}", get_ticket)
```

## Checklist

- [ ] Handler signature is `(request: dict) -> dict`
- [ ] Inputs validated; bad input raises `ValidationError`
- [ ] Missing rows surface as `NotFoundError` (repos already do this)
- [ ] No pricing/hashing/indexing logic in the handler
- [ ] Route registered in `build_app()`
- [ ] Test added that builds the app and dispatches the route
- [ ] `uv run pytest services/api` passes

## Why errors are raised, not returned

`App.dispatch` wraps every handler call in a `try/except HelplineError` and maps
`.status_code` to the response. A handler that returns `{"status": 404}` by hand
bypasses that and will drift out of sync with the error contract in
`packages/core/errors.py`.
