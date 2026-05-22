"""Error hierarchy shared across services. API maps these to HTTP codes."""

from __future__ import annotations


class HelplineError(Exception):
    """Base for every domain error. Carries an HTTP-friendly status code."""

    status_code: int = 500

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ValidationError(HelplineError):
    status_code = 422


class NotFoundError(HelplineError):
    status_code = 404


class BillingError(HelplineError):
    status_code = 402
