"""
Search panel for the segmentation workflow.

Provides UI for web image search and local folder loading with filters,
history, and thumbnail grid. Uses Blender's preview collection system
for displaying search result thumbnails.
"""

import os
import bpy
from bpy.types import Panel, PropertyGroup
from bpy.props import StringProperty, EnumProperty, IntProperty
from bpy.utils import previews

from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.image_search.search_operators import get_search_instance
from procedural_human.logger import logger
from procedural_human.image_search.search_asset_manager import get_search_preview_collection





def get_search_thumbnails_items(self, context):
    """
    EnumProperty callback to get search result thumbnails.
    Returns items for template_icon_view.
    """
    items = []
    pcoll = get_search_preview_collection()
    search_results = context.scene.get("yandex_search_cached_results", [])
    
    for i, result in enumerate(search_results):
        name = result.get("name", f"result_{i}")
        if name in pcoll:
            items.append((
                name,  # identifier
                name,  # name
                result.get("url", ""),  # description (stores URL)
                pcoll[name].icon_id,  # icon
                i  # value
            ))
    if not items:
        items.append(("NONE", "No Results", "", 0, 0))
    
    return items


def _on_thumbnail_selection_changed(self, context):
    """Callback when the user selects a different thumbnail - auto-load the image."""
    selected = self.yandex_search_thumbnails
    if not selected or selected == "NONE":
        return
    cached_results = self.get("yandex_search_cached_results", [])
    result_info = None
    for result in cached_results:
        if result.get("name") == selected:
            result_info = result
            break
    
    if not result_info:
        return
    
    filepath = result_info.get("filepath", "")
    if not filepath or not os.path.exists(filepath):
        return
    
    try:
        image = bpy.data.images.load(filepath)
        self["segmentation_image"] = image.name
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    for space in area.spaces:
                        if space.type == 'IMAGE_EDITOR':
                            space.image = image
                            area.tag_redraw()
                            break
        
        logger.info(f"Auto-loaded image: {image.name}")
    except Exception as e:
        logger.error(f"Failed to auto-load image: {e}")


def register_search_properties():
    """Register scene properties for search functionality."""
    bpy.types.Scene.yandex_search_query = StringProperty(
        name="Search Query",
        description="Enter search terms for Yandex image search",
        default=""
    )
    
    bpy.types.Scene.yandex_search_orientation = EnumProperty(
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
    
    bpy.types.Scene.yandex_search_size = EnumProperty(
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
    
    bpy.types.Scene.yandex_search_thumbnails = EnumProperty(
        name="Search Results",
        description="Click to select an image from search results",
        items=get_search_thumbnails_items,
        update=_on_thumbnail_selection_changed  # Auto-load on selection change
    )
    
    bpy.types.Scene.yandex_search_selected_index = IntProperty(
        name="Selected Index",
        default=0
    )
    bpy.types.Scene.segmentation_local_folder = StringProperty(
        name="Local Folder",
        description="Path to a folder containing images to load",
        subtype='DIR_PATH',
        default=""
    )





@procedural_panel
class SegmentationSearchPanel(Panel):
    """Image search and local folder panel for finding reference images"""
    
    bl_label = "Image Search"
    bl_idname = "PROCEDURAL_PT_segmentation_search"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Search"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        box.label(text="Local Folder", icon='FILE_FOLDER')
        row = box.row(align=True)
        row.prop(scene, "segmentation_local_folder", text="")
        row.operator("segmentation.browse_local_folder", text="", icon='FILEBROWSER')
        folder = scene.segmentation_local_folder
        if folder:
            image_count = scene.get("segmentation_local_image_count", 0)
            box.label(text=f"{image_count} image(s) loaded")
            row = box.row(align=True)
            row.operator("segmentation.refresh_local_folder", text="Refresh", icon='FILE_REFRESH')
            row.operator("segmentation.clear_local_folder", text="", icon='X')
        layout.separator()
        box = layout.box()
        box.label(text="Web Image Search", icon='VIEWZOOM')
        row = box.row(align=True)
        row.prop(scene, "yandex_search_query", text="", icon='VIEWZOOM')
        row = box.row(align=True)
        row.prop(scene, "yandex_search_orientation", text="")
        row.prop(scene, "yandex_search_size", text="")
        row = box.row(align=True)
        op = row.operator("segmentation.yandex_search", text="Search", icon='VIEWZOOM')
        if hasattr(scene, "yandex_search_query"):
            op.query = scene.yandex_search_query
        if hasattr(scene, "yandex_search_orientation"):
            op.orientation = scene.yandex_search_orientation
        if hasattr(scene, "yandex_search_size"):
            op.size = scene.yandex_search_size
        row.operator("segmentation.clear_search_history", text="", icon='X')
        result_count = scene.get("yandex_search_results", 0)
        if result_count > 0:
            query = scene.get("yandex_search_query_last", "")
            box.label(text=f"Found {result_count} results for '{query}'")
        layout.separator()
        box = layout.box()
        box.label(text="Click to Load", icon='IMAGE_DATA')
        pcoll = get_search_preview_collection()
        if len(pcoll) > 0:
            box.template_icon_view(scene, "yandex_search_thumbnails", show_labels=True)
        else:
            box.label(text="No search results yet")
            box.label(text="Enter a query above and click Search")
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR' and space.image:
                        layout.separator()
                        info_box = layout.box()
                        info_box.label(text="Current Image", icon='IMAGE_DATA')
                        info_box.label(text=f"  {space.image.name}")
                        info_box.label(text=f"  {space.image.size[0]} x {space.image.size[1]}")
                        break
                break


@procedural_panel
class AssetBrowserSegmentationPanel(Panel):
    """Panel in Asset Browser with segmentation info"""
    
    bl_label = "Segmentation"
    bl_idname = "PROCEDURAL_PT_asset_browser_segmentation"
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_category = "Segmentation"
    
    @classmethod
    def poll(cls, context):
        if context.area and context.area.type == 'FILE_BROWSER':
            for space in context.area.spaces:
                if space.type == 'FILE_BROWSER':
                    return getattr(space, 'browse_mode', '') == 'ASSETS'
        return False
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Click to select & load", icon='RESTRICT_SELECT_OFF')
        box.label(text="to Image Editor", icon='IMAGE_DATA')
        
        layout.separator()
        seg_image = context.scene.get("segmentation_image", "")
        if seg_image and seg_image in bpy.data.images:
            layout.label(text="Current Image:", icon='IMAGE_DATA')
            layout.label(text=f"  {seg_image[:25]}...")
        else:
            layout.label(text="No image loaded", icon='INFO')


@procedural_panel
class SegmentationSearchHistoryPanel(Panel):
    """Search history sub-panel"""
    
    bl_label = "Search History"
    bl_idname = "PROCEDURAL_PT_segmentation_search_history"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Search"
    bl_parent_id = "PROCEDURAL_PT_segmentation_search"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        try:
            search = get_search_instance()
            history = search.get_history()
            
            if history:
                for i, query in enumerate(history[:5]):  # Show last 5
                    row = layout.row()
                    op = row.operator(
                        "segmentation.yandex_search",
                        text=query.query[:30] + "..." if len(query.query) > 30 else query.query,
                        icon='DOT'
                    )
                    op.query = query.query
                    op.orientation = query.orientation
                    op.size = query.size
            else:
                layout.label(text="No recent searches")
        except Exception:
            layout.label(text="No history available")


