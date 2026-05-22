"""Cross-service tests for the auth service."""

import pytest

from auth.passwords import hash_password, verify_password
from auth.tokens import issue_token, verify_token
from core.errors import ValidationError


def test_password_roundtrip() -> None:
    stored = hash_password("correct horse battery staple")
    assert verify_password("correct horse battery staple", stored)
    assert not verify_password("wrong password", stored)


def test_token_roundtrip() -> None:
    token = issue_token("usr_123")
    assert verify_token(token) == "usr_123"


def test_tampered_token_rejected() -> None:
    token = issue_token("usr_123")
    tampered = token[:-1] + ("0" if token[-1] != "0" else "1")
    with pytest.raises(ValidationError):
        verify_token(tampered)
