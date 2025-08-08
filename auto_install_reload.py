"""
Auto Install & Reload Script for Procedural Human Generator
Run this script directly in Blender's scripting workspace to:
1. Copy latest files to Blender's addon directory
2. Reload the addon without restarting Blender
"""

import bpy
import sys
import os
import shutil
import importlib
from pathlib import Path

def get_project_root():
    """Find the project root directory"""
    # Try to find based on current script location
    script_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    
    # Look for procedural_human directory
    for path in [script_dir, script_dir.parent, script_dir.parent.parent]:
        if (path / "procedural_human").exists():
            return path
    
    # Fallback: ask user or use current directory
    return Path.cwd()

def find_blender_addons_path():
    """Find the Blender addons directory"""
    # Get from Blender's user preferences
    import addon_utils
    user_path = bpy.utils.user_resource('SCRIPTS', "addons")
    return Path(user_path) if user_path else None

def copy_addon_files():
    """Copy addon files to Blender's addons directory"""
    project_root = get_project_root()
    source_dir = project_root / "procedural_human"
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return False
    
    addons_path = find_blender_addons_path()
    if not addons_path:
        print("❌ Could not find Blender addons directory")
        return False
    
    target_dir = addons_path / "procedural_human"
    
    print(f"📁 Copying from: {source_dir}")
    print(f"📁 Copying to: {target_dir}")
    
    # Remove existing addon if it exists
    if target_dir.exists():
        print("🗑️ Removing existing addon...")
        shutil.rmtree(target_dir)
    
    # Create target directory
    target_dir.mkdir(exist_ok=True)
    
    # Copy all Python files
    files_copied = 0
    for file_path in source_dir.glob("*.py"):
        if file_path.is_file():
            target_file = target_dir / file_path.name
            shutil.copy2(file_path, target_file)
            print(f"✅ Copied {file_path.name}")
            files_copied += 1
    
    if files_copied == 0:
        print("❌ No Python files found to copy")
        return False
    
    print(f"✅ Successfully copied {files_copied} files")
    return True

def reload_addon():
    """Reload the Procedural Human addon"""
    addon_name = "procedural_human"
    
    print("🔄 Reloading addon...")
    
    # Disable addon if it's enabled
    if addon_name in bpy.context.preferences.addons:
        print(f"⏸️ Disabling {addon_name}...")
        bpy.ops.preferences.addon_disable(module=addon_name)
    
    # Remove from sys.modules to force reload
    modules_to_remove = []
    for module_name in sys.modules:
        if module_name.startswith(addon_name):
            modules_to_remove.append(module_name)
    
    for module_name in modules_to_remove:
        print(f"🗑️ Removing module: {module_name}")
        del sys.modules[module_name]
    
    # Re-enable addon
    try:
        print(f"▶️ Enabling {addon_name}...")
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("✅ Addon reloaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error enabling addon: {e}")
        return False

def show_result_popup(success, message):
    """Show a popup with the result"""
    def draw(self, context):
        layout = self.layout
        lines = message.split('\\n')
        for line in lines:
            layout.label(text=line)
    
    icon = 'INFO' if success else 'ERROR'
    title = "Success" if success else "Error"
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def main():
    """Main function to install and reload"""
    print("=" * 60)
    print("🔧 Auto Install & Reload - Procedural Human Generator")
    print("=" * 60)
    
    # Step 1: Copy files
    if not copy_addon_files():
        show_result_popup(False, "Failed to copy addon files!\\nCheck the console for details.")
        return False
    
    # Step 2: Reload addon
    if not reload_addon():
        show_result_popup(False, "Failed to reload addon!\\nCheck the console for details.")
        return False
    
    # Success!
    show_result_popup(True, "✅ Addon installed and reloaded successfully!\\n\\nYou can now use the Procedural Human Generator\\nin the 3D Viewport sidebar (N key) under 'Procedural' tab.")
    
    print("=" * 60)
    print("🎉 Installation and reload complete!")
    print("=" * 60)
    return True

# Run the main function
if __name__ == "__main__":
    main()
else:
    # When run from Blender's script editor
    main()
