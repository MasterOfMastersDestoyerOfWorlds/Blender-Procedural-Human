import os
import traceback
from typing import Any, Dict

import bpy

from procedural_human.testing.handlers.geometry import handle_apply_node_group


def handle_diff_group(params: Dict[str, Any]) -> Dict[str, Any]:
    """Compare mesh metrics of a node group against a baseline.

    Applies the node group, captures metrics, then optionally compares
    against a previously saved baseline file.
    """
    group_name = params.get("group", "")
    if not group_name:
        return {"success": False, "error": "No group name provided"}

    ng = bpy.data.node_groups.get(group_name)
    if ng is None:
        return {"success": False, "error": f"Node group '{group_name}' not found"}

    try:
        result = handle_apply_node_group({"group_name": group_name})
        if not result.get("success"):
            return result

        obj = bpy.data.objects.get(result.get("object_name", ""))
        if obj is None or obj.type != "MESH":
            return {"success": False, "error": "No mesh object after applying group"}

        mesh = obj.data
        current = {
            "vertices": len(mesh.vertices),
            "edges": len(mesh.edges),
            "faces": len(mesh.polygons),
        }

        baseline_path = params.get("baseline", "")
        if baseline_path:
            import json as _json
            from pathlib import Path
            bp = Path(baseline_path)
            if bp.exists():
                baseline = _json.loads(bp.read_text())
                diff = {}
                for key in current:
                    if current[key] != baseline.get(key):
                        diff[key] = {"current": current[key], "baseline": baseline.get(key)}
                return {
                    "success": True,
                    "group": group_name,
                    "current": current,
                    "baseline": baseline,
                    "diff": diff,
                    "identical": len(diff) == 0,
                }

        save_path = params.get("save", "")
        if save_path:
            import json as _json
            from pathlib import Path
            Path(save_path).write_text(_json.dumps(current, indent=2))

        return {"success": True, "group": group_name, "metrics": current}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}


def handle_export_group(params: Dict[str, Any]) -> Dict[str, Any]:
    """Export a node group to Python using the node exporter."""
    group_name = params.get("group", "")
    if not group_name:
        return {"success": False, "error": "No group name provided"}

    ng = bpy.data.node_groups.get(group_name)
    if ng is None:
        return {"success": False, "error": f"Node group '{group_name}' not found"}

    try:
        from procedural_human.utils.node_exporter.exporter import NodeGroupExporter, ExportOptions
        from procedural_human.utils.node_exporter.utils import (
            clean_string, to_snake_case, get_next_temp_file_path, get_tmp_base_dir,
        )

        options = ExportOptions(
            include_locations=params.get("include_locations", False),
            include_labels=params.get("include_labels", True),
            include_names=params.get("include_names", False),
            use_helpers=params.get("use_helpers", True),
            split_frames=params.get("split_frames", False),
        )

        exporter = NodeGroupExporter(options)
        exporter.process_group(ng)

        base_dir = get_tmp_base_dir()
        written_files = []

        if options.split_frames:
            group_dir_name = to_snake_case(clean_string(ng.name))
            group_dir = base_dir / group_dir_name
            group_dir.mkdir(parents=True, exist_ok=True)
            init_path = group_dir / "__init__.py"
            if not init_path.exists():
                init_path.touch()
            files = exporter.get_files(package_name=group_dir_name)
            for filepath, code in files.items():
                file_path = group_dir / filepath.replace("/", os.sep)
                file_path.parent.mkdir(parents=True, exist_ok=True)
                sub_init = file_path.parent / "__init__.py"
                if not sub_init.exists():
                    sub_init.touch()
                with open(file_path, "w") as f:
                    f.write(code)
                written_files.append(str(file_path))
        else:
            code = exporter.get_full_code()
            file_path = get_next_temp_file_path(str(base_dir))
            with open(file_path, "w") as f:
                f.write(code)
            written_files.append(file_path)

        return {
            "success": True,
            "group": group_name,
            "files": written_files,
            "helpers_used": sorted(exporter.used_helpers),
            "known_groups_detected": [f for _, f in exporter.used_group_imports],
        }
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}


def handle_inspect_group(params: Dict[str, Any]) -> Dict[str, Any]:
    """Inspect a node group's structure: nodes, links, interface, frames."""
    group_name = params.get("group", "")
    if not group_name:
        return {"success": False, "error": "No group name provided"}

    ng = bpy.data.node_groups.get(group_name)
    if ng is None:
        try:
            from procedural_human.decorators.geo_node_decorator import geo_node_group
            func = geo_node_group.registry.get(f"create_{group_name.lower().replace(' ', '_')}_group")
            if func is None:
                for name, f in geo_node_group.registry.items():
                    if group_name.lower() in name.lower():
                        func = f
                        break
            if func:
                func()
                ng = bpy.data.node_groups.get(group_name)
        except Exception:
            pass

    if ng is None:
        available = sorted(bpy.data.node_groups.keys())
        return {"success": False, "error": f"Node group '{group_name}' not found", "available": available[:20]}

    try:
        node_types = {}
        frames = []
        for node in ng.nodes:
            t = node.bl_idname
            node_types[t] = node_types.get(t, 0) + 1
            if t == "NodeFrame":
                label = node.label or node.name
                parent = node.parent.label if node.parent else None
                frames.append({"name": node.name, "label": label, "parent": parent})

        inputs = []
        outputs = []
        for item in ng.interface.items_tree:
            if item.item_type == "PANEL":
                continue
            entry = {"name": item.name, "type": item.socket_type, "io": item.in_out}
            if item.in_out == "INPUT":
                inputs.append(entry)
            else:
                outputs.append(entry)

        return {
            "success": True,
            "name": ng.name,
            "node_count": len(ng.nodes),
            "link_count": len(ng.links),
            "node_types": node_types,
            "frames": frames,
            "inputs": inputs,
            "outputs": outputs,
        }
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}


def handle_list_groups(params: Dict[str, Any]) -> Dict[str, Any]:
    """List all registered geo_node_group functions."""
    try:
        from procedural_human.decorators.geo_node_decorator import geo_node_group
        groups = {}
        for name, func in sorted(geo_node_group.registry.items()):
            module = getattr(func, '__module__', 'unknown')
            groups[name] = {"module": module}

        blender_groups = sorted(bpy.data.node_groups.keys())
        return {
            "success": True,
            "registered": groups,
            "registered_count": len(groups),
            "blender_groups": blender_groups,
            "blender_count": len(blender_groups),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}
