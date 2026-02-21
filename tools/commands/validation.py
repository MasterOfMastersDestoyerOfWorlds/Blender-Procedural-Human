"""High-level validation commands that compose lower-level CLI commands."""

from __future__ import annotations

from tools.cli_registry import cli_command
from tools.commands.common import BlenderClient, parse_inputs
from tools.commands.geometry import (
    validate_geometry,
    check_watertight,
    check_camera_visibility,
    check_degenerate,
)
from tools.commands.capture import screenshot


def _fail(reason: str, details: dict | None = None) -> dict:
    payload = {"ok": False, "error": reason}
    if details:
        payload["details"] = details
    return payload


def _run_preflight(client: BlenderClient, object_name: str, do_watertight: bool) -> dict:
    geo = validate_geometry(client, object_name=object_name)
    if not geo.get("ok"):
        return _fail("Geometry validation failed", geo)

    if geo.get("vertex_count", 0) < 2:
        return _fail("Geometry has fewer than 2 vertices", geo)
    if geo.get("face_count", 0) < 1:
        return _fail("Geometry has no faces", geo)

    watertight_result: dict = {"skipped": True}
    if do_watertight:
        watertight_result = check_watertight(client, object_name=object_name)
        if not watertight_result.get("ok"):
            return _fail(
                f"Mesh is not watertight: {watertight_result.get('non_manifold_edges', 0)} non-manifold edges",
                watertight_result,
            )

    degenerate_result = check_degenerate(client, object_name=object_name)
    if not degenerate_result.get("ok"):
        return _fail("Geometry is degenerate (collapsed to point or line)", degenerate_result)

    visibility = check_camera_visibility(client, object_name=object_name)
    if not visibility.get("ok"):
        return _fail("Object is not visible to active camera", visibility)

    shot = screenshot(client)
    if not shot.get("ok"):
        return _fail("Screenshot render failed", shot)

    return {
        "ok": True,
        "object_name": object_name,
        "checks": {
            "geometry": geo,
            "watertight": watertight_result,
            "degenerate": degenerate_result,
            "camera_visibility": visibility,
        },
        "screenshot": shot,
        "screenshot_path": shot.get("path"),
    }


@cli_command
def preflight(client: BlenderClient, object_name: str = "NodeGroupTest", no_watertight: bool = False) -> dict:
    """Run geometry pre-flight checks on an existing object.

    :param client: Blender HTTP client.
    :param object_name: Name of object to validate.
    :param no_watertight: Disable watertight check.
    """
    return _run_preflight(client, object_name=object_name, do_watertight=not no_watertight)


@cli_command
def validate(
    client: BlenderClient,
    group: str,
    object_name: str = "NodeGroupTest",
    no_watertight: bool = False,
    inputs: str = "{}",
) -> dict:
    """Run full validation cycle: reload clean scene, apply node group, run preflight checks.

    :param client: Blender HTTP client.
    :param group: Name of geometry node group to test.
    :param object_name: Name of object to create and validate.
    :param no_watertight: Disable watertight check.
    :param inputs: JSON object string with modifier input values.
    """
    reload_result = client.command("reload_addon", {"clean_scene": True})
    if not reload_result.get("success"):
        return _fail("Reload step failed", reload_result)

    parsed_inputs, error = parse_inputs(inputs)
    if error:
        return _fail(error)

    apply_result = client.command(
        "apply_node_group",
        {"group_name": group, "object_name": object_name, "inputs": parsed_inputs},
    )
    if not apply_result.get("success"):
        return _fail("Failed to apply node group", apply_result)

    preflight_result = _run_preflight(
        client,
        object_name=object_name,
        do_watertight=not no_watertight,
    )
    preflight_result["reload"] = reload_result
    preflight_result["apply"] = apply_result
    return preflight_result
