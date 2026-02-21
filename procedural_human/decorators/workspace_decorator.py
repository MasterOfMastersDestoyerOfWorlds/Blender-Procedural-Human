"""
Workspace decorator system for automatic registration.

This decorator automatically sets up custom Blender workspaces
and manages workspace registration.
"""

import bpy
import re
from pathlib import Path
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
    if procedural_workspace.registry:
        bpy.app.timers.register(
            procedural_workspace._auto_create_workspaces, 
            first_interval=0.1
        )


def _move_workspace_to_back(context, window, workspace_name: str):
    """Move workspace tab to back so default Layout stays first."""
    if workspace_name not in bpy.data.workspaces:
        return
    target_workspace = bpy.data.workspaces[workspace_name]
    previous_workspace = window.workspace
    try:
        window.workspace = target_workspace
        with context.temp_override(window=window, screen=window.screen):
            bpy.ops.workspace.reorder_to_back()
    except Exception as e:
        logger.warning(f"Could not reorder workspace '{workspace_name}' to back: {e}")
    finally:
        if previous_workspace is not None:
            window.workspace = previous_workspace


class procedural_workspace(DiscoverableClassDecorator):
    """
    Decorator for workspace classes that automatically sets Blender workspace attributes.
    
    Usage:
        @procedural_workspace
        class CurveSegmentationWorkspace:
            name = "Curve Segmentation"
            
            @staticmethod
            def create_layout(context):
                pass
    """

    registry = {}

    @staticmethod
    def setup_decorator(cls, **kwargs):
        """Set up the workspace class with proper attributes."""
        for key, value in kwargs.items():
            setattr(cls, key, value)
        
        class_name = cls.__name__
        if not hasattr(cls, "name"):
            name_without_workspace = re.sub(r"Workspace$", "", class_name)
            cls.name = DiscoverableClassDecorator.to_title_with_spaces(name_without_workspace)
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
        try:
            try:
                bpy.utils.unregister_class(OpenProceduralWorkspaceOperator)
            except RuntimeError:
                pass
            bpy.utils.register_class(OpenProceduralWorkspaceOperator)
        except Exception as e:
            logger.warning(f"Could not register workspace operator: {e}")
        try:
            try:
                bpy.types.TOPBAR_MT_workspace_menu.remove(workspace_add_menu_draw)
            except ValueError:
                pass
            bpy.types.TOPBAR_MT_workspace_menu.append(workspace_add_menu_draw)
        except Exception as e:
            logger.warning(f"Could not append to workspace menu: {e}")
        try:
            if _create_workspace_on_load not in bpy.app.handlers.load_post:
                bpy.app.handlers.load_post.append(_create_workspace_on_load)
        except Exception as e:
            logger.warning(f"Could not register load_post handler: {e}")
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
            window = context.window
            if window is None:
                windows = context.window_manager.windows
                if windows:
                    window = windows[0]
                else:
                    logger.error("Workspace auto-create failed: no window available")
                    return 0.2
            
            screen = context.screen or window.screen
            if screen is None:
                logger.error("Workspace auto-create failed: no screen available")
                return 0.2
            
            for class_name, workspace_cls in cls.registry.items():
                if workspace_cls.name in bpy.data.workspaces:
                    logger.info(f"Workspace '{workspace_cls.name}' already exists, skipping auto-create")
                    continue
                
                logger.info(f"Auto-creating workspace: {workspace_cls.name}")
                original_workspace = window.workspace
                
                try:
                    base_workspace = None
                    for ws_name in ["Modeling", "Sculpting", "UV Editing", "Layout"]:
                        if ws_name in bpy.data.workspaces:
                            base_workspace = bpy.data.workspaces[ws_name]
                            break
                    
                    if base_workspace is None and len(bpy.data.workspaces) > 0:
                        base_workspace = bpy.data.workspaces[0]
                    
                    if base_workspace:
                        window.workspace = base_workspace
                        logger.info(f"Using '{base_workspace.name}' as base workspace")
                    with context.temp_override(window=window, screen=window.screen):
                        bpy.ops.workspace.duplicate()
                    new_workspace = window.workspace
                    new_workspace.name = workspace_cls.name
                    logger.info("Joining all areas to create clean workspace...")
                    main_area = join_all_areas_to_one(context)
                    
                    if main_area:
                        main_area.type = 'VIEW_3D'
                    with context.temp_override(window=window, screen=window.screen):
                        workspace_cls.create_layout(context)
                    if original_workspace is not None:
                        window.workspace = original_workspace
                    _move_workspace_to_back(context, window, workspace_cls.name)
                    
                    logger.info(f"Created workspace: {workspace_cls.name}")
                except Exception as e:
                    logger.error(f"Failed to auto-create workspace '{workspace_cls.name}': {e}")
                    import traceback
                    traceback.print_exc()
        except Exception as e:
            logger.error(f"Error in auto-create workspaces: {e}")
        
        return None  # Don't repeat the timer

    @classmethod
    def unregister_all_decorators(cls):
        """
        Unregister all decorated workspace classes, menu, and operator.
        """
        try:
            bpy.types.TOPBAR_MT_workspace_menu.remove(workspace_add_menu_draw)
        except Exception:
            pass
        try:
            if _create_workspace_on_load in bpy.app.handlers.load_post:
                bpy.app.handlers.load_post.remove(_create_workspace_on_load)
        except Exception:
            pass
        try:
            bpy.utils.unregister_class(OpenProceduralWorkspaceOperator)
        except Exception:
            pass
        
        procedural_workspace.registry.clear()

    @classmethod
    def create_workspace(cls, workspace_class_name: str, context, force_recreate: bool = False) -> bool:
        """
        Create a workspace by its class name.
        
        Args:
            workspace_class_name: The name of the registered workspace class
            context: The Blender context
            force_recreate: If True, delete existing workspace and recreate it
            
        Returns:
            True if workspace was created successfully, False otherwise
        """
        if workspace_class_name not in cls.registry:
            logger.error(f"Workspace class '{workspace_class_name}' not found in registry")
            return False
        
        workspace_cls = cls.registry[workspace_class_name]
        if workspace_cls.name in bpy.data.workspaces:
            if force_recreate:
                logger.info(f"Force recreating workspace: {workspace_cls.name}")
                try:
                    ws_to_delete = bpy.data.workspaces[workspace_cls.name]
                    context.window.workspace = ws_to_delete
                    bpy.ops.workspace.delete()
                    logger.info(f"Deleted workspace: {workspace_cls.name}")
                except Exception as e:
                    logger.warning(f"Could not delete workspace: {e}")
                    return False
            else:
                context.window.workspace = bpy.data.workspaces[workspace_cls.name]
                return True
        
        try:
            base_workspace = None
            for ws_name in ["Modeling", "Sculpting", "UV Editing", "Layout"]:
                if ws_name in bpy.data.workspaces:
                    base_workspace = bpy.data.workspaces[ws_name]
                    break
            
            if base_workspace:
                context.window.workspace = base_workspace
                logger.info(f"Using '{base_workspace.name}' as base workspace")
            bpy.ops.workspace.duplicate()
            new_workspace = context.window.workspace
            new_workspace.name = workspace_cls.name
            logger.info("Joining all areas to create clean workspace...")
            main_area = join_all_areas_to_one(context)
            
            if main_area:
                main_area.type = 'VIEW_3D'
            workspace_cls.create_layout(context)
            _move_workspace_to_back(context, context.window, workspace_cls.name)
            
            logger.info(f"Created workspace: {workspace_cls.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create workspace '{workspace_cls.name}': {e}")
            import traceback
            traceback.print_exc()
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
    screen = context.screen or context.window.screen
    if screen is None:
        logger.warning("Cannot split area horizontally: no screen available")
        return None
    original_areas = list(screen.areas)
    with context.temp_override(area=area, region=area.regions[0]):
        bpy.ops.screen.area_split(direction='HORIZONTAL', factor=factor)
    new_areas = [a for a in screen.areas if a not in original_areas]
    if new_areas:
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
    screen = context.screen or context.window.screen
    if screen is None:
        logger.warning("Cannot split area vertically: no screen available")
        return None
    original_areas = list(screen.areas)
    with context.temp_override(area=area, region=area.regions[0]):
        bpy.ops.screen.area_split(direction='VERTICAL', factor=factor)
    new_areas = [a for a in screen.areas if a not in original_areas]
    if new_areas:
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


def join_all_areas_to_one(context):
    """
    Join all areas in the current screen into a single area.
    This provides a clean slate for creating a custom workspace layout.
    
    Args:
        context: Blender context
        
    Returns:
        The remaining single area, or None if failed
    """
    screen = context.screen or context.window.screen
    if screen is None:
        logger.warning("Cannot join areas: no screen available")
        return None
    max_attempts = 20  # Prevent infinite loops
    attempts = 0
    
    while len(screen.areas) > 1 and attempts < max_attempts:
        attempts += 1
        joined = False
        areas = sorted(screen.areas, key=lambda a: (a.y, a.x))
        for i, area in enumerate(areas):
            if joined:
                break
            for other_area in areas[i+1:]:
                if joined:
                    break
                if (abs(area.x + area.width - other_area.x) < 5 and
                    area.y < other_area.y + other_area.height and
                    area.y + area.height > other_area.y):
                    cursor_x = area.x + area.width
                    cursor_y = max(area.y, other_area.y) + min(area.height, other_area.height) // 2
                    try:
                        with context.temp_override(area=area):
                            bpy.ops.screen.area_join(cursor=(cursor_x, cursor_y))
                        joined = True
                    except Exception:
                        pass
                elif (abs(area.y + area.height - other_area.y) < 5 and
                      area.x < other_area.x + other_area.width and
                      area.x + area.width > other_area.x):
                    cursor_x = max(area.x, other_area.x) + min(area.width, other_area.width) // 2
                    cursor_y = area.y + area.height
                    try:
                        with context.temp_override(area=area):
                            bpy.ops.screen.area_join(cursor=(cursor_x, cursor_y))
                        joined = True
                    except Exception:
                        pass
        
        if not joined:
            if len(screen.areas) >= 2:
                area1 = screen.areas[0]
                area2 = screen.areas[1]
                try:
                    cursor_x = (area1.x + area1.width + area2.x) // 2
                    cursor_y = (area1.y + area1.height + area2.y) // 2
                    with context.temp_override(area=area1):
                        bpy.ops.screen.area_join(cursor=(cursor_x, cursor_y))
                except Exception:
                    break  # Give up if we can't join
    
    if len(screen.areas) == 1:
        return screen.areas[0]
    elif len(screen.areas) > 0:
        return max(screen.areas, key=lambda a: a.width * a.height)
    return None


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


