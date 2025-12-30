"""
Curve Segmentation Workspace definition.

This module defines the custom workspace layout for the segmentation workflow.
"""

import bpy
from procedural_human.decorators.workspace_decorator import (
    procedural_workspace,
    split_area_horizontal,
    split_area_vertical,
    set_area_type,
)
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
        screen = context.screen
        
        # Find the main VIEW_3D area
        main_area = None
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                main_area = area
                break
        
        if main_area is None:
            # If no VIEW_3D, use the first available area
            for area in screen.areas:
                main_area = area
                break
        
        if main_area is None:
            logger.error("No areas found in screen")
            return
        
        try:
            # Step 1: Split horizontally to create top (2/3) and bottom (1/3) areas
            # Factor 0.33 means the split happens at 1/3 from bottom
            result = split_area_horizontal(context, main_area, factor=0.33)
            if result is None:
                logger.error("Failed to split area horizontally")
                return
            
            top_area, bottom_area = result
            
            # Step 2: Set bottom area to FILE_BROWSER (Asset Browser mode)
            set_area_type(bottom_area, 'FILE_BROWSER')
            
            # Configure as Asset Browser showing search results
            _configure_asset_browser(bottom_area)
            
            # Step 3: Split top area vertically to create left and right
            result = split_area_vertical(context, top_area, factor=0.5)
            if result is None:
                logger.error("Failed to split area vertically")
                return
            
            left_area, right_area = result
            
            # Step 4: Set area types (VIEW_3D on left, IMAGE_EDITOR on right)
            set_area_type(left_area, 'VIEW_3D')  # 3D preview
            set_area_type(right_area, 'IMAGE_EDITOR')  # Segmentation view
            
            # Open sidebars for panels (search panel will be in IMAGE_EDITOR sidebar)
            for area in [left_area, right_area]:
                for space in area.spaces:
                    if hasattr(space, 'show_region_ui'):
                        space.show_region_ui = True
            
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
    from procedural_human.segmentation.search_asset_manager import SearchAssetManager
    
    # Ensure the asset library is registered
    SearchAssetManager.register_asset_library()
    
    for space in area.spaces:
        if space.type == 'FILE_BROWSER':
            try:
                # Set to asset browse mode
                if hasattr(space, 'browse_mode'):
                    space.browse_mode = 'ASSETS'
                
                # Configure params if available
                params = space.params
                if params is not None:
                    # Set display to thumbnails
                    if hasattr(params, 'display_type'):
                        params.display_type = 'THUMBNAIL'
                    
                    # Set thumbnail size
                    if hasattr(params, 'display_size'):
                        params.display_size = 96
                    
                    # Try to set the asset library reference
                    if hasattr(params, 'asset_library_reference'):
                        params.asset_library_reference = SearchAssetManager.LIBRARY_NAME
                    elif hasattr(params, 'asset_library_ref'):
                        params.asset_library_ref = SearchAssetManager.LIBRARY_NAME
                    
                    # Filter to show only images
                    if hasattr(params, 'use_filter'):
                        params.use_filter = True
                    if hasattr(params, 'use_filter_image'):
                        params.use_filter_image = True
                        
                logger.info("Configured Asset Browser for search results")
                
            except Exception as e:
                logger.warning(f"Could not fully configure Asset Browser: {e}")
            break


# Operator to create/switch to the workspace
from bpy.types import Operator
from procedural_human.decorators.operator_decorator import procedural_operator


@procedural_operator
class OpenCurveSegmentationWorkspace(Operator):
    """Open the Curve Segmentation workspace"""
    
    bl_idname = "workspace.open_curve_segmentation"
    bl_label = "Open Curve Segmentation Workspace"
    bl_description = "Open or create the Curve Segmentation workspace with image search and segmentation panels"
    
    def execute(self, context):
        from procedural_human.decorators.workspace_decorator import procedural_workspace
        
        success = procedural_workspace.create_workspace(
            "CurveSegmentationWorkspace",
            context
        )
        
        if success:
            self.report({'INFO'}, "Opened Curve Segmentation workspace")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to create workspace")
            return {'CANCELLED'}


