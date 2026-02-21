"""Image capture commands for Blender CLI."""

from __future__ import annotations

from tools.cli_registry import cli_command
from tools.commands.common import BlenderClient


@cli_command
def screenshot(client: BlenderClient, out: str = "", width: int = 800, height: int = 600) -> dict:
    """Render scene to PNG and return output path.

    :param client: Blender HTTP client.
    :param out: Optional output path.
    :param width: Render width in pixels.
    :param height: Render height in pixels.
    """
    params: dict = {"resolution": [width, height]}
    if out:
        params["output_path"] = out
    result = client.command("render_viewport", params)
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def capture_viewport(client: BlenderClient, out: str = "") -> dict:
    """Capture quick OpenGL viewport screenshot.

    :param client: Blender HTTP client.
    :param out: Optional output path.
    """
    params: dict = {}
    if out:
        params["output_path"] = out
    result = client.command("capture_viewport", params)
    result["ok"] = bool(result.get("success"))
    return result
