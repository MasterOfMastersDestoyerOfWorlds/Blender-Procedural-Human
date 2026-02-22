from pathlib import Path
import re


def main() -> None:
    neck_dir = Path("procedural_human/geo_node_groups/armor/neck")
    for path in sorted(neck_dir.glob("*.py")):
        if path.name in {"__init__.py", "main.py"}:
            continue

        stem = path.stem
        text = path.read_text(encoding="utf-8")

        text = re.sub(
            r"def\s+create_neck_[\w]+_group\(",
            f"def create_neck_{stem}_group(",
            text,
            count=1,
        )
        text = re.sub(
            r'group_name = "Neck_[^"]+"',
            f'group_name = "Neck_{stem}"',
            text,
            count=1,
        )

        path.write_text(text, encoding="utf-8")
        print(f"synced {path.name}")


if __name__ == "__main__":
    main()
