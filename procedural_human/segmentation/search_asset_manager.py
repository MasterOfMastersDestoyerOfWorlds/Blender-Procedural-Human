"""
Search Asset Manager for Yandex image search results.

This module manages a temporary asset library that stores downloaded search results,
making them available in Blender's Asset Browser for easy browsing and selection.
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
    Manages a temporary asset library for Yandex image search results.
    
    This class:
    - Creates and manages a temp directory for downloaded images
    - Registers this directory as a Blender Asset Library
    - Provides methods to add images as assets with previews
    - Handles cleanup on addon unload
    """
    
    LIBRARY_NAME = "Yandex Search Results"
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
        catalog_content = """# This is an Asset Catalog Definition file for Blender.
#
# Empty lines and lines starting with `#` will be ignored.
# The first non-ignored line should be the version indicator.
# Other lines are of the format "UUID:catalog/path/for/assets:Simple Catalog Name"

VERSION 1

# Yandex Search Results catalog
7a1c5e2d-8f3b-4a9e-b6c1-2d3e4f5a6b7c:search_results:Search Results
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
        """Clear all downloaded assets from the temp directory."""
        if cls._temp_dir is None or not cls._temp_dir.exists():
            return
            
        # Remove all files except the catalog file
        for item in cls._temp_dir.iterdir():
            if item.name != "blender_assets.cats.txt":
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    logger.error(f"Failed to remove {item}: {e}")
        
        # Clear tracked assets
        cls._assets.clear()
        
        # Remove any loaded images from Blender
        for img_name in list(bpy.data.images.keys()):
            if img_name.startswith("yandex_"):
                try:
                    img = bpy.data.images[img_name]
                    bpy.data.images.remove(img)
                except Exception:
                    pass
        
        logger.info("Cleared all search assets")
    
    @classmethod
    def add_image_asset(cls, image_path: str, name: str) -> Optional[bpy.types.Image]:
        """
        Load an image and mark it as an asset.
        
        Args:
            image_path: Path to the image file
            name: Name for the asset
            
        Returns:
            The loaded Blender Image data-block, or None if failed
        """
        try:
            # Ensure the image exists
            if not os.path.exists(image_path):
                logger.error(f"Image not found: {image_path}")
                return None
            
            # Copy image to temp directory if not already there
            temp_dir = cls.get_temp_dir()
            image_filename = f"yandex_{name}{Path(image_path).suffix}"
            dest_path = temp_dir / image_filename
            
            if str(image_path) != str(dest_path):
                shutil.copy2(image_path, dest_path)
            
            # Load the image into Blender
            asset_name = f"yandex_{name}"
            
            # Remove existing image with same name
            if asset_name in bpy.data.images:
                bpy.data.images.remove(bpy.data.images[asset_name])
            
            img = bpy.data.images.load(str(dest_path))
            img.name = asset_name
            
            # Mark as asset
            img.asset_mark()
            
            # Set asset metadata
            img.asset_data.description = f"Yandex search result: {name}"
            img.asset_data.catalog_id = "7a1c5e2d-8f3b-4a9e-b6c1-2d3e4f5a6b7c"
            
            # Generate preview thumbnail
            img.asset_generate_preview()
            
            # Track this asset
            cls._assets.append(asset_name)
            
            logger.info(f"Added image asset: {asset_name}")
            return img
            
        except Exception as e:
            logger.error(f"Failed to add image asset '{name}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @classmethod
    def save_assets_to_blend(cls):
        """
        Save all assets to a .blend file in the temp directory.
        This is required for the Asset Browser to display external assets.
        """
        temp_dir = cls.get_temp_dir()
        blend_file = temp_dir / "search_results.blend"
        
        try:
            # Save the current file to the temp location
            # We need to save the images as assets
            bpy.ops.wm.save_as_mainfile(
                filepath=str(blend_file),
                copy=True,
                check_existing=False
            )
            logger.info(f"Saved assets to: {blend_file}")
        except Exception as e:
            logger.error(f"Failed to save assets: {e}")
    
    @classmethod
    def refresh_asset_browser(cls):
        """Refresh all Asset Browser areas to show updated assets."""
        # Tag areas for redraw
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'FILE_BROWSER':
                    for space in area.spaces:
                        if space.type == 'FILE_BROWSER':
                            # Trigger a refresh
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


def register():
    """Register the search asset manager."""
    SearchAssetManager.register_asset_library()


def unregister():
    """Unregister and clean up."""
    SearchAssetManager.cleanup()
