"""
Curve Segmentation Workspace definition.

This module defines the custom workspace layout for the segmentation workflow.
"""

import bpy
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.workspace_decorator import (
    procedural_workspace,
    split_area_horizontal,
    split_area_vertical,
    set_area_type,
)
from procedural_human.image_search.search_asset_manager import SearchAssetManager
from procedural_human.logger import logger


@procedural_workspace
class CurveSegmentationWorkspace:
    """
    Custom workspace for curve segmentation workflow.
    
    Layout:
    - Top Left (2/3 height): VIEW_3D for 3D preview
    - Top Right (2/3 height): IMAGE_EDITOR for segmentation (with search panel in sidebar)
    - Bottom (1/3 height): Asset Browser showing Yandex search results
    """
    
    name = "Curve Segmentation" 
    
    @staticmethod
    def create_layout(context):
        """
        Create the workspace layout by splitting areas.
        
        The layout is:
        +-------------------+-------------------+
        |                   |                   |
        |     VIEW_3D       |   IMAGE_EDITOR    |
        |    (Preview)      |  (Segmentation)   |
        |                   |   [Search Panel]  |
        +-------------------+-------------------+
        |                                       |
        |            ASSET BROWSER              |
        |      (Yandex Search Results)          |
        |                                       |
        +---------------------------------------+
        """
        window = context.window
        if window is None:
            windows = context.window_manager.windows
            window = windows[0] if windows else None
        
        if window is None:
            logger.error("No window available in context")
            return
        
        screen = context.screen or window.screen
        if screen is None:
            logger.error("No screen available in context")
            return
        main_area = None
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                main_area = area
                break
        
        if main_area is None:
            for area in screen.areas:
                main_area = area
                break
        
        if main_area is None:
            logger.error("No areas found in screen")
            return
        logger.info(f"Screen '{screen.name}' has {len(screen.areas)} areas:")
        for i, area in enumerate(screen.areas):
            logger.info(f"  Area {i}: Type={area.type}, X={area.x}, Y={area.y}, W={area.width}, H={area.height}")
        result = split_area_horizontal(context, main_area, factor=0.33)
        if result is None:
            logger.error("Failed to split area horizontally")
            return
        
        top_area, bottom_area = result
        try:
            set_area_type(bottom_area, 'FILE_BROWSER')
            _configure_asset_browser(bottom_area)
            result = split_area_vertical(context, top_area, factor=0.5)
            if result is None:
                logger.error("Failed to split area vertically")
                return
            
            left_area, right_area = result
            set_area_type(left_area, 'VIEW_3D')  # 3D preview
            set_area_type(right_area, 'IMAGE_EDITOR')  # Segmentation view
            
            for space in left_area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
            for area in [left_area, right_area]:
                for space in area.spaces:
                    if hasattr(space, 'show_region_ui'):
                        space.show_region_ui = True

            timeline_area = None
            bottom_candidates = []
            target_types = {'TIMELINE', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'CONSOLE', 'INFO'}
            
            for area in screen.areas:
                if area.type in target_types:
                    bottom_candidates.append((area.y, area))
            bottom_candidates.sort(key=lambda x: x[0])
            
            if bottom_candidates:
                timeline_area = bottom_candidates[0][1]
                logger.info(f"Found bottom candidate area: Type={timeline_area.type}, Y={timeline_area.y}")
                override = {
                    "window": window,
                    "screen": screen,
                    "area": timeline_area,
                    "region": timeline_area.regions[-1],
                }

                with bpy.context.temp_override(**override):
                    bpy.ops.screen.area_close()
            
            logger.info("Curve Segmentation workspace layout created")
            
        except Exception as e:
            logger.error(f"Failed to create workspace layout: {e}")
            import traceback
            traceback.print_exc()


def _configure_asset_browser(area):
    """
    Configure a FILE_BROWSER area to show asset browser mode with the search results library.
    
    Args:
        area: The FILE_BROWSER area to configure
    """
    SearchAssetManager.register_asset_library()
    
    for space in area.spaces:
        if space.type == 'FILE_BROWSER':
            try:
                if hasattr(space, 'browse_mode'):
                    space.browse_mode = 'ASSETS'
                def configure_params():
                    try:
                        params = space.params
                        if params is None:
                            return 0.1  # Retry
                        if hasattr(params, 'display_type'):
                            params.display_type = 'THUMBNAIL'
                        if hasattr(params, 'display_size'):
                            params.display_size = 96
                        lib_name = SearchAssetManager.LIBRARY_NAME
                        if hasattr(params, 'asset_library_reference'):
                            try:
                                params.asset_library_reference = lib_name
                                logger.info(f"Set Asset Browser to library: {lib_name}")
                            except Exception as e:
                                logger.warning(f"Could not set to {lib_name}, using LOCAL: {e}")
                                params.asset_library_reference = 'LOCAL'
                        if hasattr(params, 'use_filter'):
                            params.use_filter = True
                        if hasattr(params, 'use_filter_material'):
                            params.use_filter_material = True
                            
                        logger.info("Configured Asset Browser for search results")
                    except Exception as e:
                        logger.warning(f"Error configuring params: {e}")
                    return None  # Don't repeat timer
                bpy.app.timers.register(configure_params, first_interval=0.2)
                
            except Exception as e:
                logger.warning(f"Could not fully configure Asset Browser: {e}")
            break



@procedural_operator
class OpenCurveSegmentationWorkspace(bpy.types.Operator):
    """Open the Curve Segmentation workspace"""
    
    bl_idname = "workspace.open_curve_segmentation"
    bl_label = "Open Curve Segmentation Workspace"
    bl_description = "Open or create the Curve Segmentation workspace with image search and segmentation panels"
    
    force_recreate: bpy.props.BoolProperty(
        name="Force Recreate",
        description="Delete existing workspace and create fresh",
        default=False
    )
    
    def execute(self, context):
        from procedural_human.decorators.workspace_decorator import procedural_workspace
        
        success = procedural_workspace.create_workspace(
            "CurveSegmentationWorkspace",
            context,
            force_recreate=self.force_recreate
        )
        
        if success:
            self.report({'INFO'}, "Opened Curve Segmentation workspace")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to create workspace")
            return {'CANCELLED'}


