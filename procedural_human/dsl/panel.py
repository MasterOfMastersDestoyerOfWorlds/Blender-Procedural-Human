"""
DSL Browser panel UI.
"""

import os
import bpy
from bpy.types import Panel

from procedural_human.decorators.panel_decorator import procedural_panel


def _get_dsl_instances_cache():
    """Lazy import to avoid circular dependencies."""
    from procedural_human.dsl.operators import _dsl_instances_cache
    return _dsl_instances_cache


def _get_watcher():
    """Lazy import to avoid circular dependencies."""
    from procedural_human.dsl.watcher import DSLFileWatcher
    return DSLFileWatcher.get_instance()


@procedural_panel
class DSLBrowserPanel(Panel):
    """DSL Browser panel for creating procedural objects from DSL definitions"""
    
    bl_label = "DSL Browser"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        watcher = _get_watcher()
        watched_count = len(watcher.get_watched_files())
        
        box = layout.box()
        row = box.row()
        row.label(text="File Watcher", icon='FILE_REFRESH')
        
        if watched_count > 0:
            row.label(text=f"Watching {watched_count} files")
            row.operator("mesh.procedural_dsl_stop_watcher", text="", icon='PAUSE')
        else:
            row.label(text="Not active")
            row.operator("mesh.procedural_dsl_start_watcher", text="", icon='PLAY')
        
        layout.operator("mesh.procedural_dsl_scan_files", icon='FILE_FOLDER')
        
        layout.separator()
        
        cache = _get_dsl_instances_cache()
        if cache:
            for file_path, instance_names in cache.items():
                file_name = os.path.basename(file_path).replace('.py', '').title()
                box = layout.box()
                box.label(text=file_name, icon='FILE_SCRIPT')
                
                col = box.column(align=True)
                for name in instance_names:
                    col.label(text=f"  • {name}", icon='OBJECT_DATA')
        else:
            layout.label(text="No DSL files scanned yet", icon='INFO')
        
        layout.separator()
        layout.operator("mesh.procedural_dsl_create_instance", icon='ADD')


@procedural_panel
class DSLObjectInfoPanel(Panel):
    """Panel showing DSL info for selected object"""
    
    bl_label = "DSL Object Info"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.get("dsl_source_file", "") != ""
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        source_file = obj.get("dsl_source_file", "")
        instance_name = obj.get("dsl_instance_name", "")
        definition_name = obj.get("dsl_definition_name", "")
        
        box = layout.box()
        box.label(text="DSL Source", icon='FILE_SCRIPT')
        
        col = box.column(align=True)
        col.label(text=f"Instance: {instance_name}")
        col.label(text=f"Definition: {definition_name}")
        col.label(text=f"File: {os.path.basename(source_file)}")
        
        row = layout.row(align=True)
        row.operator("mesh.procedural_dsl_refresh_from_source", icon='FILE_REFRESH')
        row.operator("mesh.procedural_dsl_open_source_file", icon='TEXT')
