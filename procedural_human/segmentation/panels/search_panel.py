"""
Search panel for the segmentation workflow.

Provides UI for Yandex image search with filters, history, and thumbnail grid.
Uses Blender's preview collection system for displaying search result thumbnails.
"""

import os
import bpy
from bpy.types import Panel, PropertyGroup
from bpy.props import StringProperty, EnumProperty, IntProperty
from bpy.utils import previews

from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.logger import logger

# Global preview collection for search result thumbnails
_preview_collections = {}


def get_search_preview_collection():
    """Get or create the preview collection for search results."""
    if "yandex_search" not in _preview_collections:
        _preview_collections["yandex_search"] = previews.new()
    return _preview_collections["yandex_search"]


def clear_search_previews():
    """Clear all search result previews."""
    if "yandex_search" in _preview_collections:
        pcoll = _preview_collections["yandex_search"]
        pcoll.clear()


def load_image_preview(filepath: str, name: str) -> int:
    """
    Load an image into the preview collection.
    
    Args:
        filepath: Path to the image file
        name: Unique name for this preview
        
    Returns:
        The icon_id for use in UI elements
    """
    pcoll = get_search_preview_collection()
    
    if name not in pcoll:
        try:
            pcoll.load(name, filepath, 'IMAGE')
        except Exception as e:
            logger.error(f"Failed to load preview for {name}: {e}")
            return 0
    
    return pcoll[name].icon_id


def get_search_thumbnails_items(self, context):
    """
    EnumProperty callback to get search result thumbnails.
    Returns items for template_icon_view.
    """
    items = []
    pcoll = get_search_preview_collection()
    
    # Get cached search results from scene
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
    
    # Must have at least one item
    if not items:
        items.append(("NONE", "No Results", "", 0, 0))
    
    return items


def register_search_properties():
    """Register scene properties for search functionality."""
    bpy.types.Scene.yandex_search_query = StringProperty(
        name="Search Query",
        description="Enter search terms for Yandex image search",
        default=""
    )
    
    bpy.types.Scene.yandex_search_thumbnails = EnumProperty(
        name="Search Results",
        description="Click to select an image from search results",
        items=get_search_thumbnails_items
    )
    
    bpy.types.Scene.yandex_search_selected_index = IntProperty(
        name="Selected Index",
        default=0
    )


def unregister_search_properties():
    """Unregister scene properties."""
    try:
        del bpy.types.Scene.yandex_search_query
        del bpy.types.Scene.yandex_search_thumbnails
        del bpy.types.Scene.yandex_search_selected_index
    except:
        pass
    
    # Clean up preview collections
    for pcoll in _preview_collections.values():
        previews.remove(pcoll)
    _preview_collections.clear()


@procedural_panel
class SegmentationSearchPanel(Panel):
    """Yandex Image Search panel for finding reference images"""
    
    bl_label = "Image Search"
    bl_idname = "PROCEDURAL_PT_segmentation_search"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_category = "Segmentation"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Search input section
        box = layout.box()
        box.label(text="Yandex Image Search", icon='VIEWZOOM')
        
        # Search query input
        row = box.row(align=True)
        row.prop(scene, "yandex_search_query", text="", icon='VIEWZOOM')
        
        # Search and clear buttons
        row = box.row(align=True)
        op = row.operator("segmentation.yandex_search", text="Search", icon='VIEWZOOM')
        if hasattr(scene, "yandex_search_query"):
            op.query = scene.yandex_search_query
        row.operator("segmentation.clear_search_history", text="", icon='X')
        
        # Show search results info
        result_count = scene.get("yandex_search_results", 0)
        if result_count > 0:
            query = scene.get("yandex_search_query_last", "")
            box.label(text=f"Found {result_count} results for '{query}'")
        
        # Thumbnail grid
        layout.separator()
        box = layout.box()
        box.label(text="Search Results", icon='IMAGE_DATA')
        
        # Display thumbnail grid using template_icon_view
        pcoll = get_search_preview_collection()
        if len(pcoll) > 0:
            box.template_icon_view(scene, "yandex_search_thumbnails", show_labels=True)
            
            # Show selected image info
            selected = scene.yandex_search_thumbnails
            if selected and selected != "NONE":
                box.label(text=f"Selected: {selected}")
                row = box.row(align=True)
                row.operator("segmentation.load_selected_result", text="Load Image", icon='IMPORT')
        else:
            box.label(text="No search results yet")
            box.label(text="Enter a query above and click Search")
        
        # Load from disk section
        layout.separator()
        box = layout.box()
        box.label(text="Load from Disk", icon='FILE_IMAGE')
        box.operator("segmentation.load_image", text="Open Image", icon='FILE_FOLDER')
        
        # Current image info
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
class SegmentationSearchFiltersPanel(Panel):
    """Search filters sub-panel"""
    
    bl_label = "Search Filters"
    bl_idname = "PROCEDURAL_PT_segmentation_search_filters"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_category = "Segmentation"
    bl_parent_id = "PROCEDURAL_PT_segmentation_search"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Quick Filters:")
        
        # Get current query
        query = scene.get("yandex_search_query", "")
        
        row = layout.row(align=True)
        op = row.operator("segmentation.yandex_search", text="Portrait")
        op.query = query
        op.orientation = 'vertical'
        op.size = 'large'
        
        op = row.operator("segmentation.yandex_search", text="Landscape")
        op.query = query
        op.orientation = 'horizontal'
        op.size = 'large'
        
        row = layout.row(align=True)
        op = row.operator("segmentation.yandex_search", text="Large")
        op.query = query
        op.size = 'large'
        
        op = row.operator("segmentation.yandex_search", text="Wallpaper")
        op.query = query
        op.size = 'wallpaper'


@procedural_panel
class SegmentationSearchHistoryPanel(Panel):
    """Search history sub-panel"""
    
    bl_label = "Search History"
    bl_idname = "PROCEDURAL_PT_segmentation_search_history"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_category = "Segmentation"
    bl_parent_id = "PROCEDURAL_PT_segmentation_search"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        try:
            from procedural_human.segmentation.operators.search_operators import get_search_instance
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


