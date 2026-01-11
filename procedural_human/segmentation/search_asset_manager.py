"""
Search Asset Manager for image search results and local folder images.

This module manages a temporary asset library that stores downloaded search results
and local folder images, making them available in Blender's Asset Browser for easy
browsing and selection.
"""

import bpy
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, List

from procedural_human.logger import logger


class SearchAssetManager:
    """
    Manages a temporary asset library for image search results and local folder images.
    
    This class:
    - Creates and manages a temp directory for downloaded/copied images
    - Registers this directory as a Blender Asset Library
    - Provides methods to add images as assets with previews (yandex_ and local_ prefixes)
    - Handles cleanup on addon unload
    """
    
    LIBRARY_NAME = "Search Results"
    
    # Catalog UUIDs for different sources (must be valid UUIDs - hex only: 0-9, a-f)
    CATALOG_SEARCH = "7a1c5e2d-8f3b-4a9e-b6c1-2d3e4f5a6b7c"
    CATALOG_LOCAL = "8b2d6f3e-9a4c-5b0f-c7d2-3e4f5a6a7b8d"
    _temp_dir: Optional[Path] = None
    _registered: bool = False
    _assets: List[str] = []  # Track loaded asset names
    
    @classmethod
    def get_temp_dir(cls) -> Path:
        """
        Get or create the temporary directory for search results.
        
        Returns:
            Path to the temp directory
        """
        if cls._temp_dir is None or not cls._temp_dir.exists():
            cls._temp_dir = Path(tempfile.mkdtemp(prefix="blender_yandex_search_"))
            logger.info(f"Created temp directory for search assets: {cls._temp_dir}")
            
            # Create a blender_assets.cats.txt file for asset catalogs
            cls._create_catalog_file()
        
        return cls._temp_dir
    
    @classmethod
    def _create_catalog_file(cls):
        """Create the asset catalog definition file."""
        if cls._temp_dir is None:
            return
            
        catalog_file = cls._temp_dir / "blender_assets.cats.txt"
        catalog_content = f"""# This is an Asset Catalog Definition file for Blender.
#
# Empty lines and lines starting with `#` will be ignored.
# The first non-ignored line should be the version indicator.
# Other lines are of the format "UUID:catalog/path/for/assets:Simple Catalog Name"

VERSION 1

# Web Search Results catalog
{cls.CATALOG_SEARCH}:search_results:Web Search

# Local Folder catalog
{cls.CATALOG_LOCAL}:local_folder:Local Folder
"""
        try:
            with open(catalog_file, 'w') as f:
                f.write(catalog_content)
            logger.info(f"Created asset catalog file: {catalog_file}")
        except Exception as e:
            logger.error(f"Failed to create catalog file: {e}")
    
    @classmethod
    def register_asset_library(cls):
        """
        Register the temp directory as a Blender Asset Library.
        This makes the search results available in the Asset Browser.
        """
        if cls._registered:
            return
            
        temp_dir = cls.get_temp_dir()
        prefs = bpy.context.preferences.filepaths.asset_libraries
        
        # Check if already registered
        for lib in prefs:
            if lib.name == cls.LIBRARY_NAME:
                # Update path if needed
                if lib.path != str(temp_dir):
                    lib.path = str(temp_dir)
                cls._registered = True
                logger.info(f"Updated existing asset library: {cls.LIBRARY_NAME}")
                return
        
        # Add new library
        try:
            new_lib = prefs.new(name=cls.LIBRARY_NAME)
            new_lib.path = str(temp_dir)
            cls._registered = True
            logger.info(f"Registered asset library: {cls.LIBRARY_NAME} at {temp_dir}")
        except Exception as e:
            logger.error(f"Failed to register asset library: {e}")
    
    @classmethod
    def unregister_asset_library(cls):
        """Remove the asset library from Blender preferences."""
        prefs = bpy.context.preferences.filepaths.asset_libraries
        
        # Find and remove the library
        for i, lib in enumerate(prefs):
            if lib.name == cls.LIBRARY_NAME:
                prefs.remove(lib)
                cls._registered = False
                logger.info(f"Unregistered asset library: {cls.LIBRARY_NAME}")
                break
    
    @classmethod
    def clear_assets(cls):
        """Clear web search assets only (preserves local folder assets)."""
        # Clear only yandex previews from the preview collection
        try:
            from procedural_human.segmentation.panels.search_panel import get_search_preview_collection
            pcoll = get_search_preview_collection()
            # Only remove search_ prefixed previews (web search), not local_
            search_keys = [k for k in pcoll.keys() if k.startswith("search_")]
            for key in search_keys:
                try:
                    del pcoll[key]
                except Exception:
                    pass
        except Exception:
            pass
        
        # Remove only yandex materials from Blender
        for mat_name in list(bpy.data.materials.keys()):
            if mat_name.startswith("yandex_"):
                try:
                    mat = bpy.data.materials[mat_name]
                    bpy.data.materials.remove(mat)
                except Exception:
                    pass
        
        # Remove only yandex images from Blender
        for img_name in list(bpy.data.images.keys()):
            if img_name.startswith("yandex_"):
                try:
                    img = bpy.data.images[img_name]
                    bpy.data.images.remove(img)
                except Exception:
                    pass
        
        if cls._temp_dir is None or not cls._temp_dir.exists():
            # Only clear yandex assets from tracking
            cls._assets = [a for a in cls._assets if not a.startswith("yandex_")]
            logger.info("Cleared web search assets")
            return
            
        # Remove only yandex files from temp directory (preserve local_ files)
        for item in cls._temp_dir.iterdir():
            if item.name.startswith("yandex_"):
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    logger.error(f"Failed to remove {item}: {e}")
        
        # Clear only yandex assets from tracking
        cls._assets = [a for a in cls._assets if not a.startswith("yandex_")]
        
        logger.info("Cleared web search assets")
    
    @classmethod
    def _create_material_asset(
        cls, 
        image_path: str, 
        name: str, 
        prefix: str, 
        catalog_id: str,
        description_prefix: str
    ) -> Optional[bpy.types.Material]:
        """
        Internal method to create a Material asset with the image as a texture.
        
        This is the single code path used by both web search and local folder assets.
        
        Args:
            image_path: Path to the image file
            name: Name for the asset (without prefix)
            prefix: Prefix for asset name (e.g., 'yandex_' or 'local_')
            catalog_id: UUID of the catalog to assign
            description_prefix: Prefix for the description (e.g., 'Search result' or 'Local folder')
            
        Returns:
            The created Material data-block, or None if failed
        """
        try:
            # Ensure the image exists
            if not os.path.exists(image_path):
                logger.error(f"Image not found: {image_path}")
                return None
            
            # Copy image to temp directory if not already there
            temp_dir = cls.get_temp_dir()
            image_filename = f"{prefix}{name}{Path(image_path).suffix}"
            dest_path = temp_dir / image_filename
            
            if str(image_path) != str(dest_path):
                shutil.copy2(image_path, dest_path)
            
            # Create material asset name
            asset_name = f"{prefix}{name}"
            
            # Remove existing material with same name
            if asset_name in bpy.data.materials:
                bpy.data.materials.remove(bpy.data.materials[asset_name])
            
            # Create a new material
            mat = bpy.data.materials.new(name=asset_name)
            mat.use_nodes = True
            
            # Clear default nodes
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            # Create nodes: Image Texture -> Principled BSDF -> Output
            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            output_node.location = (300, 0)
            
            bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            bsdf_node.location = (0, 0)
            
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.location = (-300, 0)
            
            # Load the image
            img = bpy.data.images.load(str(dest_path))
            img.name = f"{asset_name}_img"
            tex_node.image = img
            
            # Connect nodes
            links = mat.node_tree.links
            links.new(tex_node.outputs['Color'], bsdf_node.inputs['Base Color'])
            links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
            
            # Mark material as asset
            mat.asset_mark()
            
            # Set asset metadata
            mat.asset_data.description = f"{description_prefix}: {name}"
            mat.asset_data.catalog_id = catalog_id
            
            # Load custom preview using the image file
            try:
                with bpy.context.temp_override(id=mat):
                    bpy.ops.ed.lib_id_load_custom_preview(filepath=str(dest_path))
            except Exception as e:
                logger.warning(f"Could not load custom preview: {e}")
                # Fallback to generated preview
                mat.asset_generate_preview()
            
            # Track this asset
            cls._assets.append(asset_name)
            
            logger.info(f"Added material asset: {asset_name}")
            return mat
            
        except Exception as e:
            logger.error(f"Failed to add material asset '{prefix}{name}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @classmethod
    def add_image_asset(cls, image_path: str, name: str) -> Optional[bpy.types.Material]:
        """
        Create a Material asset from a web search result.
        
        Args:
            image_path: Path to the image file
            name: Name for the asset
            
        Returns:
            The created Material data-block, or None if failed
        """
        return cls._create_material_asset(
            image_path=image_path,
            name=name,
            prefix="yandex_",
            catalog_id=cls.CATALOG_SEARCH,
            description_prefix="Search result"
        )
    
    @classmethod
    def add_local_image_asset(cls, image_path: str, name: str) -> Optional[bpy.types.Material]:
        """
        Create a Material asset from a local folder image.
        
        Args:
            image_path: Path to the image file
            name: Name for the asset
            
        Returns:
            The created Material data-block, or None if failed
        """
        return cls._create_material_asset(
            image_path=image_path,
            name=name,
            prefix="local_",
            catalog_id=cls.CATALOG_LOCAL,
            description_prefix="Local folder"
        )
    
    @classmethod
    def save_assets_to_blend(cls):
        """
        Save all material assets to a .blend file in the temp directory.
        This is required for the Asset Browser to display external assets.
        
        Uses the same approach as Asset Bridge - save the file to the library location.
        """
        temp_dir = cls.get_temp_dir()
        blend_file = temp_dir / "search_results.blend"
        
        try:
            # Get list of yandex and local materials to save
            mats_to_save = [
                mat for mat in bpy.data.materials 
                if (mat.name.startswith("yandex_") or mat.name.startswith("local_")) 
                and mat.asset_data is not None
            ]
            
            if not mats_to_save:
                logger.warning("No material assets to save")
                return
            
            logger.info(f"Saving {len(mats_to_save)} material assets to {blend_file}")
            
            # Save to a separate .blend file using wm.save_as_mainfile
            # This preserves all asset data including previews
            bpy.ops.wm.save_as_mainfile(
                filepath=str(blend_file),
                copy=True,  # Don't change current file path
                check_existing=False,
                compress=True
            )
            
            logger.info(f"Saved {len(mats_to_save)} assets to: {blend_file}")
            
        except Exception as e:
            logger.error(f"Failed to save assets to blend file: {e}")
            import traceback
            traceback.print_exc()
    
    @classmethod
    def refresh_asset_browser(cls):
        """Refresh all Asset Browser areas to show updated assets."""
        # First save assets to blend file
        cls.save_assets_to_blend()
        
        # Find the Asset Browser area and configure it
        file_browser_area = None
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'FILE_BROWSER':
                    file_browser_area = area
                    for space in area.spaces:
                        if space.type == 'FILE_BROWSER':
                            # Set to asset browse mode
                            if hasattr(space, 'browse_mode'):
                                space.browse_mode = 'ASSETS'
                            
                            # Configure params
                            if hasattr(space, 'params') and space.params:
                                params = space.params
                                
                                # Set display to thumbnails
                                if hasattr(params, 'display_type'):
                                    params.display_type = 'THUMBNAIL'
                            
                            # Trigger a refresh
                            area.tag_redraw()
        
        # Try to refresh the asset library by invoking the refresh operator
        if file_browser_area:
            try:
                # Find a region in the area
                for region in file_browser_area.regions:
                    if region.type == 'WINDOW':
                        with bpy.context.temp_override(area=file_browser_area, region=region):
                            bpy.ops.asset.library_refresh()
                            logger.info("Refreshed asset library")
                        break
            except Exception as e:
                logger.debug(f"library_refresh: {e}")
        
        # Also trigger a general UI update
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()
    
    @classmethod
    def cleanup(cls):
        """
        Clean up resources on addon unload.
        Removes temp directory and unregisters asset library.
        """
        cls.unregister_asset_library()
        
        if cls._temp_dir is not None and cls._temp_dir.exists():
            try:
                shutil.rmtree(cls._temp_dir)
                logger.info(f"Cleaned up temp directory: {cls._temp_dir}")
            except Exception as e:
                logger.error(f"Failed to clean up temp directory: {e}")
            cls._temp_dir = None
        
        cls._assets.clear()
        cls._registered = False


_last_active_asset = None
_asset_watch_timer_running = False


def _load_material_image_to_editor(mat_name: str) -> bool:
    """
    Load the image from a material into all Image Editors.
    Returns True if successful.
    """
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        logger.warning(f"Material not found: {mat_name}")
        return False
    
    if not mat.node_tree:
        logger.warning(f"Material has no node tree: {mat_name}")
        return False
    
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and node.image:
            image = node.image
            
            # Store reference for segmentation
            try:
                bpy.context.scene["segmentation_image"] = image.name
            except Exception:
                pass
            
            # Load into all Image Editors
            loaded_count = 0
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'IMAGE_EDITOR':
                        for space in area.spaces:
                            if space.type == 'IMAGE_EDITOR':
                                space.image = image
                                area.tag_redraw()
                                loaded_count += 1
            
            logger.info(f"Loaded image '{image.name}' from material '{mat_name}' into {loaded_count} editor(s)")
            return True
    
    logger.warning(f"No image texture node found in material: {mat_name}")
    return False


def _is_segmentation_asset(name: str) -> bool:
    """Check if an asset name is a segmentation asset (yandex or local)."""
    return name.startswith("yandex_") or name.startswith("local_")


def _watch_asset_selection():
    """
    Timer callback to watch for asset selection changes in the Asset Browser.
    When a yandex or local folder asset is selected, load its image into the Image Editor.
    """
    global _last_active_asset, _asset_watch_timer_running
    
    try:
        # Only run in the segmentation workspace
        if not bpy.context.window or bpy.context.window.workspace.name != "Curve Segmentation":
            return 0.5  # Keep checking
        
        # Find the Asset Browser area
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'FILE_BROWSER':
                    for space in area.spaces:
                        if space.type == 'FILE_BROWSER' and getattr(space, 'browse_mode', '') == 'ASSETS':
                            # Try to get active file through context override
                            try:
                                with bpy.context.temp_override(window=window, area=area, space_data=space):
                                    active_file = getattr(bpy.context, 'active_file', None)
                                    if active_file:
                                        asset_name = getattr(active_file, 'name', '')
                                        
                                        # Process yandex or local materials if changed
                                        if asset_name and _is_segmentation_asset(asset_name) and asset_name != _last_active_asset:
                                            _last_active_asset = asset_name
                                            logger.info(f"Asset selected: {asset_name}")
                                            success = _load_material_image_to_editor(asset_name)
                                            if not success:
                                                logger.warning(f"Failed to load image for asset: {asset_name}")
                            except Exception as e:
                                logger.debug(f"Context override failed: {e}")
        
        return 0.2  # Check every 200ms
        
    except Exception as e:
        logger.warning(f"Asset watch error: {e}")
        return 0.5


def _on_depsgraph_update(scene, depsgraph):
    """
    Handler to detect when a segmentation material is applied to an object.
    When a yandex or local material is applied (e.g., by drag-drop in Asset Browser),
    automatically load its image into the Image Editor.
    """
    global _last_active_asset
    
    try:
        # Check if we're in the segmentation workspace
        if bpy.context.window.workspace.name != "Curve Segmentation":
            return
        
        # Check the active object's active material
        obj = bpy.context.active_object
        if obj is None or not hasattr(obj, 'active_material'):
            return
        
        mat = obj.active_material
        if mat is None:
            return
        
        # Only process segmentation materials (yandex or local)
        if not _is_segmentation_asset(mat.name):
            return
        
        # Avoid processing the same material multiple times
        if mat.name == _last_active_asset:
            return
        
        _last_active_asset = mat.name
        
        # Find the image in the material's node tree
        if mat.node_tree is None:
            return
        
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                image = node.image
                
                # Store reference for segmentation
                scene["segmentation_image"] = image.name
                
                # Load into all Image Editors
                for window in bpy.context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'IMAGE_EDITOR':
                            for space in area.spaces:
                                if space.type == 'IMAGE_EDITOR':
                                    space.image = image
                                    area.tag_redraw()
                
                logger.info(f"Auto-loaded image from applied material: {image.name}")
                break
                
    except Exception as e:
        # Silently ignore errors in depsgraph handler
        pass
 

def register():
    """Register the search asset manager."""
    global _asset_watch_timer_running
    
    SearchAssetManager.register_asset_library()
    
    # Add depsgraph handler to detect material applications
    if _on_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(_on_depsgraph_update)
    
    # Start the asset selection watcher timer
    if not _asset_watch_timer_running:
        bpy.app.timers.register(_watch_asset_selection, first_interval=1.0, persistent=True)
        _asset_watch_timer_running = True
        logger.info("Started asset selection watcher timer")


def unregister():
    """Unregister and clean up."""
    global _asset_watch_timer_running
    
    # Stop the asset selection watcher timer
    if _asset_watch_timer_running:
        try:
            bpy.app.timers.unregister(_watch_asset_selection)
        except Exception:
            pass
        _asset_watch_timer_running = False
    
    # Remove depsgraph handler
    if _on_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_on_depsgraph_update)
    
    SearchAssetManager.cleanup()

