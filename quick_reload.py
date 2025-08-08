"""
Quick Reload Script for Procedural Human Generator
Run this directly in Blender's scripting workspace to reload the addon
"""

import bpy
import sys
import importlib

def reload_procedural_human():
    """Reload the Procedural Human addon"""
    addon_name = "procedural_human"
    
    print("=" * 50)
    print("Reloading Procedural Human Generator...")
    print("=" * 50)
    
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
        print("SUCCESS: Addon reloaded successfully!")
        
        # Show success popup
        def show_message(self, context):
            self.layout.label(text="Procedural Human addon reloaded!")
        
        bpy.context.window_manager.popup_menu(show_message, title="Success", icon='INFO')
        
    except Exception as e:
        print(f"ERROR: Failed to enable addon: {e}")
        
        # Show error popup
        def show_error(self, context):
            self.layout.label(text=f"Error reloading addon: {str(e)}")
        
        bpy.context.window_manager.popup_menu(show_error, title="Error", icon='ERROR')
    
    print("=" * 50)

# Run the reload
reload_procedural_human()
