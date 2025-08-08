#!/usr/bin/env python3
"""
Auto-installer and reloader for Procedural Human Generator
Automatically installs/updates the addon in Blender and reloads it
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

def find_blender_addons_path():
    """Find the Blender addons directory"""
    # Common Blender addon paths
    possible_paths = [
        # Windows
        os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/4.5/scripts/addons"),
        os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/4.4/scripts/addons"),
        os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/4.3/scripts/addons"),
        os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/4.2/scripts/addons"),
        os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/4.1/scripts/addons"),
        os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/4.0/scripts/addons"),
        # macOS
        os.path.expanduser("~/Library/Application Support/Blender/4.5/scripts/addons"),
        os.path.expanduser("~/Library/Application Support/Blender/4.4/scripts/addons"),
        os.path.expanduser("~/Library/Application Support/Blender/4.3/scripts/addons"),
        # Linux
        os.path.expanduser("~/.config/blender/4.5/scripts/addons"),
        os.path.expanduser("~/.config/blender/4.4/scripts/addons"),
        os.path.expanduser("~/.config/blender/4.3/scripts/addons"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found Blender addons directory: {path}")
            return path
    
    print("Could not find Blender addons directory!")
    print("Please make sure Blender is installed and has been run at least once.")
    return None

def copy_addon_files(source_dir, target_dir):
    """Copy addon files to target directory"""
    # Remove existing addon if it exists
    if os.path.exists(target_dir):
        print(f"Removing existing addon at: {target_dir}")
        shutil.rmtree(target_dir)
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    print(f"Created addon directory: {target_dir}")
    
    # Copy all Python files
    files_to_copy = [
        "__init__.py",
        "advanced_nodes.py", 
        "operators.py",
        "panels.py",
        "menus.py",
        "utils.py"
    ]
    
    for filename in files_to_copy:
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            print(f"Copied {filename}")
        else:
            print(f"Warning: {filename} not found")

def create_reload_script():
    """Create a Python script that can be run inside Blender to reload the addon"""
    reload_script = '''
import bpy
import sys
import importlib

def reload_procedural_human():
    """Reload the Procedural Human addon"""
    addon_name = "procedural_human"
    
    # Disable addon if it's enabled
    if addon_name in bpy.context.preferences.addons:
        print(f"Disabling {addon_name}...")
        bpy.ops.preferences.addon_disable(module=addon_name)
    
    # Remove from sys.modules to force reload
    modules_to_remove = []
    for module_name in sys.modules:
        if module_name.startswith(addon_name):
            modules_to_remove.append(module_name)
    
    for module_name in modules_to_remove:
        print(f"Removing module: {module_name}")
        del sys.modules[module_name]
    
    # Re-enable addon
    try:
        print(f"Enabling {addon_name}...")
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("Addon reloaded successfully!")
        
        # Show success message
        def show_message(message="Procedural Human addon reloaded!", title="Success", icon='INFO'):
            def draw(self, context):
                self.layout.label(text=message)
            bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
        
        show_message()
        
    except Exception as e:
        print(f"Error enabling addon: {e}")
        
        # Show error message
        def show_error(message=f"Error reloading addon: {e}", title="Error", icon='ERROR'):
            def draw(self, context):
                self.layout.label(text=message)
            bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
        
        show_error()

# Run the reload
reload_procedural_human()
'''
    
    with open("reload_addon.py", "w", encoding='utf-8') as f:
        f.write(reload_script)
    
    print("Created reload_addon.py script")

def main():
    print("=" * 60)
    print("Procedural Human Generator - Auto Installer & Reloader")
    print("=" * 60)
    
    # Find source directory
    source_dir = "procedural_human"
    if not os.path.exists(source_dir):
        print(f"✗ Error: Source directory '{source_dir}' not found!")
        return False
    
    # Find Blender addons directory
    blender_addons_path = find_blender_addons_path()
    if not blender_addons_path:
        return False
    
    # Target directory
    target_dir = os.path.join(blender_addons_path, "procedural_human")
    
    # Copy files
    print("\\nCopying addon files...")
    copy_addon_files(source_dir, target_dir)
    
    # Create reload script
    print("\\nCreating reload script...")
    create_reload_script()
    
    print("\\n" + "=" * 60)
    print("Installation complete!")
    print("=" * 60)
    print("\\nTo reload the addon in Blender:")
    print("1. In Blender, go to Scripting workspace")
    print("2. Open the file 'reload_addon.py'")
    print("3. Click 'Run Script' or press Alt+P")
    print("\\nOr use the Text Editor:")
    print("1. Text > Open > select 'reload_addon.py'")
    print("2. Text > Run Script")
    print("\\nThe addon will be automatically reloaded without restarting Blender!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\\nInstallation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Don't wait for input in automated workflows
