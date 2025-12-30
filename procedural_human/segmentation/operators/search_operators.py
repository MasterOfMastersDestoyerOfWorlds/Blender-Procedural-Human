"""
Yandex Search operators for the segmentation workflow.
"""

import bpy
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
            results = search.search(
                query=self.query,
                orientation=self.orientation,
                size=self.size,
                page=self.page
            )
            
            # Store results in scene properties for UI access
            context.scene["yandex_search_results"] = len(results)
            context.scene["yandex_search_query"] = self.query
            
            self.report({'INFO'}, f"Found {len(results)} images for '{self.query}'")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            self.report({'ERROR'}, f"Search failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "query")
        layout.prop(self, "orientation")
        layout.prop(self, "size")


@procedural_operator
class ClearSearchHistoryOperator(Operator):
    """Clear the Yandex search history"""
    
    bl_idname = "segmentation.clear_search_history"
    bl_label = "Clear Search History"
    bl_description = "Clear all saved search queries"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        search = get_search_instance()
        search.clear_history()
        self.report({'INFO'}, "Search history cleared")
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


