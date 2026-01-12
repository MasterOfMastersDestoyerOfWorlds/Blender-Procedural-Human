"""
Novel View Generation module for generating 3D views from segmentation masks.

This module provides:
- Hunyuan3D API server management (subprocess spawn/kill)
- API client for sending images and receiving 3D meshes
- Novel view generation from segmentation masks

The server is started when the addon loads and stopped when Blender quits
(not on addon reload).
"""

__all__ = [
    "start_hunyuan_server",
    "stop_hunyuan_server",
    "is_server_running",
    "is_server_running_cached",
    "is_server_starting",
    "get_server_start_error",
    "refresh_server_status",
    "get_server_url",
    "generate_3d_mesh",
]


def __getattr__(name):
    """Lazy import for module attributes."""
    if name in (
        "start_hunyuan_server",
        "stop_hunyuan_server",
        "is_server_running",
        "is_server_running_cached",
        "is_server_starting",
        "get_server_start_error",
        "refresh_server_status",
        "get_server_url",
    ):
        from procedural_human.novel_view_gen.server_manager import (
            start_hunyuan_server,
            stop_hunyuan_server,
            is_server_running,
            is_server_running_cached,
            is_server_starting,
            get_server_start_error,
            refresh_server_status,
            get_server_url,
        )
        return locals()[name]
    elif name == "generate_3d_mesh":
        from procedural_human.novel_view_gen.api_client import generate_3d_mesh
        return generate_3d_mesh
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
