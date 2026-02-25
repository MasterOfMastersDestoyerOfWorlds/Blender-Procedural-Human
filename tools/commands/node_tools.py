"""CLI commands for node group development: open, export, list-groups, inspect, diff."""

from __future__ import annotations

from tools.cli_registry import cli_command
from tools.commands.common import BlenderClient


@cli_command
def open(client: BlenderClient, filepath: str) -> dict:
    """Open a .blend file in the running Blender instance.

    :param client: Blender HTTP client.
    :param filepath: Absolute path to the .blend file to open.
    """
    result = client.command("open_file", {"filepath": filepath})
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def list_groups(client: BlenderClient) -> dict:
    """List all registered geo_node_group functions and Blender node groups.

    :param client: Blender HTTP client.
    """
    result = client.command("list_groups", {})
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def inspect(client: BlenderClient, group: str) -> dict:
    """Inspect a node group's structure: nodes, links, interface, frames.

    :param client: Blender HTTP client.
    :param group: Name of the node group to inspect.
    """
    result = client.command("inspect_group", {"group": group})
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def export(client: BlenderClient, group: str, use_helpers: bool = True,
           split_frames: bool = False, include_labels: bool = True,
           include_locations: bool = False, include_names: bool = False) -> dict:
    """Export a node group to Python via the node exporter.

    :param client: Blender HTTP client.
    :param group: Name of the node group to export.
    :param use_helpers: Substitute node_helpers where patterns match.
    :param split_frames: Split top-level frames into separate files.
    :param include_labels: Include node labels in output.
    :param include_locations: Include node locations in output.
    :param include_names: Include node names in output.
    """
    result = client.command("export_group", {
        "group": group,
        "use_helpers": use_helpers,
        "split_frames": split_frames,
        "include_labels": include_labels,
        "include_locations": include_locations,
        "include_names": include_names,
    })
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def diff(client: BlenderClient, group: str, baseline: str = "",
         save: str = "") -> dict:
    """Compare mesh metrics of a node group, optionally against a baseline.

    :param client: Blender HTTP client.
    :param group: Name of the node group to evaluate.
    :param baseline: Path to a baseline JSON file to compare against.
    :param save: Path to save current metrics as a new baseline.
    """
    result = client.command("diff_group", {
        "group": group,
        "baseline": baseline,
        "save": save,
    })
    result["ok"] = bool(result.get("success"))
    return result
