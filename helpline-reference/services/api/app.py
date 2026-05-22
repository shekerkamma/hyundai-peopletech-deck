"""Tiny request-routing app. Stands in for FastAPI/Starlette in the demo."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from core.errors import HelplineError

Handler = Callable[[dict[str, Any]], dict[str, Any]]


class App:
    """Maps "METHOD /path" keys to handlers and dispatches requests."""

    def __init__(self) -> None:
        self._routes: dict[str, Handler] = {}

    def route(self, key: str, handler: Handler) -> None:
        self._routes[key] = handler

    def dispatch(self, key: str, request: dict[str, Any]) -> dict[str, Any]:
        handler = self._routes.get(key)
        if handler is None:
            return {"status": 404, "error": "no such route"}
        try:
            return {"status": 200, "data": handler(request)}
        except HelplineError as exc:
            return {"status": exc.status_code, "error": exc.message}
