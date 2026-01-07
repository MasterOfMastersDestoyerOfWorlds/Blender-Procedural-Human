"""
Gizmo decorator system for automatic registration.

This decorator automatically sets up Blender GizmoGroup classes
and manages their registration.
"""

import bpy
import re
from procedural_human.decorators.discoverable_decorator import (
    DiscoverableClassDecorator,
)
from procedural_human.logger import logger


class procedural_gizmo(DiscoverableClassDecorator):
    """
    Decorator for GizmoGroup classes that automatically sets Blender gizmo attributes.
    
    Usage:
        @procedural_gizmo
        class MyGizmoGroup(GizmoGroup):
            # bl_idname, bl_label, bl_space_type, bl_region_type auto-set
            
            def setup(self, context):
                pass
                
            def draw_prepare(self, context):
                pass
    """

    registry = {}
    _draw_handlers = {}  # Track draw handlers for cleanup

    @staticmethod
    def setup_decorator(cls, **kwargs):
        """Set up the GizmoGroup class with proper attributes."""
        for key, value in kwargs.items():
            setattr(cls, key, value)
        
        class_name = cls.__name__
        
        # Auto-generate bl_idname if not provided
        if not hasattr(cls, "bl_idname"):
            # Convert CamelCase to UPPER_CASE with GGT prefix
            snake_case = DiscoverableClassDecorator.to_snake_case(class_name)
            cls.bl_idname = f"MESH_GGT_{snake_case}"
        
        # Auto-generate bl_label if not provided
        if not hasattr(cls, "bl_label"):
            name_without_suffix = re.sub(r"(GizmoGroup|WidgetGroup|Gizmo)$", "", class_name)
            cls.bl_label = DiscoverableClassDecorator.to_title_with_spaces(name_without_suffix)
        
        # Set defaults for space and region type
        if not hasattr(cls, "bl_space_type"):
            cls.bl_space_type = 'VIEW_3D'
        
        if not hasattr(cls, "bl_region_type"):
            cls.bl_region_type = 'WINDOW'
        
        # Set default options for 3D gizmos
        if not hasattr(cls, "bl_options"):
            cls.bl_options = {'3D', 'PERSISTENT'}
        
        procedural_gizmo.registry[cls.__name__] = cls

    @classmethod
    def discover_and_register_all_decorators(cls):
        """
        Register all decorated GizmoGroup classes.
        """
        logger.info(
            f"[Gizmo Registry] Registering {len(procedural_gizmo.registry.keys())} gizmo groups"
        )
        
        for gizmo_cls in procedural_gizmo.registry.values():
            try:
                # Unregister first if already registered (hot-reload support)
                try:
                    bpy.utils.unregister_class(gizmo_cls)
                except RuntimeError:
                    pass
                bpy.utils.register_class(gizmo_cls)
                logger.info(f"  - Registered: {gizmo_cls.bl_idname}")
            except Exception as e:
                logger.warning(
                    f"Failed to register gizmo group {gizmo_cls.__name__}: {e}"
                )
        
        logger.info(
            f"[Gizmo Registry] Registered: {[gizmo_cls.bl_idname for gizmo_cls in procedural_gizmo.registry.values()]}"
        )

    @classmethod
    def unregister_all_decorators(cls):
        """
        Unregister all decorated GizmoGroup classes in reverse order.
        """
        # Remove any draw handlers
        for handler_key, handler in list(cls._draw_handlers.items()):
            try:
                bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
            except Exception:
                pass
        cls._draw_handlers.clear()
        
        # Unregister gizmo groups
        for gizmo_cls in reversed(list(procedural_gizmo.registry.values())):
            try:
                bpy.utils.unregister_class(gizmo_cls)
            except Exception as e:
                logger.warning(
                    f"Failed to unregister gizmo group {gizmo_cls.__name__}: {e}"
                )
        procedural_gizmo.registry.clear()

    @classmethod
    def register_draw_handler(cls, name: str, callback, args=(), draw_type='POST_VIEW'):
        """
        Register a GPU draw handler and track it for cleanup.
        
        Args:
            name: Unique name for this handler
            callback: The draw callback function
            args: Arguments to pass to the callback
            draw_type: 'POST_VIEW', 'POST_PIXEL', 'PRE_VIEW', etc.
        
        Returns:
            The handler reference
        """
        # Remove existing handler with same name
        if name in cls._draw_handlers:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(cls._draw_handlers[name], 'WINDOW')
            except Exception:
                pass
        
        handler = bpy.types.SpaceView3D.draw_handler_add(
            callback, args, 'WINDOW', draw_type
        )
        cls._draw_handlers[name] = handler
        return handler

    @classmethod
    def unregister_draw_handler(cls, name: str):
        """
        Unregister a specific draw handler by name.
        """
        if name in cls._draw_handlers:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(cls._draw_handlers[name], 'WINDOW')
            except Exception:
                pass
            del cls._draw_handlers[name]



