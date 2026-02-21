"""afterFileEdit hook: run a light Blender CLI canary for geo-node edits."""

import json
import subprocess
import sys
from pathlib import PurePosixPath


def _read_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _extract_file_path(payload: dict) -> str:
    for key in ("file_path", "target_file", "file", "path"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    tool_input = payload.get("toolInput")
    if isinstance(tool_input, dict):
        for key in ("file_path", "target_file", "file", "path"):
            value = tool_input.get(key)
            if isinstance(value, str) and value:
                return value
    return ""


def _is_geo_node_file(file_path: str) -> bool:
    normalized = file_path.replace("\\", "/")
    parts = PurePosixPath(normalized).parts
    if "procedural_human" not in parts:
        return False
    if "geo_node_groups" not in parts:
        return False
    return normalized.endswith(".py")


def main() -> int:
    """Entry point for afterFileEdit hook."""
    payload = _read_payload()
    file_path = _extract_file_path(payload)
    if file_path and _is_geo_node_file(file_path):
        subprocess.Popen(
            [sys.executable, "tools/blender_cli.py", "ping"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    print(json.dumps({"decision": "allow"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
