"""CLI commands for inspecting addon logs."""

from __future__ import annotations

import re
from pathlib import Path

from tools.cli_registry import cli_command

REPO_ROOT = Path(__file__).resolve().parents[2]
ADDON_LOG = REPO_ROOT / ".cursor" / "logs" / "addon.log"

_ERROR_WARN_RE = re.compile(r"\b(ERROR|WARNING)\b", re.IGNORECASE)


@cli_command
def errors(log_file: str = "", group: str = "", clear: bool = False, tail: int = 50) -> dict:
    """Show ERROR and WARNING lines from the addon log.

    :param log_file: Path to log file (default: .cursor/logs/addon.log).
    :param group: Optional regex filter applied to each matching line.
    :param clear: Truncate the log file before returning (use before a test run).
    :param tail: Maximum number of lines to return.
    """
    path = Path(log_file) if log_file else ADDON_LOG

    if not path.exists():
        return {"ok": False, "error": f"Log file not found: {path}"}

    if clear:
        path.write_text("", encoding="utf-8")
        return {"ok": True, "lines": [], "total_matches": 0, "cleared": True}

    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    group_re = re.compile(group, re.IGNORECASE) if group else None

    matches = []
    for line in lines:
        if not _ERROR_WARN_RE.search(line):
            continue
        if group_re and not group_re.search(line):
            continue
        matches.append(line)

    total = len(matches)
    trimmed = matches[-tail:]

    return {
        "ok": True,
        "lines": trimmed,
        "total_matches": total,
        "cleared": False,
    }
