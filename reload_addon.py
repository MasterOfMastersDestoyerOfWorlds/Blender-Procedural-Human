
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
