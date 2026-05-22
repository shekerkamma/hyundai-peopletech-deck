"""Validate the pyright language server by completing a real LSP handshake.

Spawns `pyright-langserver --stdio`, sends an `initialize` request with proper
Content-Length framing, and confirms the server returns its capabilities.
Run via: uv run python tooling/validate/check_lsp.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _frame(message: dict) -> bytes:
    body = json.dumps(message).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def _read_message(stream) -> dict:
    headers: dict[str, str] = {}
    while True:
        raw = stream.readline()
        if not raw:
            raise RuntimeError("language server closed the stream before replying")
        line = raw.decode("utf-8", "replace").strip()
        if not line:
            break
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
    length = int(headers["content-length"])
    return json.loads(stream.read(length))


def main() -> int:
    proc = subprocess.Popen(
        ["pyright-langserver", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    assert proc.stdin and proc.stdout
    try:
        proc.stdin.write(
            _frame(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "processId": os.getpid(),
                        "rootUri": ROOT.as_uri(),
                        "capabilities": {},
                    },
                }
            )
        )
        proc.stdin.flush()
        # The server may emit log/progress notifications before the actual
        # response — read until we see the reply to request id 1.
        for _ in range(50):
            message = _read_message(proc.stdout)
            if message.get("id") == 1:
                caps = message.get("result", {}).get("capabilities")
                if not caps:
                    print("FAIL: initialize returned no capabilities")
                    return 1
                print(
                    f"PASS: pyright language server initialized "
                    f"({len(caps)} capabilities)"
                )
                return 0
        print("FAIL: no initialize response after 50 messages")
        return 1
    finally:
        try:
            proc.stdin.write(_frame({"jsonrpc": "2.0", "id": 2, "method": "shutdown"}))
            proc.stdin.flush()
        except OSError:
            pass
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    sys.exit(main())
