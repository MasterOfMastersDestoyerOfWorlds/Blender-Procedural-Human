from datetime import datetime
import json
import os
import tempfile
from typing import Any
from procedural_human.logger import *


def export_debug_info(
    node_group: Any,
    instance_name: str,
    source_file: str,
) -> None:
    """Export node group structure to temp folder in repo for debugging."""
    debug_data = {
        "instance_name": instance_name,
        "source_file": source_file,
        "timestamp": datetime.now().isoformat(),
        "node_group_name": node_group.name,
        "nodes": [],
        "links": [],
    }

    for node in node_group.nodes:
        node_data = {
            "name": node.name,
            "label": node.label,
            "type": node.bl_idname,
            "location": list(node.location),
        }

        if hasattr(node, "inputs"):
            node_data["inputs"] = [
                {"name": inp.name, "type": inp.bl_idname} for inp in node.inputs
            ]

        if hasattr(node, "outputs"):
            node_data["outputs"] = [
                {"name": out.name, "type": out.bl_idname} for out in node.outputs
            ]

        if hasattr(node, "node_tree") and node.node_tree:
            node_data["node_tree"] = node.node_tree.name

        if node.parent:
            node_data["parent"] = node.parent.name

        debug_data["nodes"].append(node_data)

    for link in node_group.links:
        link_data = {
            "from_node": link.from_node.name,
            "from_socket": link.from_socket.name,
            "to_node": link.to_node.name,
            "to_socket": link.to_socket.name,
        }
        debug_data["links"].append(link_data)

    if source_file and os.path.exists(source_file):
        source_dir = os.path.dirname(source_file)
        while source_dir:
            if os.path.exists(os.path.join(source_dir, ".git")):
                debug_folder = os.path.join(source_dir, ".temp", "debug")
            if os.path.exists(os.path.join(source_dir, "procedural_human")):
                debug_folder = os.path.join(source_dir, ".temp", "debug")
            parent = os.path.dirname(source_dir)
            if parent == source_dir:
                break
            source_dir = parent
    if not debug_folder:
        debug_folder = os.path.join(tempfile.gettempdir(), "procedural_human_debug")
    os.makedirs(debug_folder, exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in instance_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_file = os.path.join(debug_folder, f"{safe_name}_{timestamp}.json")

    with open(debug_file, "w") as f:
        json.dump(debug_data, f, indent=2)

    logger.info(f"[DSL Debug] Exported node structure to: {debug_file}")
