"""SessionStart hook — dynamic orientation for the deck workspace.

Prints a short orientation block at the start of every Claude Code session.
Claude Code injects this stdout into the session context, so Claude starts
knowing which deliverables have active work and recent direction of travel.

Tested standalone: python .claude/hooks/session_start_context.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_EXCLUDE_DIRS = frozenset({
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
    ".pytest_cache", "graphify-out", "helpline-reference",
})


def _project_root() -> Path:
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(project) if project else Path(__file__).resolve().parents[2]


def _force_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def _working_tree_changes() -> list[str]:
    """Return changed/untracked file paths via git status --porcelain."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if len(line) > 3:
            paths.append(line[3:].strip().replace("\\", "/"))
    return paths


def _categorize_changes(paths: list[str]) -> dict[str, list[str]]:
    """Group changed files into categories relevant to deck building."""
    categories: dict[str, list[str]] = {
        "build-scripts": [],
        "architecture": [],
        "research": [],
        "deliverables": [],
        "other": [],
    }
    for path in paths:
        if path.startswith("second-brain/"):
            categories["research"].append(path)
        elif path.endswith((".drawio",)):
            categories["architecture"].append(path)
        elif path.endswith((".py", ".js", ".sh")) and "build" in path:
            categories["build-scripts"].append(path)
        elif path.endswith((".pptx", ".docx", ".xlsx")):
            categories["deliverables"].append(path)
        elif not path.startswith(("graphify-out/", "node_modules/", "helpline-reference/")):
            categories["other"].append(path)
    return {k: v for k, v in categories.items() if v}


def _recent_commits(limit: int = 5) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "log", f"-{limit}", "--pretty=format:%h %s"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> None:
    _force_utf8()

    try:
        sys.stdin.read()
    except (OSError, ValueError):
        pass

    lines = ["## Hyundai PeopleTech Deck — session orientation", ""]

    changes = _working_tree_changes()
    categories = _categorize_changes(changes)

    if categories:
        lines.append("Active work this session:")
        for category, files in categories.items():
            lines.append(f"- **{category}**: {len(files)} file(s)")
            for f in files[:5]:
                lines.append(f"  - `{f}`")
            if len(files) > 5:
                lines.append(f"  - ... and {len(files) - 5} more")
    else:
        lines.append("Working tree is clean — no pending work.")

    commits = _recent_commits()
    if commits:
        lines.append("")
        lines.append("Recent commits (newest first):")
        lines.extend(f"- {commit}" for commit in commits)

    lines.append("")
    lines.append("Use `CODEBASE_MAP.md` to find where a deliverable lives before exploring.")
    lines.append("REMINDER: Customer-facing materials must NEVER mention internal tools.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
