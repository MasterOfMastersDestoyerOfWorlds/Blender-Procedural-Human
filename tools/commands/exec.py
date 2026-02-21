"""Generic execution command for Blender CLI."""

from __future__ import annotations

from tools.cli_registry import cli_command
from tools.commands.common import BlenderClient


@cli_command
def exec(client: BlenderClient, code: str) -> dict:
    """Execute arbitrary Python code in Blender context.

    :param client: Blender HTTP client.
    :param code: Python source string executed with bpy in scope.
    """
    result = client.command("exec_python", {"code": code})
    result["ok"] = bool(result.get("success"))
    return result
