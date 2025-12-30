"""
Workspace decorator system for automatic registration.

This decorator automatically sets up custom Blender workspaces
and manages workspace registration.
"""

import bpy
import re
from bpy.app.handlers import persistent
from procedural_human.decorators.discoverable_decorator import (
    DiscoverableClassDecorator,
)
from procedural_human.logger import *


def workspace_add_menu_draw(self, context):
    """Draw function to add our workspaces to the workspace add menu."""
    layout = self.layout
    
    if procedural_workspace.registry:
        layout.separator()
        # Add each workspace directly to the menu (no submenu)
        for class_name, workspace_cls in procedural_workspace.registry.items():
            op = layout.operator(
                "workspace.open_procedural_workspace",
                text=workspace_cls.name,
                icon='WORKSPACE'
            )
            op.workspace_class_name = class_name


@persistent
def _create_workspace_on_load(dummy):
    """Handler to create workspaces when a new file is loaded."""
    # Delay execution slightly to ensure Blender is ready
    if procedural_workspace.registry:
        bpy.app.timers.register(
            procedural_workspace._auto_create_workspaces, 
            first_interval=0.1
        )


class procedural_workspace(DiscoverableClassDecorator):
    """
    Decorator for workspace classes that automatically sets Blender workspace attributes.
    
    Usage:
        @procedural_workspace
        class CurveSegmentationWorkspace:
            name = "Curve Segmentation"
            
            @staticmethod
            def create_layout(context):
                # Workspace layout creation logic
                pass
    """

    registry = {}

    @staticmethod
    def setup_decorator(cls, **kwargs):
        """Set up the workspace class with proper attributes."""
        for key, value in kwargs.items():
            setattr(cls, key, value)
        
        class_name = cls.__name__
        
        # Auto-generate name if not provided
        if not hasattr(cls, "name"):
            # Convert CamelCase to Title With Spaces
            name_without_workspace = re.sub(r"Workspace$", "", class_name)
            cls.name = DiscoverableClassDecorator.to_title_with_spaces(name_without_workspace)
        
        # Ensure create_layout method exists
        if not hasattr(cls, "create_layout"):
            raise NotImplementedError(
                f"Workspace class {class_name} must implement create_layout(context) method"
            )
        
        procedural_workspace.registry[cls.__name__] = cls

    @classmethod
    def discover_and_register_all_decorators(cls):
        """
        Register all decorated workspace classes, menu, and operator.
        Also schedules auto-creation of workspaces.
        """
        logger.info(
            f"[Workspace Registry] Registered {len(procedural_workspace.registry.keys())} workspace definitions"
        )
        for workspace_cls in procedural_workspace.registry.values():
            logger.info(f"  - {workspace_cls.name}")
        
        # Register the generic workspace opener operator
        try:
            bpy.utils.register_class(OpenProceduralWorkspaceOperator)
        except Exception as e:
            logger.warning(f"Could not register workspace operator: {e}")
        
        # Add to workspace add menu (directly, no submenu)
        try:
            bpy.types.TOPBAR_MT_workspace_menu.append(workspace_add_menu_draw)
        except Exception as e:
            logger.warning(f"Could not append to workspace menu: {e}")
        
        # Register load_post handler to create workspaces on new file
        try:
            if _create_workspace_on_load not in bpy.app.handlers.load_post:
                bpy.app.handlers.load_post.append(_create_workspace_on_load)
        except Exception as e:
            logger.warning(f"Could not register load_post handler: {e}")
        
        # Schedule auto-creation of workspaces after Blender is fully loaded
        if cls.registry:
            bpy.app.timers.register(cls._auto_create_workspaces, first_interval=0.5)

    @classmethod
    def _auto_create_workspaces(cls):
        """
        Timer callback to auto-create registered workspaces.
        Called after Blender is fully initialized.
        """
        try:
            context = bpy.context
            
            for class_name, workspace_cls in cls.registry.items():
                # Check if workspace already exists
                if workspace_cls.name not in bpy.data.workspaces:
                    logger.info(f"Auto-creating workspace: {workspace_cls.name}")
                    
                    # Store the current workspace to return to it
                    original_workspace = context.window.workspace
                    
                    try:
                        # Create a fresh new workspace (not a duplicate)
                        bpy.ops.workspace.add()
                        
                        # Rename the new workspace
                        new_workspace = context.window.workspace
                        new_workspace.name = workspace_cls.name
                        
                        # Apply the layout
                        workspace_cls.create_layout(context)
                        
                        # Switch back to original workspace
                        context.window.workspace = original_workspace
                        
                        logger.info(f"Created workspace: {workspace_cls.name}")
                    except Exception as e:
                        logger.error(f"Failed to auto-create workspace '{workspace_cls.name}': {e}")
                else:
                    logger.info(f"Workspace '{workspace_cls.name}' already exists")
        except Exception as e:
            logger.error(f"Error in auto-create workspaces: {e}")
        
        return None  # Don't repeat the timer

    @classmethod
    def unregister_all_decorators(cls):
        """
        Unregister all decorated workspace classes, menu, and operator.
        """
        # Remove from workspace add menu
        try:
            bpy.types.TOPBAR_MT_workspace_menu.remove(workspace_add_menu_draw)
        except Exception:
            pass
        
        # Remove load_post handler
        try:
            if _create_workspace_on_load in bpy.app.handlers.load_post:
                bpy.app.handlers.load_post.remove(_create_workspace_on_load)
        except Exception:
            pass
        
        # Unregister operator
        try:
            bpy.utils.unregister_class(OpenProceduralWorkspaceOperator)
        except Exception:
            pass
        
        procedural_workspace.registry.clear()

    @classmethod
    def create_workspace(cls, workspace_class_name: str, context) -> bool:
        """
        Create a workspace by its class name.
        
        Args:
            workspace_class_name: The name of the registered workspace class
            context: The Blender context
            
        Returns:
            True if workspace was created successfully, False otherwise
        """
        if workspace_class_name not in cls.registry:
            logger.error(f"Workspace class '{workspace_class_name}' not found in registry")
            return False
        
        workspace_cls = cls.registry[workspace_class_name]
        
        # Check if workspace already exists
        if workspace_cls.name in bpy.data.workspaces:
            # Switch to existing workspace
            context.window.workspace = bpy.data.workspaces[workspace_cls.name]
            return True
        
        try:
            # Create a fresh new workspace (not a duplicate)
            bpy.ops.workspace.add()
            
            # Rename the new workspace
            new_workspace = context.window.workspace
            new_workspace.name = workspace_cls.name
            
            # Call the class's layout creation method
            workspace_cls.create_layout(context)
            
            logger.info(f"Created workspace: {workspace_cls.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create workspace '{workspace_cls.name}': {e}")
            return False

    @classmethod
    def get_registered_workspaces(cls) -> list:
        """
        Get a list of all registered workspace definitions.
        
        Returns:
            List of (class_name, display_name) tuples
        """
        return [
            (name, workspace_cls.name)
            for name, workspace_cls in cls.registry.items()
        ]


def split_area_horizontal(context, area, factor=0.5):
    """
    Split an area horizontally.
    
    Args:
        context: Blender context
        area: The area to split
        factor: Split position (0.0 to 1.0, default 0.5 for middle)
        
    Returns:
        Tuple of (top_area, bottom_area) or None if failed
    """
    # Store original area count
    original_areas = list(context.screen.areas)
    
    # Override context for the split operation
    with context.temp_override(area=area, region=area.regions[0]):
        bpy.ops.screen.area_split(direction='HORIZONTAL', factor=factor)
    
    # Find the new area
    new_areas = [a for a in context.screen.areas if a not in original_areas]
    if new_areas:
        # The original area becomes the top, new area is bottom
        return area, new_areas[0]
    
    return None


def split_area_vertical(context, area, factor=0.5):
    """
    Split an area vertically.
    
    Args:
        context: Blender context
        area: The area to split
        factor: Split position (0.0 to 1.0, default 0.5 for middle)
        
    Returns:
        Tuple of (left_area, right_area) or None if failed
    """
    # Store original area count
    original_areas = list(context.screen.areas)
    
    # Override context for the split operation
    with context.temp_override(area=area, region=area.regions[0]):
        bpy.ops.screen.area_split(direction='VERTICAL', factor=factor)
    
    # Find the new area
    new_areas = [a for a in context.screen.areas if a not in original_areas]
    if new_areas:
        # The original area becomes the left, new area is right
        return area, new_areas[0]
    
    return None


def set_area_type(area, area_type: str):
    """
    Change an area's editor type.
    
    Args:
        area: The Blender area
        area_type: One of 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', etc.
    """
    area.type = area_type


class OpenProceduralWorkspaceOperator(bpy.types.Operator):
    """Open a Procedural Human workspace"""
    
    bl_idname = "workspace.open_procedural_workspace"
    bl_label = "Open Procedural Workspace"
    bl_description = "Open or switch to a Procedural Human workspace"
    bl_options = {'REGISTER'}
    
    workspace_class_name: bpy.props.StringProperty(
        name="Workspace Class",
        description="Name of the workspace class to open",
        default=""
    )
    
    def execute(self, context):
        if not self.workspace_class_name:
            self.report({'ERROR'}, "No workspace specified")
            return {'CANCELLED'}
        
        success = procedural_workspace.create_workspace(
            self.workspace_class_name,
            context
        )
        
        if success:
            workspace_cls = procedural_workspace.registry.get(self.workspace_class_name)
            name = workspace_cls.name if workspace_cls else self.workspace_class_name
            self.report({'INFO'}, f"Opened workspace: {name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Failed to open workspace: {self.workspace_class_name}")
            return {'CANCELLED'}


