"""Geometry-centric Blender CLI commands."""

from __future__ import annotations

from tools.cli_registry import cli_command
from tools.commands.common import BlenderClient, parse_inputs


@cli_command
def apply_node_group(
    client: BlenderClient,
    group: str,
    object_name: str = "NodeGroupTest",
    inputs: str = "{}",
) -> dict:
    """Apply a geometry node group to a generated test object.

    :param client: Blender HTTP client.
    :param group: Name of the geometry node group (e.g. BasaltColumns).
    :param object_name: Name for created object.
    :param inputs: JSON object string with modifier input values.
    """
    parsed_inputs, error = parse_inputs(inputs)
    if error:
        return {"ok": False, "error": error}
    result = client.command(
        "apply_node_group",
        {"group_name": group, "object_name": object_name, "inputs": parsed_inputs},
    )
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def validate_geometry(client: BlenderClient, object_name: str = "") -> dict:
    """Validate evaluated geometry has more than one vertex and at least one face.

    :param client: Blender HTTP client.
    :param object_name: Optional object name (uses active object when omitted).
    """
    params = {"object_name": object_name} if object_name else {}
    result = client.command("validate_geometry", params)
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def mesh_metrics(client: BlenderClient, object_name: str = "") -> dict:
    """Get mesh counts, dimensions, and face side histogram.

    :param client: Blender HTTP client.
    :param object_name: Optional object name (uses active object when omitted).
    """
    params = {"object_name": object_name} if object_name else {}
    result = client.command("get_mesh_metrics", params)
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def check_watertight(client: BlenderClient, object_name: str = "") -> dict:
    """Check whether evaluated mesh is watertight (all edges manifold).

    :param client: Blender HTTP client.
    :param object_name: Optional object name (uses active object when omitted).
    """
    params = {"object_name": object_name} if object_name else {}
    result = client.command("check_watertight", params)
    result["ok"] = bool(result.get("success")) and result.get("is_watertight", False)
    return result


@cli_command
def check_camera_visibility(client: BlenderClient, object_name: str = "") -> dict:
    """Check whether object bounding box is visible in the active camera frame.

    :param client: Blender HTTP client.
    :param object_name: Optional object name (uses active object when omitted).
    """
    params = {"object_name": object_name} if object_name else {}
    result = client.command("check_camera_visibility", params)
    result["ok"] = bool(result.get("success")) and result.get("visible", False)
    return result


@cli_command
def check_degenerate(client: BlenderClient, object_name: str = "") -> dict:
    """Check whether geometry is degenerate (collapsed to a point or line).

    :param client: Blender HTTP client.
    :param object_name: Optional object name (uses active object when omitted).
    """
    params = {"object_name": object_name} if object_name else {}
    metrics = client.command("get_mesh_metrics", params)
    if not metrics.get("success"):
        return {"ok": False, "error": "Failed to retrieve mesh metrics", "details": metrics}

    dims = metrics.get("dimensions", [])
    nonzero_axes = sum(1 for d in dims if isinstance(d, (int, float)) and d > 1e-6)
    is_degenerate = nonzero_axes < 2

    return {
        "ok": not is_degenerate,
        "is_degenerate": is_degenerate,
        "nonzero_axes": nonzero_axes,
        "dimensions": dims,
        "object_name": metrics.get("object_name", ""),
    }
