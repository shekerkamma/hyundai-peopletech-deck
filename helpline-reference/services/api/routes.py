"""Wires every route handler onto the App. This is the API surface map."""

from __future__ import annotations

from api.app import App
from api.tickets import create_ticket, list_tickets


def build_app() -> App:
    app = App()
    app.route("POST /tickets", create_ticket)
    app.route("GET /tickets", list_tickets)
    return app
