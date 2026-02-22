from pathlib import Path
import re


def label_slug(label: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    return slug


def main() -> None:
    neck_dir = Path("procedural_human/geo_node_groups/armor/neck")
    files = sorted([p for p in neck_dir.glob("frame_*.py") if p.name != "frame_pipes.py"])

    used: set[str] = set()
    renames: list[tuple[Path, Path]] = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        label = ""
        for line in text.splitlines():
            if '.label = "' in line and "frame" in line:
                label = line.split('.label = "', 1)[1].rsplit('"', 1)[0].strip()
                break

        base = label_slug(label) if label else path.stem
        if not base:
            base = path.stem
        if base in used:
            match = re.search(r"frame_(\d+)", path.stem)
            suffix = f"f{match.group(1)}" if match else path.stem
            base = f"{base}_{suffix}"
        used.add(base)
        renames.append((path, neck_dir / f"{base}.py"))

    # Add decorator support to all frame files.
    for old, _ in renames:
        text = old.read_text(encoding="utf-8")
        if "from procedural_human.decorators.geo_node_decorator import geo_node_group" not in text:
            text = text.replace(
                "import bpy\n",
                "import bpy\nfrom procedural_human.decorators.geo_node_decorator import geo_node_group\n",
                1,
            )
        if "@geo_node_group\n" not in text:
            text = re.sub(
                r"\ndef\s+(create_neck_[\w]+_group\()",
                r"\n@geo_node_group\ndef \1",
                text,
                count=1,
            )
        old.write_text(text, encoding="utf-8")

    # Rename files.
    for old, new in renames:
        target = new
        if old == target:
            continue
        if target.exists():
            target = target.with_name(f"{target.stem}_{old.stem}.py")
        old.rename(target)
        print(f"{old.name} -> {target.name}")


if __name__ == "__main__":
    main()
