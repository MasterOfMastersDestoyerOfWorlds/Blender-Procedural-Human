"""
Local Folder Manager for loading images from disk.

This module provides functionality to load images from a local folder,
display them as material assets in the Asset Browser, and watch for
new images being added to the folder.
"""

import bpy
import os
from pathlib import Path
from typing import Optional, List, Set

from procedural_human.image_search.search_asset_manager import SearchAssetManager
from procedural_human.image_search.search_asset_manager import get_search_preview_collection, load_image_preview
from procedural_human.logger import logger
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}


class LocalFolderManager:
    """
    Manages local folder image sources with file watching.
    
    This class:
    - Scans a folder for image files
    - Adds each image as a material asset (via SearchAssetManager)
    - Watches the folder for new images and adds them automatically
    - Tracks known files to avoid re-adding existing ones
    """
    
    _watched_folder: Optional[Path] = None
    _known_files: Set[str] = set()
    _watcher_running: bool = False
    
    @classmethod
    def get_watched_folder(cls) -> Optional[Path]:
        """Get the currently watched folder path."""
        return cls._watched_folder
    
    @classmethod
    def scan_folder(cls, folder_path: Path) -> List[Path]:
        """
        Scan a folder for image files.
        
        Args:
            folder_path: Path to the folder to scan
            
        Returns:
            List of image file paths found
        """
        if not folder_path.exists() or not folder_path.is_dir():
            logger.warning(f"Folder does not exist or is not a directory: {folder_path}")
            return []
        
        image_files = []
        for item in folder_path.iterdir():
            if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS:
                image_files.append(item)
        image_files.sort(key=lambda p: p.name.lower())
        
        logger.info(f"Found {len(image_files)} images in folder: {folder_path}")
        return image_files
    
    @classmethod
    def set_folder(cls, folder_path: str) -> int:
        """
        Set the folder to watch and load all images from it.
        
        Args:
            folder_path: Path to the folder
            
        Returns:
            Number of images successfully loaded
        """
        
        path = Path(folder_path)
        if not path.exists() or not path.is_dir():
            logger.error(f"Invalid folder path: {folder_path}")
            return 0
        
        # Ensure asset library is registered before adding assets
        SearchAssetManager.register_asset_library()
        
        cls.clear_local_assets()
        cls._watched_folder = path
        cls._known_files.clear()
        image_files = cls.scan_folder(path)
        success_count = 0
        cached_results = []
        
        for i, image_path in enumerate(image_files):
            result_info = cls._add_image_from_path(image_path, i)
            if result_info:
                success_count += 1
                cached_results.append(result_info)
                cls._known_files.add(str(image_path))
        cls._update_cached_results(cached_results)
        
        # Debug: log material assets created
        local_mats = [m for m in bpy.data.materials if m.name.startswith("local_")]
        local_assets = [m for m in local_mats if m.asset_data is not None]
        logger.info(f"Created {len(local_mats)} local materials, {len(local_assets)} marked as assets")
        
        SearchAssetManager.refresh_asset_browser()
        def delayed_refresh():
            try:
                SearchAssetManager.refresh_asset_browser()
            except Exception:
                pass
            return None  # Don't repeat
        
        bpy.app.timers.register(delayed_refresh, first_interval=0.5)
        cls._start_watcher()
        
        logger.info(f"Loaded {success_count} images from local folder: {folder_path}")
        return success_count
    
    @classmethod
    def _update_cached_results(cls, local_results: list):
        """
        Update the cached results to include local folder images.
        Merges with existing web search results.
        """
        try:
            scene = bpy.context.scene
            existing_results = scene.get("yandex_search_cached_results", [])
            web_results = [r for r in existing_results if not r.get("name", "").startswith("local_")]
            combined = web_results + local_results
            scene["yandex_search_cached_results"] = combined
            
            logger.info(f"Updated cached results: {len(web_results)} web + {len(local_results)} local")
        except Exception as e:
            logger.error(f"Failed to update cached results: {e}")
    
    @classmethod
    def _add_image_from_path(cls, image_path: Path, index: int) -> Optional[dict]:
        """
        Add an image from a file path as a material asset and preview.
        
        Args:
            image_path: Path to the image file
            index: Index for naming
            
        Returns:
            Dict with result info if successful, None otherwise
        """
        
        try:
            name = image_path.stem[:30]  # Limit length
            name = name.replace(" ", "_").replace("/", "_").replace("\\", "_")
            full_name = f"{index:03d}_{name}"
            asset = SearchAssetManager.add_local_image_asset(str(image_path), full_name)
            preview_name = f"local_{index:03d}"
            icon_id = load_image_preview(str(image_path), preview_name)
            
            if asset or icon_id:
                return {
                    "name": preview_name,
                    "title": name,
                    "url": "",  # No URL for local files
                    "filepath": str(image_path),
                    "icon_id": icon_id,
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to add image {image_path}: {e}")
            return None
    
    @classmethod
    def refresh_folder(cls) -> int:
        """
        Refresh the watched folder, adding any new images.
        
        Returns:
            Number of new images added
        """
        
        if cls._watched_folder is None:
            logger.warning("No folder is being watched")
            return 0
        
        if not cls._watched_folder.exists():
            logger.warning(f"Watched folder no longer exists: {cls._watched_folder}")
            return 0
        image_files = cls.scan_folder(cls._watched_folder)
        new_count = 0
        new_results = []
        current_index = len(cls._known_files)
        
        for image_path in image_files:
            path_str = str(image_path)
            if path_str not in cls._known_files:
                result_info = cls._add_image_from_path(image_path, current_index)
                if result_info:
                    new_count += 1
                    new_results.append(result_info)
                    cls._known_files.add(path_str)
                    current_index += 1
        
        if new_count > 0:
            cls._append_to_cached_results(new_results)
            SearchAssetManager.refresh_asset_browser()
            def delayed_refresh():
                try:
                    SearchAssetManager.refresh_asset_browser()
                except Exception:
                    pass
                return None
            
            bpy.app.timers.register(delayed_refresh, first_interval=0.5)
            logger.info(f"Added {new_count} new images from folder")
        
        return new_count
    
    @classmethod
    def _append_to_cached_results(cls, new_results: list):
        """Append new local results to the cached results."""
        try:
            scene = bpy.context.scene
            existing_results = scene.get("yandex_search_cached_results", [])
            combined = existing_results + new_results
            scene["yandex_search_cached_results"] = combined
        except Exception as e:
            logger.error(f"Failed to append to cached results: {e}")
    
    @classmethod
    def _folder_watcher(cls) -> Optional[float]:
        """
        Timer callback to detect new files in the watched folder.
        
        Returns:
            Interval to next check, or None to stop the timer
        """
        if cls._watched_folder is None:
            cls._watcher_running = False
            return None
        
        if not cls._watched_folder.exists():
            logger.warning(f"Watched folder was deleted: {cls._watched_folder}")
            cls._watcher_running = False
            return None
        
        try:
            new_files = []
            for item in cls._watched_folder.iterdir():
                if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS:
                    if str(item) not in cls._known_files:
                        new_files.append(item)
            
            if new_files:
                logger.info(f"Folder watcher detected {len(new_files)} new file(s)")
                cls.refresh_folder()
        except Exception as e:
            logger.debug(f"Folder watcher error: {e}")
        
        return 3.0  # Check every 3 seconds
    
    @classmethod
    def _start_watcher(cls):
        """Start the folder watcher timer if not already running."""
        if cls._watcher_running:
            return
        
        cls._watcher_running = True
        bpy.app.timers.register(cls._folder_watcher, first_interval=3.0, persistent=True)
        logger.info("Started local folder watcher")
    
    @classmethod
    def _stop_watcher(cls):
        """Stop the folder watcher timer."""
        if not cls._watcher_running:
            return
        
        try:
            bpy.app.timers.unregister(cls._folder_watcher)
        except Exception:
            pass
        
        cls._watcher_running = False
        logger.info("Stopped local folder watcher")
    
    @classmethod
    def clear_local_assets(cls):
        """Clear all local folder assets and stop watching."""
        cls._stop_watcher()
        try:
            pcoll = get_search_preview_collection()
            local_keys = [k for k in pcoll.keys() if k.startswith("local_")]
            for key in local_keys:
                try:
                    del pcoll[key]
                except Exception:
                    pass
        except Exception:
            pass
        try:
            scene = bpy.context.scene
            existing_results = scene.get("yandex_search_cached_results", [])
            web_results = [r for r in existing_results if not r.get("name", "").startswith("local_")]
            scene["yandex_search_cached_results"] = web_results
        except Exception:
            pass
        for mat_name in list(bpy.data.materials.keys()):
            if mat_name.startswith("local_"):
                try:
                    mat = bpy.data.materials[mat_name]
                    bpy.data.materials.remove(mat)
                except Exception:
                    pass
        for img_name in list(bpy.data.images.keys()):
            if img_name.startswith("local_"):
                try:
                    img = bpy.data.images[img_name]
                    bpy.data.images.remove(img)
                except Exception:
                    pass
        cls._watched_folder = None
        cls._known_files.clear()
        
        logger.info("Cleared all local folder assets")
    
    @classmethod
    def get_image_count(cls) -> int:
        """Get the number of currently loaded local images."""
        return len(cls._known_files)
    
    @classmethod
    def cleanup(cls):
        """Clean up resources on addon unload."""
        cls._stop_watcher()
        cls._watched_folder = None
        cls._known_files.clear()


def register():
    """Register the local folder manager."""
    pass  # No registration needed, class methods are used directly


def unregister():
    """Unregister and clean up."""
    LocalFolderManager.cleanup()
