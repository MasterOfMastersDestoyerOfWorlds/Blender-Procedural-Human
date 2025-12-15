"""
File watcher for DSL auto-update.
"""

import os
import hashlib
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
import bpy
from procedural_human.logger import *


@dataclass
class WatchedFile:
    """Information about a watched DSL file."""

    path: str
    last_hash: str
    last_modified: float
    linked_objects: List[str] = field(default_factory=list)

    def needs_update(self) -> bool:
        """Check if file has been modified since last check."""
        if not os.path.exists(self.path):
            return False

        current_modified = os.path.getmtime(self.path)
        if current_modified > self.last_modified:
            current_hash = self._compute_hash()
            if current_hash != self.last_hash:
                return True
        return False

    def _compute_hash(self) -> str:
        """Compute hash of file contents."""
        try:
            with open(self.path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def update_state(self) -> None:
        """Update last modified time and hash."""
        if os.path.exists(self.path):
            self.last_modified = os.path.getmtime(self.path)
            self.last_hash = self._compute_hash()


class DSLFileWatcher:
    """Watches DSL files for changes and triggers updates."""

    _instance: Optional["DSLFileWatcher"] = None

    def __init__(self):
        self._watched_files: Dict[str, WatchedFile] = {}
        self._timer_running: bool = False
        self._check_interval: float = 1.0
        self._on_change_callbacks: List[Callable] = []

    @classmethod
    def get_instance(cls) -> "DSLFileWatcher":
        """Get singleton instance of the watcher."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def watch_file(
        self, file_path: str, linked_objects: Optional[List[str]] = None
    ) -> None:
        """Start watching a DSL file."""
        abs_path = os.path.abspath(file_path)

        if abs_path in self._watched_files:
            if linked_objects:
                self._watched_files[abs_path].linked_objects.extend(linked_objects)
        else:
            watched = WatchedFile(
                path=abs_path,
                last_hash="",
                last_modified=0,
                linked_objects=linked_objects or [],
            )
            watched.update_state()
            self._watched_files[abs_path] = watched

    def unwatch_file(self, file_path: str) -> None:
        """Stop watching a DSL file."""
        abs_path = os.path.abspath(file_path)
        if abs_path in self._watched_files:
            del self._watched_files[abs_path]

    def add_callback(self, callback: Callable[[str, List[str]], None]) -> None:
        """Add a callback for file change events."""
        if callback not in self._on_change_callbacks:
            self._on_change_callbacks.append(callback)

    def check_files(self) -> List[str]:
        """Check all watched files for changes."""
        changed = []

        for path, watched in self._watched_files.items():
            if watched.needs_update():
                watched.update_state()
                changed.append(path)

                for callback in self._on_change_callbacks:
                    try:
                        callback(path, watched.linked_objects)
                    except Exception as e:
                        logger.info(f"DSL watcher callback error: {e}")

        return changed

    def start_timer(self, interval: float = 1.0) -> None:
        """Start periodic file checking using Blender's timer."""
        if self._timer_running:
            return

        self._check_interval = interval
        self._timer_running = True
        bpy.app.timers.register(self._timer_callback, first_interval=interval)

    def stop_timer(self) -> None:
        """Stop the periodic file checking timer."""
        self._timer_running = False
        try:
            bpy.app.timers.unregister(self._timer_callback)
        except Exception:
            pass

    def _timer_callback(self) -> Optional[float]:
        """Timer callback for periodic file checking."""
        if not self._timer_running:
            return None
        self.check_files()
        return self._check_interval

    def get_watched_files(self) -> Dict[str, WatchedFile]:
        """Get all watched files."""
        return self._watched_files.copy()


def on_dsl_file_changed(file_path: str, linked_objects: List[str]) -> None:
    """Default callback for DSL file changes."""

    from procedural_human.dsl.generator import regenerate_dsl_object

    logger.info(f"DSL file changed: {file_path}")

    for obj_name in linked_objects:
        if obj_name in bpy.data.objects:
            obj = bpy.data.objects[obj_name]
            regenerate_dsl_object(obj)
            logger.info(f"Regenerated: {obj_name}")


def start_watching(dsl_directory: Optional[str] = None) -> DSLFileWatcher:
    """Start watching DSL files in a directory."""
    watcher = DSLFileWatcher.get_instance()

    if dsl_directory is None:
        dsl_directory = os.path.dirname(__file__)

    internal_modules = {
        "__init__.py",
        "primitives.py",
        "naming.py",
        "executor.py",
        "generator.py",
        "watcher.py",
        "operators.py",
        "panel.py",
    }

    for filename in os.listdir(dsl_directory):
        if filename.endswith(".py") and filename not in internal_modules:
            file_path = os.path.join(dsl_directory, filename)
            watcher.watch_file(file_path)

    watcher.add_callback(on_dsl_file_changed)
    watcher.start_timer()

    return watcher


def stop_watching() -> None:
    """Stop watching DSL files."""
    watcher = DSLFileWatcher.get_instance()
    watcher.stop_timer()
