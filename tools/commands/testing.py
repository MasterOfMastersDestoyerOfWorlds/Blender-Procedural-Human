"""CLI commands wrapping Coon-patch testing server handlers."""

from __future__ import annotations

from tools.cli_registry import cli_command
from tools.commands.common import BlenderClient


@cli_command
def verify_topology(client: BlenderClient, point_csv: str = "", edge_csv: str = "") -> dict:
    """Verify mesh topology using point and edge CSV files.

    :param client: Blender HTTP client.
    :param point_csv: Path to point CSV file (uses latest export if omitted).
    :param edge_csv: Path to edge CSV file (uses latest export if omitted).
    """
    result = client.command("verify_topology", {
        "point_csv": point_csv,
        "edge_csv": edge_csv,
    })
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def get_csv_data(client: BlenderClient) -> dict:
    """Get CSV data from the latest point/edge exports.

    :param client: Blender HTTP client.
    """
    result = client.command("get_csv_data", {})
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def get_point_data(client: BlenderClient, point_id: int) -> dict:
    """Get data for a specific point ID from the latest CSV export.

    :param client: Blender HTTP client.
    :param point_id: ID of the point to inspect.
    """
    result = client.command("get_point_data", {"point_id": point_id})
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def check_corner(client: BlenderClient, corner_id: int) -> dict:
    """Check topology for a specific corner point.

    :param client: Blender HTTP client.
    :param corner_id: ID of the corner to check.
    """
    result = client.command("check_corner", {"corner_id": corner_id})
    result["ok"] = bool(result.get("success"))
    return result
