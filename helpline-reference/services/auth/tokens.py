"""Session token issue + verify. HMAC-signed; demo secret, not production."""

from __future__ import annotations

import hashlib
import hmac
import time

from core.errors import ValidationError

_SECRET = b"demo-signing-key-not-for-production"
_TTL_SECONDS = 3600


def issue_token(user_id: str) -> str:
    """Return a signed token of the form ``user_id.expiry.signature``."""
    expiry = int(time.time()) + _TTL_SECONDS
    payload = f"{user_id}.{expiry}"
    sig = hmac.new(_SECRET, payload.encode(), hashlib.sha256).hexdigest()[:16]
    return f"{payload}.{sig}"


def verify_token(token: str) -> str:
    """Return the user_id if the token is valid and unexpired, else raise."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValidationError("malformed token")
    user_id, expiry_str, sig = parts
    payload = f"{user_id}.{expiry_str}"
    expected = hmac.new(_SECRET, payload.encode(), hashlib.sha256).hexdigest()[:16]
    if not hmac.compare_digest(sig, expected):
        raise ValidationError("bad token signature")
    if int(expiry_str) < int(time.time()):
        raise ValidationError("token expired")
    return user_id
