"""
DSL Browser panel UI.
"""

import os
from typing import List

try:
    import bpy
    from bpy.types import Panel, UIList, PropertyGroup
    from bpy.props import StringProperty, IntProperty, CollectionProperty
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    bpy = None
    Panel = object
    UIList = object
    PropertyGroup = object
    StringProperty = None
    IntProperty = None
    CollectionProperty = None

from procedural_human.dsl.operators import get_all_dsl_instances, scan_dsl_files
from procedural_human.dsl.watcher import DSLFileWatcher


if BLENDER_AVAILABLE:
    
    class DSLInstanceItem(PropertyGroup):
        """Property group for a DSL instance list item."""
        name: StringProperty(name="Name")
        file_path: StringProperty(name="File Path")
        definition: StringProperty(name="Definition")
    
    
    class DSL_UL_InstanceList(UIList):
        """UI list for DSL instances."""
        
        def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
            if self.layout_type in {'DEFAULT', 'COMPACT'}:
                row = layout.row(align=True)
                row.label(text=item.name, icon='OBJECT_DATA')
                row.label(text=item.definition, icon='FILE_SCRIPT')
            elif self.layout_type in {'GRID'}:
                layout.alignment = 'CENTER'
                layout.label(text=item.name, icon='OBJECT_DATA')
    
    
    class DSL_PT_Browser(Panel):
        """DSL Browser panel."""
        bl_label = "DSL Browser"
        bl_idname = "DSL_PT_browser"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Procedural Human'
        bl_options = {'DEFAULT_CLOSED'}
        
        def draw(self, context):
            layout = self.layout
            scene = context.scene
            
            watcher = DSLFileWatcher.get_instance()
            watched_count = len(watcher.get_watched_files())
            
            box = layout.box()
            row = box.row()
            row.label(text="File Watcher", icon='FILE_REFRESH')
            
            if watched_count > 0:
                row.label(text=f"Watching {watched_count} files")
                row.operator("dsl.stop_watcher", text="", icon='PAUSE')
            else:
                row.label(text="Not active")
                row.operator("dsl.start_watcher", text="", icon='PLAY')
            
            layout.operator("dsl.scan_files", icon='FILE_FOLDER')
            
            if hasattr(scene, 'dsl_instances'):
                layout.template_list(
                    "DSL_UL_InstanceList", "",
                    scene, "dsl_instances",
                    scene, "dsl_instance_index",
                    rows=5
                )
                
                if scene.dsl_instances and scene.dsl_instance_index < len(scene.dsl_instances):
                    item = scene.dsl_instances[scene.dsl_instance_index]
                    
                    row = layout.row(align=True)
                    op = row.operator("dsl.create_instance", text=f"Create {item.name}", icon='ADD')
                    op.file_path = item.file_path
                    op.instance_name = item.name
    
    
    class DSL_PT_ObjectInfo(Panel):
        """Panel showing DSL info for selected object."""
        bl_label = "DSL Object Info"
        bl_idname = "DSL_PT_object_info"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Procedural Human'
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
            row.operator("dsl.refresh_from_source", icon='FILE_REFRESH')
            row.operator("dsl.open_source_file", icon='TEXT')


_classes = []

if BLENDER_AVAILABLE:
    _classes = [
        DSLInstanceItem,
        DSL_UL_InstanceList,
        DSL_PT_Browser,
        DSL_PT_ObjectInfo,
    ]


def register():
    """Register DSL panel classes."""
    if not BLENDER_AVAILABLE:
        return
    
    for cls in _classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.dsl_instances = CollectionProperty(type=DSLInstanceItem)
    bpy.types.Scene.dsl_instance_index = IntProperty(name="DSL Instance Index", default=0)


def unregister():
    """Unregister DSL panel classes."""
    if not BLENDER_AVAILABLE:
        return
    
    del bpy.types.Scene.dsl_instances
    del bpy.types.Scene.dsl_instance_index
    
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)

