"""Persist last-used CLI arguments per command in .blender-cli-state.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / ".blender-cli-state.json"


def _read_all() -> dict[str, dict[str, Any]]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(command_name: str, kwargs: dict[str, Any]) -> None:
    """Save the arguments for a command invocation."""
    serializable = {}
    for k, v in kwargs.items():
        if isinstance(v, (str, int, float, bool, type(None))):
            serializable[k] = v

    if not serializable:
        return

    state = _read_all()
    state[command_name] = serializable
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)


def load_state(command_name: str) -> dict[str, Any]:
    """Load saved arguments for a command, or return empty dict."""
    return _read_all().get(command_name, {})
