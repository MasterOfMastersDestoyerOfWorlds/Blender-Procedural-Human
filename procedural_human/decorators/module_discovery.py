"""
Module discovery system for automatic import of decorated classes.

Scans the procedural_human directory recursively and imports all Python modules,
which triggers the decorators and populates the operator/panel registries.
"""

import os
import importlib
import sys
from pathlib import Path
from typing import Set
from procedural_human.logger import *

_discovered_modules: Set[str] = set()


def get_addon_root() -> Path:
    """Get the root path of the procedural_human addon."""
    return Path(__file__).parent.parent


def discover_modules(root_path: Path = None, package_name: str = "procedural_human") -> Set[str]:
    """
    Recursively discover all Python modules in the addon directory.
    
    Args:
        root_path: Root path to scan, defaults to procedural_human directory
        package_name: Base package name for import paths
    
    Returns:
        Set of discovered module names
    """
    if root_path is None:
        root_path = get_addon_root()
    
    modules = set()
    
    skip_dirs = {"__pycache__", ".git", "masonry"}
    skip_files = {"__init__.py"}
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs] 
        
        rel_path = Path(dirpath).relative_to(root_path)
        
        if rel_path == Path("."):
            current_package = package_name
        else:
            current_package = f"{package_name}.{'.'.join(rel_path.parts)}"
        
        for filename in filenames:
            if filename.endswith(".py") and filename not in skip_files:
                module_name = filename[:-3]
                full_module_name = f"{current_package}.{module_name}"
                modules.add(full_module_name)
    
    return modules


def import_all_modules() -> Set[str]:
    """
    Import all discovered modules to trigger decorators.
    
    Returns:
        Set of successfully imported module names
    """
    global _discovered_modules
    
    modules = discover_modules() 
    imported = set()
    
    logger.info(f"[Module Discovery] Found {len(modules)} modules to import")
    
    for module_name in sorted(modules):
        if module_name in _discovered_modules:
            continue
        
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)
            
            imported.add(module_name)
            _discovered_modules.add(module_name)
        except ModuleNotFoundError as e:
            missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
            logger.info(f"[Module Discovery] SKIPPED {module_name}: missing dependency '{missing_module}'")
            logger.info(f"    -> Install via addon preferences or run: pip install {missing_module}")
        except Exception as e:
            import traceback
            logger.info(f"[Module Discovery] ERROR importing {module_name}:")
            traceback.print_exc()
    
    logger.info(f"[Module Discovery] Successfully imported {len(imported)} new modules")
    return imported


def clear_discovered():
    """Clear the set of discovered modules (useful for reloading)."""
    _discovered_modules.clear() 

