"""
Search operators for the segmentation workflow.

Includes Yandex/web image search and local folder loading operators.
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


def download_and_add_asset(result, index: int) -> dict:
    """
    Download a search result and add it as an asset.
    
    Args:
        result: SearchResult object
        index: Result index for naming
        
    Returns:
        Dict with result info if successful, None otherwise
    """
    from procedural_human.segmentation.search_asset_manager import SearchAssetManager
    from procedural_human.segmentation.panels.search_panel import load_image_preview
    
    try:
        # Download the thumbnail (faster than full image)
        img = result.download_thumbnail()
        if img is None:
            logger.warning(f"Failed to download thumbnail for result {index}")
            return None
        
        # Save to temp file
        temp_dir = SearchAssetManager.get_temp_dir()
        filename = f"result_{index:03d}.jpg"
        filepath = temp_dir / filename
        
        # Save the image
        img.save(str(filepath), "JPEG", quality=90)
        
        # Create a clean name from the title or URL
        name = result.title[:30] if result.title else f"result_{index}"
        name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
        full_name = f"{index:03d}_{name}"
        
        # Add as asset (for Asset Browser)
        asset = SearchAssetManager.add_image_asset(str(filepath), full_name)
        
        # Load into preview collection (for panel display)
        preview_name = f"search_{index:03d}"
        icon_id = load_image_preview(str(filepath), preview_name)
        
        if asset or icon_id:
            return {
                "name": preview_name,
                "title": name,
                "url": result.url,
                "filepath": str(filepath),
                "icon_id": icon_id,
            }
        return None
        
    except Exception as e:
        logger.error(f"Failed to process result {index}: {e}")
        return None


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
            
            # Report any fallback messages
            for msg in search.get_fallback_messages():
                self.report({'WARNING'}, msg)
            
            if not results:
                self.report({'WARNING'}, f"No results found for '{self.query}'")
                return {'CANCELLED'}
            
            # Download and add each result as an asset
            success_count = 0
            web_results = []
            for i, result in enumerate(results[:20]):  # Limit to first 20 results
                result_info = download_and_add_asset(result, i)
                if result_info:
                    success_count += 1
                    web_results.append(result_info)
            
            # Store cached results for panel display - MERGE with local folder results
            existing_results = context.scene.get("yandex_search_cached_results", [])
            # Keep local folder results, replace web search results
            local_results = [r for r in existing_results if r.get("name", "").startswith("local_")]
            combined_results = web_results + local_results
            context.scene["yandex_search_cached_results"] = combined_results
                    
            # Refresh asset browser
            SearchAssetManager.refresh_asset_browser()
            
            # Debug: Log asset browser state
            self._debug_asset_browser_state(context, SearchAssetManager)
            
            # Store results in scene properties for UI access
            context.scene["yandex_search_results"] = success_count
            context.scene["yandex_search_query_last"] = self.query
            
            # Auto-load the first result into the Image Editor
            if cached_results:
                first_result = cached_results[0]
                filepath = first_result.get("filepath", "")
                if filepath and os.path.exists(filepath):
                    try:
                        image = bpy.data.images.load(filepath)
                        context.scene["segmentation_image"] = image.name
                        
                        # Show in all IMAGE_EDITOR areas
                        for area in context.screen.areas:
                            if area.type == 'IMAGE_EDITOR':
                                for space in area.spaces:
                                    if space.type == 'IMAGE_EDITOR':
                                        space.image = image
                                        area.tag_redraw()
                                        break
                        
                        logger.info(f"Auto-loaded first result: {image.name}")
                    except Exception as e:
                        logger.warning(f"Could not auto-load first result: {e}")
            
            # Report with source info
            source = search.get_last_source()
            if source != "Yandex":
                self.report({'INFO'}, f"Using {source}: Loaded {success_count} images for '{self.query}'")
            else:
                self.report({'INFO'}, f"Loaded {success_count} images for '{self.query}'")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Search failed: {e}")
            return {'CANCELLED'}
    
    def _debug_asset_browser_state(self, context, SearchAssetManager):
        """Debug: Log the current state of asset browsers and yandex assets."""
        import bpy
        
        # Count yandex materials in bpy.data.materials
        yandex_mats = [mat for mat in bpy.data.materials if mat.name.startswith("yandex_")]
        yandex_mat_assets = [mat for mat in yandex_mats if mat.asset_data is not None]
        
        # Count yandex images in bpy.data.images
        yandex_images = [img for img in bpy.data.images if img.name.startswith("yandex_")]
        
        logger.info(f"=== Asset Browser Debug ===")
        logger.info(f"Yandex materials loaded: {len(yandex_mats)}")
        logger.info(f"Yandex materials marked as assets: {len(yandex_mat_assets)}")
        logger.info(f"Yandex images loaded: {len(yandex_images)}")
        
        # Log temp directory contents
        temp_dir = SearchAssetManager.get_temp_dir()
        if temp_dir.exists():
            files = list(temp_dir.iterdir())
            logger.info(f"Temp directory: {temp_dir}")
            logger.info(f"Files in temp dir: {len(files)}")
            
            # Check for the critical .blend file
            blend_file = temp_dir / "search_results.blend"
            if blend_file.exists():
                logger.info(f"  ✓ search_results.blend exists ({blend_file.stat().st_size} bytes)")
            else:
                logger.warning(f"  ✗ search_results.blend MISSING - assets won't show in browser!")
            
            for f in files[:5]:  # Show first 5
                logger.info(f"  - {f.name}")
            if len(files) > 5:
                logger.info(f"  ... and {len(files) - 5} more")
        
        # Check asset library registration
        logger.info(f"Asset library registered: {SearchAssetManager._registered}")
        logger.info(f"Asset library name: {SearchAssetManager.LIBRARY_NAME}")
        
        # Check asset libraries in preferences
        prefs = bpy.context.preferences.filepaths.asset_libraries
        logger.info(f"Registered asset libraries in Blender: {len(prefs)}")
        for lib in prefs:
            if "yandex" in lib.name.lower() or "search" in lib.name.lower():
                logger.info(f"  Found library: '{lib.name}' at '{lib.path}'")
        
        # Check FILE_BROWSER areas
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'FILE_BROWSER':
                    for space in area.spaces:
                        if space.type == 'FILE_BROWSER':
                            browse_mode = getattr(space, 'browse_mode', 'UNKNOWN')
                            logger.info(f"Found FILE_BROWSER area: browse_mode={browse_mode}")
                            if hasattr(space, 'params') and space.params:
                                params = space.params
                                # Try to get the asset library reference
                                asset_lib_ref = getattr(params, 'asset_library_reference', None)
                                asset_lib_ref_str = getattr(params, 'asset_library_ref', None)
                                display_type = getattr(params, 'display_type', 'N/A')
                                
                                # Log what we found
                                if asset_lib_ref is not None:
                                    logger.info(f"  asset_library_reference: {asset_lib_ref}")
                                if asset_lib_ref_str is not None:
                                    logger.info(f"  asset_library_ref: {asset_lib_ref_str}")
                                logger.info(f"  display_type: {display_type}")
                                
                                # Check if LOCAL mode shows assets
                                if str(asset_lib_ref) == 'LOCAL' or str(asset_lib_ref_str) == 'LOCAL':
                                    logger.info(f"  → Should show Current File assets (LOCAL mode)")
                                else:
                                    logger.info(f"  → Set to external library mode")
        
        logger.info(f"=== End Asset Browser Debug ===")


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
class LoadSelectedResultOperator(Operator):
    """Load the selected search result image into the Image Editor"""
    
    bl_idname = "segmentation.load_selected_result"
    bl_label = "Load Selected Result"
    bl_description = "Load the selected search result into the Image Editor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        
        # Get the selected thumbnail name
        selected = scene.yandex_search_thumbnails
        if not selected or selected == "NONE":
            self.report({'WARNING'}, "No image selected")
            return {'CANCELLED'}
        
        # Find the cached result info
        cached_results = scene.get("yandex_search_cached_results", [])
        result_info = None
        for result in cached_results:
            if result.get("name") == selected:
                result_info = result
                break
        
        if not result_info:
            self.report({'WARNING'}, "Could not find selected image data")
            return {'CANCELLED'}
        
        filepath = result_info.get("filepath", "")
        if not filepath or not os.path.exists(filepath):
            self.report({'ERROR'}, "Image file not found")
            return {'CANCELLED'}
        
        try:
            # Load image into Blender
            image = bpy.data.images.load(filepath)
            
            # Store reference for segmentation
            scene["segmentation_image"] = image.name
            
            # Show in IMAGE_EDITOR
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    for space in area.spaces:
                        if space.type == 'IMAGE_EDITOR':
                            space.image = image
                            break
                    break
            
            self.report({'INFO'}, f"Loaded: {result_info.get('title', image.name)}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            self.report({'ERROR'}, f"Failed to load image: {e}")
            return {'CANCELLED'}


@procedural_operator
class ActivateAssetOperator(Operator):
    """Operator called when an asset is double-clicked in the Asset Browser/Shelf"""
    
    bl_idname = "segmentation.activate_asset"
    bl_label = "Activate Asset"
    bl_description = "Load the asset's image into the Image Editor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get the active asset from context
        asset = getattr(context, 'asset', None)
        
        if asset is None:
            # Try to get from active_file
            active_file = getattr(context, 'active_file', None)
            if active_file:
                asset_name = getattr(active_file, 'name', '')
                if asset_name:
                    mat = bpy.data.materials.get(asset_name)
                    if mat:
                        return self._load_material_image(context, mat)
            
            self.report({'WARNING'}, "No asset selected")
            return {'CANCELLED'}
        
        # Try to find the material by asset name
        mat = bpy.data.materials.get(asset.name)
        if mat:
            return self._load_material_image(context, mat)
        
        self.report({'WARNING'}, f"Material not found: {asset.name}")
        return {'CANCELLED'}
    
    def _load_material_image(self, context, mat):
        """Load the image from a material into the Image Editor."""
        if mat.node_tree is None:
            self.report({'WARNING'}, "Material has no node tree")
            return {'CANCELLED'}
        
        # Find the image texture node
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                image = node.image
                
                # Store reference for segmentation
                context.scene["segmentation_image"] = image.name
                
                # Load into all Image Editors
                loaded = False
                for window in bpy.context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'IMAGE_EDITOR':
                            for space in area.spaces:
                                if space.type == 'IMAGE_EDITOR':
                                    space.image = image
                                    area.tag_redraw()
                                    loaded = True
                
                if loaded:
                    self.report({'INFO'}, f"Loaded: {image.name}")
                    return {'FINISHED'}
                else:
                    self.report({'WARNING'}, "No Image Editor found")
                    return {'CANCELLED'}
        
        self.report({'WARNING'}, "No image texture found in material")
        return {'CANCELLED'}


@procedural_operator
class LoadAssetToSegmentation(Operator):
    """Load the active asset's image into the Image Editor for segmentation"""
    
    bl_idname = "segmentation.load_asset_to_editor"
    bl_label = "Load Asset to Segmentation"
    bl_description = "Load the selected material asset's image into the Image Editor"
    bl_options = {'REGISTER', 'UNDO'}
    
    asset_name: bpy.props.StringProperty(
        name="Asset Name",
        description="Name of the asset to load (optional, will use active if not set)",
        default=""
    )
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        image_to_load = None
        asset_name = self.asset_name
        
        # If asset_name is provided, load that specific asset
        if asset_name:
            mat = bpy.data.materials.get(asset_name)
            if mat and mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        image_to_load = node.image
                        break
        
        # If no specific asset, try to get the active file from Asset Browser
        if image_to_load is None:
            active_file = getattr(context, 'active_file', None)
            if active_file:
                # The active file has a name attribute
                file_name = getattr(active_file, 'name', '')
                if file_name:
                    # Try to find matching material
                    mat = bpy.data.materials.get(file_name)
                    if mat and mat.node_tree:
                        for node in mat.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image:
                                image_to_load = node.image
                                break
        
        # If still no image, try to use the last yandex material
        if image_to_load is None:
            yandex_mats = [m for m in bpy.data.materials if m.name.startswith("yandex_")]
            for mat in reversed(yandex_mats):  # Try most recent first
                if mat.node_tree:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            image_to_load = node.image
                            break
                if image_to_load:
                    break
        
        if image_to_load is None:
            self.report({'WARNING'}, "No image found. Run a search first.")
            return {'CANCELLED'}
        
        # Store reference for segmentation
        context.scene["segmentation_image"] = image_to_load.name
        
        # Load into ALL Image Editors
        loaded = False
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        space.image = image_to_load
                        area.tag_redraw()
                        loaded = True
                        break
        
        if loaded:
            self.report({'INFO'}, f"Loaded: {image_to_load.name}")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, f"No Image Editor found to display: {image_to_load.name}")
            return {'CANCELLED'}


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


# ============================================================================
# Local Folder Operators
# ============================================================================

@procedural_operator
class BrowseLocalFolderOperator(Operator):
    """Browse for a local folder containing images"""
    
    bl_idname = "segmentation.browse_local_folder"
    bl_label = "Browse Local Folder"
    bl_description = "Select a folder containing images to load into the Asset Browser"
    bl_options = {'REGISTER'}
    
    directory: StringProperty(
        subtype='DIR_PATH',
        default=""
    )
    
    def execute(self, context):
        if not self.directory:
            self.report({'WARNING'}, "No folder selected")
            return {'CANCELLED'}
        
        try:
            from procedural_human.segmentation.local_folder_manager import LocalFolderManager
            
            # Set the folder and load images
            count = LocalFolderManager.set_folder(self.directory)
            
            if count == 0:
                self.report({'WARNING'}, "No images found in folder")
                return {'CANCELLED'}
            
            # Store folder path in scene for UI display
            context.scene.segmentation_local_folder = self.directory
            context.scene["segmentation_local_image_count"] = count
            
            # Auto-load the first image into the Image Editor
            self._auto_load_first_image(context)
            
            self.report({'INFO'}, f"Loaded {count} images from folder")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to load folder: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Failed to load folder: {e}")
            return {'CANCELLED'}
    
    def _auto_load_first_image(self, context):
        """Load the first local image into the Image Editor."""
        # Find the first local material
        for mat in bpy.data.materials:
            if mat.name.startswith("local_") and mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        image = node.image
                        context.scene["segmentation_image"] = image.name
                        
                        # Load into Image Editors
                        for area in context.screen.areas:
                            if area.type == 'IMAGE_EDITOR':
                                for space in area.spaces:
                                    if space.type == 'IMAGE_EDITOR':
                                        space.image = image
                                        area.tag_redraw()
                                        break
                        
                        logger.info(f"Auto-loaded first local image: {image.name}")
                        return
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


@procedural_operator
class RefreshLocalFolderOperator(Operator):
    """Refresh the local folder to detect new images"""
    
    bl_idname = "segmentation.refresh_local_folder"
    bl_label = "Refresh Local Folder"
    bl_description = "Scan the folder again for new images"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from procedural_human.segmentation.local_folder_manager import LocalFolderManager
            
            folder = LocalFolderManager.get_watched_folder()
            if folder is None:
                self.report({'WARNING'}, "No folder is being watched. Browse for a folder first.")
                return {'CANCELLED'}
            
            # Refresh the folder
            new_count = LocalFolderManager.refresh_folder()
            
            # Update count in scene
            context.scene["segmentation_local_image_count"] = LocalFolderManager.get_image_count()
            
            if new_count > 0:
                self.report({'INFO'}, f"Added {new_count} new image(s)")
            else:
                self.report({'INFO'}, "No new images found")
            
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to refresh folder: {e}")
            self.report({'ERROR'}, f"Failed to refresh folder: {e}")
            return {'CANCELLED'}


@procedural_operator
class ClearLocalFolderOperator(Operator):
    """Clear local folder images and stop watching"""
    
    bl_idname = "segmentation.clear_local_folder"
    bl_label = "Clear Local Folder"
    bl_description = "Remove all loaded local folder images and stop watching for changes"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from procedural_human.segmentation.local_folder_manager import LocalFolderManager
            from procedural_human.segmentation.search_asset_manager import SearchAssetManager
            
            # Clear local assets
            LocalFolderManager.clear_local_assets()
            
            # Clear scene properties
            context.scene.segmentation_local_folder = ""
            context.scene["segmentation_local_image_count"] = 0
            
            # Refresh asset browser
            SearchAssetManager.refresh_asset_browser()
            
            self.report({'INFO'}, "Local folder cleared")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to clear local folder: {e}")
            self.report({'ERROR'}, f"Failed to clear: {e}")
            return {'CANCELLED'}


