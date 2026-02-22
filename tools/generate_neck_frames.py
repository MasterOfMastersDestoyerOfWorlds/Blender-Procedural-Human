#!/usr/bin/env python3
"""Generate per-frame neck group modules from neck/main.py."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NECK_MAIN = ROOT / "procedural_human" / "geo_node_groups" / "armor" / "neck" / "main.py"
OUT_DIR = ROOT / "procedural_human" / "geo_node_groups" / "armor" / "neck"


def file_base_for_frame(frame_var: str, label: str) -> str:
    if frame_var == "frame":
        if label:
            slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
            if slug:
                return slug
        return "pipes"
    if label:
        slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
        if slug:
            return slug
    return frame_var


def parse_blocks(src_lines: list[str], body_start: int, parent_start: int) -> dict[str, tuple[int, int]]:
    starts: list[tuple[int, str]] = []
    pat = re.compile(r"^    ([A-Za-z_][\w]*) = nodes\.new\(")
    for i in range(body_start, parent_start):
        m = pat.match(src_lines[i])
        if m:
            starts.append((i, m.group(1)))
    blocks: dict[str, tuple[int, int]] = {}
    for idx, (s, var) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else parent_start
        blocks[var] = (s, e)
    return blocks


def main() -> None:
    text = NECK_MAIN.read_text(encoding="utf-8")
    lines = text.splitlines()

    fn_start = next(i for i, ln in enumerate(lines) if ln.startswith("def create_neck_group"))
    parent_start = next(i for i, ln in enumerate(lines) if ln.strip() == "# Parent assignments")
    auto_idx = next(i for i, ln in enumerate(lines) if ln.strip().startswith("auto_layout_nodes(group)"))
    body_start = next(i for i, ln in enumerate(lines) if ln.strip().startswith("# --- Interface ---"))

    block_ranges = parse_blocks(lines, body_start, parent_start)

    label_pat = re.compile(r"^    (frame[\w]*)\.label = \"(.*)\"$")
    labels = {m.group(1): m.group(2) for ln in lines for m in [label_pat.match(ln)] if m}
    frame_vars = sorted(labels.keys(), key=lambda v: (v != "frame", v))

    parent_pat = re.compile(r"^    ([A-Za-z_][\w]*)\.parent = ([A-Za-z_][\w]*)$")
    parent_map: dict[str, str] = {}
    children: dict[str, list[str]] = defaultdict(list)
    for i in range(parent_start + 1, auto_idx):
        m = parent_pat.match(lines[i])
        if not m:
            continue
        child, parent = m.group(1), m.group(2)
        parent_map[child] = parent
        children[parent].append(child)

    link_pat = re.compile(
        r"^    links\.new\(([\w]+)\.outputs\[(\d+)\], ([\w]+)\.inputs\[(\d+)\]\)$"
    )
    all_links: list[tuple[str, int, str, int]] = []
    for ln in lines:
        m = link_pat.match(ln)
        if m:
            all_links.append((m.group(1), int(m.group(2)), m.group(3), int(m.group(4))))

    def descendants(frame: str) -> set[str]:
        out: set[str] = set()
        stack = [frame]
        while stack:
            n = stack.pop()
            out.add(n)
            for c in children.get(n, []):
                if c not in out:
                    stack.append(c)
        return out

    imports = [
        "import bpy",
        "from mathutils import Euler, Vector",
        "from procedural_human.decorators.geo_node_decorator import geo_node_group",
        "from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group",
        "from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group",
        "from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold__decorations_group",
        "from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group",
        "from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group",
        "from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group",
        "from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group",
        "from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group",
        "from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group",
        "from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op",
        "from procedural_human.utils.node_layout import auto_layout_nodes",
        "",
        "",
    ]

    used_bases: set[str] = set()
    for frame_var in frame_vars:
        label = labels.get(frame_var, "")
        file_base = file_base_for_frame(frame_var, label)
        if file_base in used_bases:
            suffix = frame_var.replace("frame_", "f")
            file_base = f"{file_base}_{suffix}"
        used_bases.add(file_base)
        fn_name = f"create_neck_{file_base}_group"
        group_name = f"Neck_{file_base}"
        members = descendants(frame_var)
        member_nodes = sorted([m for m in members if m in block_ranges], key=lambda v: block_ranges[v][0])
        internal_links = [lk for lk in all_links if lk[0] in members and lk[2] in members]
        parent_lines = [
            f"    {c}.parent = {p}"
            for c, p in sorted(parent_map.items())
            if c in members and p in members
        ]

        out_lines: list[str] = []
        out_lines.extend(imports)
        out_lines.append("@geo_node_group")
        out_lines.append(f"def {fn_name}():")
        out_lines.append(f"    group_name = \"{group_name}\"")
        out_lines.append("    group, needs_rebuild = get_or_rebuild_node_group(group_name)")
        out_lines.append("    if not needs_rebuild:")
        out_lines.append("        return group")
        out_lines.append("")
        out_lines.append("    group.interface.new_socket(name=\"Geometry\", in_out=\"OUTPUT\", socket_type=\"NodeSocketGeometry\")")
        out_lines.append("")
        out_lines.append("    nodes = group.nodes")
        out_lines.append("    links = group.links")
        out_lines.append("    group_output = nodes.new(\"NodeGroupOutput\")")
        out_lines.append("    group_output.is_active_output = True")
        out_lines.append("")

        for var in member_nodes:
            s, e = block_ranges[var]
            for ln in lines[s:e]:
                if ln.strip().startswith("links.new("):
                    continue
                out_lines.append(ln)
            out_lines.append("")

        if parent_lines:
            out_lines.append("    # Parent assignments")
            out_lines.extend(parent_lines)
            out_lines.append("")

        if internal_links:
            out_lines.append("    # Internal links")
            for src, so, dst, di in internal_links:
                out_lines.append(f"    links.new({src}.outputs[{so}], {dst}.inputs[{di}])")
            out_lines.append("")

        # Best effort: emit first geometry-producing node if any.
        if member_nodes:
            out_lines.append(f"    links.new({member_nodes[0]}.outputs[0], group_output.inputs[0])")
            out_lines.append("")

        out_lines.append("    auto_layout_nodes(group)")
        out_lines.append("    return group")
        out_lines.append("")

        (OUT_DIR / f"{file_base}.py").write_text("\n".join(out_lines), encoding="utf-8")
        print(f"Wrote {file_base}.py with {len(member_nodes)} nodes")


if __name__ == "__main__":
    main()
