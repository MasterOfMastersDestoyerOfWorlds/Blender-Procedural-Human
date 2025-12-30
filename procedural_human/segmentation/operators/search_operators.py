"""
Yandex Search operators for the segmentation workflow.
"""

import bpy
import os
import tempfile
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty, IntProperty

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


# Global search instance (shared across operators)
_search_instance = None


def get_search_instance():
    """Get or create the global YandexImageSearch instance."""
    global _search_instance
    if _search_instance is None:
        from procedural_human.segmentation.yandex_search import YandexImageSearch
        _search_instance = YandexImageSearch()
    return _search_instance


def download_and_add_asset(result, index: int) -> bool:
    """
    Download a search result and add it as an asset.
    
    Args:
        result: SearchResult object
        index: Result index for naming
        
    Returns:
        True if successful
    """
    from procedural_human.segmentation.search_asset_manager import SearchAssetManager
    
    try:
        # Download the thumbnail (faster than full image)
        img = result.download_thumbnail()
        if img is None:
            logger.warning(f"Failed to download thumbnail for result {index}")
            return False
        
        # Save to temp file
        temp_dir = SearchAssetManager.get_temp_dir()
        filename = f"result_{index:03d}.jpg"
        filepath = temp_dir / filename
        
        # Save the image
        img.save(str(filepath), "JPEG", quality=90)
        
        # Create a clean name from the title or URL
        name = result.title[:30] if result.title else f"result_{index}"
        name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
        
        # Add as asset
        asset = SearchAssetManager.add_image_asset(str(filepath), f"{index:03d}_{name}")
        
        return asset is not None
        
    except Exception as e:
        logger.error(f"Failed to process result {index}: {e}")
        return False


@procedural_operator
class YandexImageSearchOperator(Operator):
    """Search Yandex Images for reference images"""
    
    bl_idname = "segmentation.yandex_search"
    bl_label = "Search Yandex Images"
    bl_description = "Search Yandex Images for reference photos"
    bl_options = {'REGISTER'}
    
    query: StringProperty(
        name="Search Query",
        description="Keywords to search for",
        default=""
    )
    
    orientation: EnumProperty(
        name="Orientation",
        description="Image orientation filter",
        items=[
            ('any', "Any", "All orientations"),
            ('horizontal', "Horizontal", "Landscape images"),
            ('vertical', "Vertical", "Portrait images"),
            ('square', "Square", "Square images"),
        ],
        default='any'
    )
    
    size: EnumProperty(
        name="Size",
        description="Image size filter",
        items=[
            ('any', "Any", "All sizes"),
            ('large', "Large", "Large images (recommended)"),
            ('medium', "Medium", "Medium sized images"),
            ('wallpaper', "Wallpaper", "Very large images"),
        ],
        default='large'
    )
    
    page: IntProperty(
        name="Page",
        description="Search results page",
        default=1,
        min=1
    )
    
    def execute(self, context):
        if not self.query:
            self.report({'WARNING'}, "Please enter a search query")
            return {'CANCELLED'}
        
        search = get_search_instance()
        
        try:
            # Import the asset manager
            from procedural_human.segmentation.search_asset_manager import SearchAssetManager
            
            # Clear previous search results
            SearchAssetManager.clear_assets()
            
            # Perform the search
            results = search.search(
                query=self.query,
                orientation=self.orientation,
                size=self.size,
                page=self.page
            )
            
            if not results:
                self.report({'WARNING'}, f"No results found for '{self.query}'")
                return {'CANCELLED'}
            
            # Download and add each result as an asset
            success_count = 0
            for i, result in enumerate(results[:20]):  # Limit to first 20 results
                if download_and_add_asset(result, i):
                    success_count += 1
                    
            # Refresh asset browser
            SearchAssetManager.refresh_asset_browser()
            
            # Store results in scene properties for UI access
            context.scene["yandex_search_results"] = success_count
            context.scene["yandex_search_query_last"] = self.query
            
            self.report({'INFO'}, f"Added {success_count} images to Asset Browser for '{self.query}'")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Search failed: {e}")
            return {'CANCELLED'}


@procedural_operator
class ClearSearchHistoryOperator(Operator):
    """Clear the Yandex search history and downloaded assets"""
    
    bl_idname = "segmentation.clear_search_history"
    bl_label = "Clear Search History"
    bl_description = "Clear all saved search queries and downloaded assets"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        search = get_search_instance()
        search.clear_history()
        
        # Also clear downloaded assets
        try:
            from procedural_human.segmentation.search_asset_manager import SearchAssetManager
            SearchAssetManager.clear_assets()
            SearchAssetManager.refresh_asset_browser()
        except Exception as e:
            logger.warning(f"Could not clear assets: {e}")
        
        self.report({'INFO'}, "Search history and assets cleared")
        return {'FINISHED'}


@procedural_operator
class LoadImageFromDiskOperator(Operator):
    """Load an image from disk for segmentation"""
    
    bl_idname = "segmentation.load_image"
    bl_label = "Load Image"
    bl_description = "Load an image from your computer"
    bl_options = {'REGISTER'}
    
    filepath: StringProperty(
        subtype='FILE_PATH',
        default=""
    )
    
    filter_glob: StringProperty(
        default="*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.webp",
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        if not self.filepath:
            self.report({'WARNING'}, "No file selected")
            return {'CANCELLED'}
        
        try:
            # Load image into Blender
            image = bpy.data.images.load(self.filepath)
            
            # Store reference for segmentation
            context.scene["segmentation_image"] = image.name
            
            # Try to show in active IMAGE_EDITOR
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    for space in area.spaces:
                        if space.type == 'IMAGE_EDITOR':
                            space.image = image
                            break
                    break
            
            self.report({'INFO'}, f"Loaded image: {image.name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            self.report({'ERROR'}, f"Failed to load image: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


