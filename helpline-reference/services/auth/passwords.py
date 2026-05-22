"""Password hashing. PBKDF2 over SHA-256 with a per-hash random salt."""

from __future__ import annotations

import hashlib
import hmac
import os

_ITERATIONS = 120_000


def hash_password(plaintext: str) -> str:
    """Return ``salt_hex:digest_hex`` for storage."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", plaintext.encode(), salt, _ITERATIONS)
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(plaintext: str, stored: str) -> bool:
    """Check a plaintext password against a stored ``salt:digest`` value."""
    try:
        salt_hex, digest_hex = stored.split(":", 1)
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", plaintext.encode(), salt, _ITERATIONS)
    return hmac.compare_digest(digest.hex(), digest_hex)
