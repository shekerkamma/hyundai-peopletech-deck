# services/auth — authentication

Token issuance and password hashing. Security-sensitive — review changes here
carefully.

## Conventions

- **Never log a token or a password**, hashed or plain. Not in errors, not in
  debug output.
- **`_SECRET` in `tokens.py` is a demo key.** Real deployments load it from the
  environment — do not commit a real secret here.
- **Password hashing is PBKDF2-SHA256 at `_ITERATIONS`.** Do not lower the
  iteration count. If you raise it, existing stored hashes still verify
  (the iteration count is fixed per-hash — see the format note in the file).
- Token format is `user_id.expiry.signature`. Comparisons use
  `hmac.compare_digest` — keep it constant-time.

## Tests

```bash
uv run pytest services/auth
```
