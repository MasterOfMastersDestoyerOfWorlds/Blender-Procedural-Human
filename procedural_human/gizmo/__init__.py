"""
Gizmo module for Procedural Human.

Contains GizmoGroup implementations for mesh editing tools,
including the Bezier handle gizmo system for lofting curves.
"""

from procedural_human.gizmo.mesh_curves_gizmo import (
    ATTR_HANDLE_LEFT,
    ATTR_HANDLE_RIGHT,
    ensure_handle_attributes,
    calculate_auto_handles,
    calculate_auto_handles_bmesh,
    ensure_bmesh_layers,
    has_bmesh_handle_layers,
    register,
    unregister,
)

__all__ = [
    "ATTR_HANDLE_LEFT",
    "ATTR_HANDLE_RIGHT",
    "ensure_handle_attributes",
    "calculate_auto_handles",
    "calculate_auto_handles_bmesh",
    "ensure_bmesh_layers",
    "has_bmesh_handle_layers",
    "register",
    "unregister",
] 
