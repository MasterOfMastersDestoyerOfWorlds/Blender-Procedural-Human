"""Bootstrap script for starting Procedural Human addon in Blender."""

import bpy


def _ensure_addon():
    """Enable addon if needed so register() can auto-start HTTP server."""
    if "procedural_human" not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module="procedural_human")
    return None


bpy.app.timers.register(_ensure_addon, first_interval=0.5)
