"""Validate the codebase-search MCP server with a real MCP stdio handshake.

Spawns the server exactly as `.mcp.json` would, completes the MCP handshake,
lists tools, and actually calls all three — proving the server does real
AST-based structured search end to end, not just that the file imports.

Run via: uv run --extra dev python tooling/validate/check_mcp.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class McpClient:
    def __init__(self) -> None:
        self.proc = subprocess.Popen(
            ["uv", "run", "--extra", "dev", "python", "tooling/mcp/codebase_search.py"],
            cwd=ROOT,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )

    def send(self, message: dict) -> None:
        assert self.proc.stdin
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()

    def recv(self, want_id: int) -> dict:
        assert self.proc.stdout
        for _ in range(100):
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("MCP server closed the stream")
            message = json.loads(line)
            if message.get("id") == want_id:
                return message
        raise RuntimeError(f"no response with id {want_id}")

    def call(self, call_id: int, tool: str, arguments: dict) -> str:
        self.send(
            {
                "jsonrpc": "2.0",
                "id": call_id,
                "method": "tools/call",
                "params": {"name": tool, "arguments": arguments},
            }
        )
        return self.recv(call_id)["result"]["content"][0]["text"]

    def close(self) -> None:
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def main() -> int:
    client = McpClient()
    try:
        client.send(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "helpline-validate", "version": "1.0"},
                },
            }
        )
        init = client.recv(1)
        server_name = init.get("result", {}).get("serverInfo", {}).get("name", "?")
        client.send({"jsonrpc": "2.0", "method": "notifications/initialized"})

        client.send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = [t["name"] for t in client.recv(2)["result"]["tools"]]
        expected = {"where_is", "find_references", "outline"}
        if not expected.issubset(tools):
            print(f"FAIL: expected structured tools {sorted(expected)} — got {tools}")
            return 1

        # where_is — AST definition lookup, must report the *kind*.
        where_text = client.call(3, "where_is", {"name": "create_subscription"})
        if "subscriptions.py" not in where_text or "[function]" not in where_text:
            print(f"FAIL: where_is did not structurally locate create_subscription — {where_text!r}")
            return 1

        # find_references — AST reference lookup, must find the real call site.
        refs_text = client.call(4, "find_references", {"name": "monthly_total_cents"})
        if "invoices.py" not in refs_text or "[call]" not in refs_text:
            print(f"FAIL: find_references did not find the call site — {refs_text!r}")
            return 1

        # outline — structured module API.
        outline_text = client.call(5, "outline", {"module": "subscriptions"})
        if "create_subscription" not in outline_text or "monthly_total_cents" not in outline_text:
            print(f"FAIL: outline did not return the module API — {outline_text!r}")
            return 1

        print(
            f"PASS: MCP server '{server_name}' — handshake ok, tools {tools}; "
            f"where_is + find_references + outline returned real AST results"
        )
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
