#!/usr/bin/env python3
"""
Simple installer for Procedural Human Generator
Just copies files to Blender's addon directory without user interaction
"""

import os
import shutil
import sys
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
        # macOS
        os.path.expanduser("~/Library/Application Support/Blender/4.5/scripts/addons"),
        os.path.expanduser("~/Library/Application Support/Blender/4.4/scripts/addons"),
        # Linux
        os.path.expanduser("~/.config/blender/4.5/scripts/addons"),
        os.path.expanduser("~/.config/blender/4.4/scripts/addons"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def copy_addon_files(source_dir, target_dir):
    """Copy addon files to target directory"""
    # Remove existing addon if it exists
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    
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
            print(f"✅ Copied {filename}")
        else:
            print(f"⚠️ Warning: {filename} not found")

def main():
    """Main installation function"""
    print("🔧 Installing Procedural Human Generator...")
    
    # Find source directory
    source_dir = "procedural_human"
    if not os.path.exists(source_dir):
        print(f"❌ Source directory '{source_dir}' not found!")
        return False
    
    # Find Blender addons directory
    blender_addons_path = find_blender_addons_path()
    if not blender_addons_path:
        print("❌ Could not find Blender addons directory!")
        print("Make sure Blender is installed and has been run at least once.")
        return False
    
    # Target directory
    target_dir = os.path.join(blender_addons_path, "procedural_human")
    
    print(f"📁 Installing to: {target_dir}")
    
    # Copy files
    copy_addon_files(source_dir, target_dir)
    
    print("✅ Installation complete!")
    print("")
    print("Next steps:")
    print("1. Open Blender")
    print("2. Go to Edit > Preferences > Add-ons")
    print("3. Search for 'Procedural Human'")
    print("4. Enable the addon")
    print("")
    print("OR run the auto_install_reload.py script in Blender's scripting workspace!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
