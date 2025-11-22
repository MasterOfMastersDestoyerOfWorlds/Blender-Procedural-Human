"""
Addon preferences for Procedural Human Generator
"""

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from pathlib import Path


class ProceduralHumanPreferences(AddonPreferences):
    """Preferences for the Procedural Human Generator addon"""
    
    bl_idname = "procedural_human"
    
    codebase_path: StringProperty(
        name="Codebase Path",
        description="Path to the Procedural Human development codebase (for exporting modifications)",
        default="",
        subtype='DIR_PATH',
    )
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Development Settings:", icon='SETTINGS')
        
        box = layout.box()
        box.label(text="Codebase Path Configuration:")
        box.prop(self, "codebase_path")
        
        
        from .config import detect_codebase_path, get_codebase_path, validate_codebase_path
        
        detected = detect_codebase_path()
        current = get_codebase_path()
        
        info_box = layout.box()
        info_box.label(text="Path Detection Info:", icon='INFO')
        
        if detected:
            row = info_box.row()
            row.label(text=f"Auto-Detected: {detected}")
            if validate_codebase_path(detected):
                row.label(text="", icon='CHECKMARK')
            else:
                row.label(text="(Invalid)", icon='ERROR')
        else:
            info_box.label(text="Auto-Detected: None", icon='ERROR')
        
        if current:
            row = info_box.row()
            row.label(text=f"Current: {current}")
            if validate_codebase_path(current):
                row.label(text="", icon='CHECKMARK')
            else:
                row.label(text="(Invalid)", icon='ERROR')
        else:
            info_box.label(text="Current: None (configure above)", icon='ERROR')
        
        
        row = layout.row()
        row.operator("wm.procedural_refresh_codebase_path", text="Refresh Detection", icon='FILE_REFRESH')
        
        
        help_box = layout.box()
        help_box.label(text="Help:", icon='QUESTION')
        help_box.label(text="• Auto-detection walks up from addon location to find project root")
        help_box.label(text="• Looks for .git, pyproject.toml, or uv.lock markers")
        help_box.label(text="• Set manual path above if auto-detection fails")
        help_box.label(text="• Path is used when exporting profile curves to source code")


class RefreshCodebasePath(bpy.types.Operator):
    """Refresh codebase path detection"""
    bl_idname = "wm.procedural_refresh_codebase_path"
    bl_label = "Refresh Codebase Path"
    bl_description = "Re-detect the codebase path"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        from .config import clear_cache, get_codebase_path
        
        clear_cache()
        new_path = get_codebase_path()
        
        if new_path:
            self.report({'INFO'}, f"Detected codebase at: {new_path}")
        else:
            self.report({'WARNING'}, "Could not auto-detect codebase path. Please set manually.")
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ProceduralHumanPreferences)
    bpy.utils.register_class(RefreshCodebasePath)


def unregister():
    bpy.utils.unregister_class(RefreshCodebasePath)
    bpy.utils.unregister_class(ProceduralHumanPreferences)

