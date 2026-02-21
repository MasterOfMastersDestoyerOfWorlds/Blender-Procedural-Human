"""Stop hook reminder for compounding validation learnings."""

import json
from datetime import datetime, timezone
from pathlib import Path


OUT_PATH = Path(".cursor/logs/compound-reminders.log")


def main() -> int:
    """Entry point for stop hook."""
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    reminder_parts = [
        "If this session involved non-trivial work:",
        "1. Search .cursor/docs/ai-learnings/ (grep tags/title) for related learnings before writing new ones.",
        "2. Capture or update a learning with YAML frontmatter (title, category, severity, modules, tags).",
        "3. If you discovered a counter-intuitive finding, compound it into docs so future runs avoid the same trap.",
        "4. Keep .cursor/rules/blender-validation.mdc and CLI command docs in sync when workflow changes.",
    ]
    reminder = " ".join(reminder_parts)
    with OUT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"{datetime.now(timezone.utc).isoformat()} stop hook: {reminder}\n")
    print(json.dumps({"decision": "allow", "message": reminder}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
