"""Prove the LSP navigation rule is backed by a working capability.

The rule in CLAUDE.md says "navigate by symbol, not by grep." This test shows
that's real: it asks pyright (over LSP) to resolve a symbol to its definition,
confirms the answer is the *correct* file, and contrasts it with a naive grep —
which returns every textual mention, not the definition.

Run via: uv run python tooling/validate/check_lsp_navigation.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# A reference whose definition lives in a *different* file — the case where
# grep is noisy and go-to-definition earns its keep.
PROBE_FILE = ROOT / "services" / "billing" / "invoices.py"
SYMBOL = "monthly_total_cents"
EXPECT_DEF_FILE = "subscriptions.py"


def _frame(message: dict) -> bytes:
    body = json.dumps(message).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def _read_message(stream) -> dict:
    headers: dict[str, str] = {}
    while True:
        raw = stream.readline()
        if not raw:
            raise RuntimeError("language server closed the stream")
        line = raw.decode("utf-8", "replace").strip()
        if not line:
            break
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
    return json.loads(stream.read(int(headers["content-length"])))


def _read_until(stream, want_id: int) -> dict:
    for _ in range(200):
        message = _read_message(stream)
        if message.get("id") == want_id:
            return message
    raise RuntimeError(f"no response with id {want_id}")


def _grep_mentions(symbol: str) -> list[str]:
    hits: list[str] = []
    for directory in ("services", "packages"):
        for path in (ROOT / directory).rglob("*.py"):
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if symbol in line:
                    hits.append(f"{path.relative_to(ROOT).as_posix()}:{number}")
    return hits


def _probe_position(symbol: str) -> tuple[int, int]:
    """Return the 0-indexed (line, char) of a *usage* of `symbol`.

    Skips import lines — go-to-definition is meaningful from a call site, and
    pyright is more reliable resolving a usage than an imported name.
    """
    for index, line in enumerate(PROBE_FILE.read_text(encoding="utf-8").splitlines()):
        stripped = line.lstrip()
        if stripped.startswith(("from ", "import ")):
            continue
        if symbol in line:
            return index, line.index(symbol)
    raise RuntimeError(f"no usage of {symbol} found in {PROBE_FILE}")


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
                        "workspaceFolders": [
                            {"uri": ROOT.as_uri(), "name": "helpline"}
                        ],
                        "capabilities": {"textDocument": {"definition": {}}},
                    },
                }
            )
        )
        proc.stdin.flush()
        _read_until(proc.stdout, 1)
        proc.stdin.write(
            _frame({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        )

        # Open the probe file so pyright analyzes it and its imports.
        uri = PROBE_FILE.as_uri()
        proc.stdin.write(
            _frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "languageId": "python",
                            "version": 1,
                            "text": PROBE_FILE.read_text(encoding="utf-8"),
                        }
                    },
                }
            )
        )
        proc.stdin.flush()

        line, char = _probe_position(SYMBOL)

        # Ask for the definition. Retry while pyright finishes analysis.
        location = None
        for attempt in range(12):
            req_id = 100 + attempt
            proc.stdin.write(
                _frame(
                    {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "method": "textDocument/definition",
                        "params": {
                            "textDocument": {"uri": uri},
                            "position": {"line": line, "character": char},
                        },
                    }
                )
            )
            proc.stdin.flush()
            result = _read_until(proc.stdout, req_id).get("result")
            if isinstance(result, dict):
                result = [result]
            if result:
                location = result[0]
                break
            time.sleep(1)

        grep_hits = _grep_mentions(SYMBOL)

        if not location:
            print(
                f"FAIL: LSP could not resolve a definition for {SYMBOL!r} "
                f"(probed {PROBE_FILE.name} at line {line + 1}, char {char})"
            )
            return 1

        def_uri = location.get("uri", "")
        def_line = location.get("range", {}).get("start", {}).get("line", -1) + 1
        if not def_uri.endswith(EXPECT_DEF_FILE):
            print(f"FAIL: LSP resolved {SYMBOL!r} to {def_uri}, expected {EXPECT_DEF_FILE}")
            return 1

        print(
            f"PASS: LSP go-to-definition resolved '{SYMBOL}' to the real "
            f"definition — {EXPECT_DEF_FILE}:{def_line}"
        )
        print(
            f"  contrast: a plain grep for '{SYMBOL}' returns {len(grep_hits)} "
            f"line matches ({', '.join(grep_hits)})."
        )
        print(
            "  the LSP pinpoints the one definition; grep hands back every "
            "mention and leaves the agent to guess. The rule pays off."
        )
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    sys.exit(main())
