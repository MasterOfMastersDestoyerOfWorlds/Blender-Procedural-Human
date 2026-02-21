"""Guard dangerous shell commands from Cursor hooks."""

import json
import re
import sys


DANGEROUS_PATTERNS = [
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+checkout\s+--\b",
    r"\brm\s+-rf\b",
    r"\bdel\s+/f\s+/q\b",
    r"\btaskkill\b",
    r"\bformat\s+[a-z]:\b",
    r"\bgit\s+push\s+--force\b",
]


def _read_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _extract_command(payload: dict) -> str:
    candidates = [
        payload.get("command"),
        payload.get("toolInput", {}).get("command") if isinstance(payload.get("toolInput"), dict) else None,
        payload.get("input", {}).get("command") if isinstance(payload.get("input"), dict) else None,
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate
    return ""


def main() -> int:
    """Entry point for preToolUse hook."""
    payload = _read_payload()
    command = _extract_command(payload)
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(
                json.dumps(
                    {
                        "decision": "deny",
                        "reason": f"Blocked dangerous shell command pattern: {pattern}",
                    }
                )
            )
            return 2
    print(json.dumps({"decision": "allow"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
