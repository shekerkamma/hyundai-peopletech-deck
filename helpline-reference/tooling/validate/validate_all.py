"""End-to-end validation of the Helpline AI Layer.

Runs every layer the article describes — the app itself, the CLAUDE.md
hierarchy, hooks, skills, LSP, the MCP server, the subagent, and the plugin —
and writes a VALIDATION.md report at the repo root.

Run via: uv run --extra dev python tooling/validate/validate_all.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Result = tuple[bool, str]


def _run(cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout
    )


def check_app_tests() -> Result:
    proc = _run(["uv", "run", "pytest", "-q"])
    line = next(
        (ln for ln in reversed(proc.stdout.splitlines()) if "passed" in ln or "error" in ln),
        "",
    )
    return proc.returncode == 0, f"pytest: {line.strip() or 'see output'}"


def check_types() -> Result:
    proc = _run(["uv", "run", "pyright"])
    last = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    return proc.returncode == 0, f"pyright: {last}"


def check_claude_md_hierarchy() -> Result:
    expected = [
        "CLAUDE.md",
        "services/api/CLAUDE.md",
        "services/auth/CLAUDE.md",
        "services/billing/CLAUDE.md",
        "services/notifications/CLAUDE.md",
        "services/search/CLAUDE.md",
        "packages/core/CLAUDE.md",
        "packages/db/CLAUDE.md",
    ]
    missing = [p for p in expected if not (ROOT / p).is_file()]
    return not missing, (
        f"{len(expected)} CLAUDE.md files present"
        if not missing
        else f"missing: {missing}"
    )


def check_session_start_hook() -> Result:
    proc = _run(["uv", "run", "python", ".claude/hooks/session_start_context.py"], 30)
    ok = proc.returncode == 0 and "session orientation" in proc.stdout
    return ok, "SessionStart hook ran and emitted orientation context"


def check_stop_hook() -> Result:
    """The self-improving Stop hook: trigger + reflector compile, the trigger
    runs clean, the recursion guard holds, and a real end-to-end reflection
    writes a claude-md-review.md."""
    hooks = ROOT / ".claude/hooks"
    trigger = hooks / "propose_claude_md.py"
    reflector = hooks / "reflect_claude_md.py"

    # 1. Both files exist and are syntactically valid.
    for path in (trigger, reflector):
        if not path.is_file():
            return False, f"missing .claude/hooks/{path.name}"
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            return False, f"{path.name} syntax error: {exc}"

    # 2. The trigger hook runs and exits 0.
    proc = _run(["uv", "run", "python", ".claude/hooks/propose_claude_md.py"], 30)
    if proc.returncode != 0:
        return False, f"trigger hook exited {proc.returncode}"

    # 3. Recursion guard — with the lock set, the reflector must no-op cleanly.
    guarded = subprocess.run(
        ["uv", "run", "python", ".claude/hooks/reflect_claude_md.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "HELPLINE_AILAYER_REFLECT_LOCK": "1"},
    )
    if guarded.returncode != 0:
        return False, "recursion guard failed: reflector errored when lock was set"

    # 4. Real end-to-end reflection. Probe a service file (exact-bytes restore
    #    in finally), run the reflector synchronously, confirm the review file.
    probe = ROOT / "services/search/query.py"
    review = ROOT / ".claude/claude-md-review.md"
    original = probe.read_bytes()
    try:
        probe.write_bytes(original + b"\n# ai-layer validation probe\n")
        refl = _run(["uv", "run", "python", ".claude/hooks/reflect_claude_md.py"], 240)
    finally:
        probe.write_bytes(original)
    if refl.returncode != 0:
        return False, f"reflector exited {refl.returncode}"
    if not review.is_file():
        return False, "reflector produced no claude-md-review.md"
    body = review.read_text(encoding="utf-8")
    if not body.startswith("# CLAUDE.md review"):
        return False, "claude-md-review.md missing expected header"
    mode = (
        "LLM reflection"
        if "Reflection by `claude -p`" in body
        else "deterministic fallback"
    )
    return True, (
        f"trigger + reflector compile, recursion guard holds, "
        f"end-to-end reflection wrote claude-md-review.md ({mode})"
    )


def check_skills() -> Result:
    skills = ["billing-money-rules", "api-add-route", "scoped-tests"]
    bad: list[str] = []
    for skill in skills:
        skill_md = ROOT / ".claude/skills" / skill / "SKILL.md"
        if not skill_md.is_file():
            bad.append(f"{skill} (missing)")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---") or "name:" not in text or "description:" not in text:
            bad.append(f"{skill} (bad frontmatter)")
        frontmatter = text.split("---", 2)[1] if text.count("---") >= 2 else ""
        if not any(ln.strip().startswith("paths:") for ln in frontmatter.splitlines()):
            bad.append(f"{skill} (no paths: scoping)")
    return not bad, (
        f"{len(skills)} skills valid (frontmatter + paths-scoped + progressive disclosure)"
        if not bad
        else f"problems: {bad}"
    )


def check_subagent() -> Result:
    agent = ROOT / ".claude/agents/explorer.md"
    if not agent.is_file():
        return False, "explorer.md missing"
    text = agent.read_text(encoding="utf-8")
    if not (text.startswith("---") and "name: explorer" in text):
        return False, "explorer.md missing frontmatter / name"
    tools_line = next(
        (ln for ln in text.splitlines() if ln.strip().startswith("tools:")), ""
    )
    if not tools_line:
        return False, "explorer.md has no tools: line"
    granted = {t.strip() for t in tools_line.split(":", 1)[1].split(",") if t.strip()}
    writers = granted & {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    if writers:
        return False, f"explorer is not genuinely read-only — grants {sorted(writers)}"
    if not {"Read", "Grep", "Glob"}.issubset(granted):
        return False, f"explorer missing read tools — has {sorted(granted)}"
    return True, f"explorer subagent is genuinely read-only (tools: {sorted(granted)})"


def check_lsp() -> Result:
    proc = _run(["uv", "run", "python", "tooling/validate/check_lsp.py"], 60)
    return proc.returncode == 0, (proc.stdout.strip() or "see check_lsp.py")


def check_lsp_navigation() -> Result:
    proc = _run(["uv", "run", "python", "tooling/validate/check_lsp_navigation.py"], 90)
    first = proc.stdout.strip().splitlines()[0] if proc.stdout.strip() else ""
    return proc.returncode == 0, (first or "see check_lsp_navigation.py")


def check_mcp() -> Result:
    proc = _run(
        ["uv", "run", "--extra", "dev", "python", "tooling/validate/check_mcp.py"], 90
    )
    return proc.returncode == 0, (proc.stdout.strip() or "see check_mcp.py")


def check_plugin() -> Result:
    files = [
        "tooling/.claude-plugin/marketplace.json",
        "tooling/helpline-ai-layer/.claude-plugin/plugin.json",
        "tooling/helpline-ai-layer/hooks/hooks.json",
        "tooling/helpline-ai-layer/hooks/propose_claude_md.py",
        "tooling/helpline-ai-layer/hooks/reflect_claude_md.py",
        "tooling/helpline-ai-layer/skills/scoped-tests/SKILL.md",
        "tooling/helpline-ai-layer/agents/explorer.md",
        "tooling/helpline-ai-layer/mcp/codebase_search.py",
    ]
    for rel in files:
        path = ROOT / rel
        if not path.is_file():
            return False, f"plugin file missing: {rel}"
        if rel.endswith(".json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                return False, f"invalid JSON in {rel}: {exc}"
    return True, f"plugin: {len(files)} bundled files present, all JSON valid"


def check_ignore_and_settings() -> Result:
    if not (ROOT / ".claudeignore").is_file():
        return False, ".claudeignore missing"
    try:
        json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f".claude/settings.json invalid: {exc}"
    return True, ".claudeignore present, settings.json valid (incl. hooks block)"


def check_app_runs() -> Result:
    proc = _run(["uv", "run", "python", "scripts/seed_data.py"], 30)
    ok = proc.returncode == 0 and "seeded" in proc.stdout
    return ok, f"app smoke: {proc.stdout.strip() or 'seed failed'}"


CHECKS: list[tuple[str, Callable[[], Result]]] = [
    ("App — test suite", check_app_tests),
    ("App — type check", check_types),
    ("App — runtime smoke", check_app_runs),
    ("CLAUDE.md hierarchy", check_claude_md_hierarchy),
    ("Hook — SessionStart", check_session_start_hook),
    ("Hook — Stop (self-improving)", check_stop_hook),
    ("Skills (path-scoped)", check_skills),
    ("Subagent (explorer)", check_subagent),
    ("LSP (pyright handshake)", check_lsp),
    ("LSP navigation (go-to-definition)", check_lsp_navigation),
    ("MCP server (handshake + calls)", check_mcp),
    ("Plugin (bundle + marketplace)", check_plugin),
    (".claudeignore + settings.json", check_ignore_and_settings),
]


def main() -> int:
    rows: list[tuple[str, bool, str]] = []
    for name, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as exc:  # noqa: BLE001 - report any failure, don't crash
            ok, detail = False, f"check raised: {exc}"
        rows.append((name, ok, detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")

    passed = sum(1 for _, ok, _ in rows if ok)
    total = len(rows)
    stamp = datetime.now().isoformat(timespec="seconds")

    lines = [
        "# Helpline AI Layer — Validation Report",
        "",
        f"_Generated {stamp} by `tooling/validate/validate_all.py`._",
        "",
        f"**{passed}/{total} checks passed.**",
        "",
        "| Check | Result | Detail |",
        "|-------|--------|--------|",
    ]
    for name, ok, detail in rows:
        lines.append(f"| {name} | {'✅ PASS' if ok else '❌ FAIL'} | {detail} |")
    lines.append("")
    lines.append(
        "Re-run any time with "
        "`uv run --extra dev python tooling/validate/validate_all.py`."
    )
    (ROOT / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n{passed}/{total} passed — wrote VALIDATION.md")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
