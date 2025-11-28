"""
Dynamic operators for DSL procedural generation.
"""

import os
from typing import Dict, List, Optional, Type, Any

try:
    import bpy
    from bpy.types import Operator
    from bpy.props import StringProperty
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    bpy = None
    Operator = object
    StringProperty = None

from procedural_human.dsl.executor import execute_dsl_file, get_dsl_instances
from procedural_human.dsl.generator import generate_from_dsl_file
from procedural_human.dsl.watcher import DSLFileWatcher, start_watching


_registered_operators: List[Type] = []
_dsl_instances_cache: Dict[str, List[str]] = {}


def get_dsl_files() -> List[str]:
    """Get all DSL definition files in the dsl directory."""
    dsl_dir = os.path.dirname(__file__)
    internal_modules = {
        '__init__.py', 'primitives.py', 'naming.py',
        'executor.py', 'generator.py', 'watcher.py', 
        'operators.py', 'panel.py'
    }
    
    dsl_files = []
    for filename in os.listdir(dsl_dir):
        if filename.endswith('.py') and filename not in internal_modules:
            dsl_files.append(os.path.join(dsl_dir, filename))
    
    return dsl_files


def scan_dsl_files() -> Dict[str, List[str]]:
    """Scan all DSL files and extract instance names."""
    global _dsl_instances_cache
    _dsl_instances_cache.clear()
    
    for file_path in get_dsl_files():
        try:
            instances = get_dsl_instances(file_path)
            _dsl_instances_cache[file_path] = instances
        except Exception as e:
            print(f"Error scanning DSL file {file_path}: {e}")
    
    return _dsl_instances_cache


def get_all_dsl_instances() -> List[tuple]:
    """Get all DSL instances from all files."""
    if not _dsl_instances_cache:
        scan_dsl_files()
    
    instances = []
    for file_path, instance_names in _dsl_instances_cache.items():
        for name in instance_names:
            instances.append((file_path, name))
    
    return instances


if BLENDER_AVAILABLE:
    
    class DSL_OT_CreateInstance(Operator):
        """Create a procedural object from DSL definition"""
        bl_idname = "dsl.create_instance"
        bl_label = "Create DSL Instance"
        bl_options = {'REGISTER', 'UNDO'}
        
        file_path: StringProperty(name="DSL File", default="")
        instance_name: StringProperty(name="Instance", default="")
        
        @classmethod
        def poll(cls, context):
            return context.area.type == 'VIEW_3D'
        
        def execute(self, context):
            if not self.file_path or not self.instance_name:
                self.report({'ERROR'}, "File path and instance name required")
                return {'CANCELLED'}
            
            try:
                generated = generate_from_dsl_file(
                    self.file_path, context, instance_filter=[self.instance_name])
                
                if generated:
                    obj = generated[0].blend_obj
                    context.view_layer.objects.active = obj
                    obj.select_set(True)
                    
                    watcher = DSLFileWatcher.get_instance()
                    watcher.watch_file(self.file_path, [obj.name])
                    
                    self.report({'INFO'}, f"Created {self.instance_name}")
                    return {'FINISHED'}
                else:
                    self.report({'ERROR'}, f"Failed to generate {self.instance_name}")
                    return {'CANCELLED'}
            except Exception as e:
                self.report({'ERROR'}, str(e))
                return {'CANCELLED'}
    
    
    class DSL_OT_RefreshFromSource(Operator):
        """Refresh object from its DSL source file"""
        bl_idname = "dsl.refresh_from_source"
        bl_label = "Refresh from DSL"
        bl_options = {'REGISTER', 'UNDO'}
        
        @classmethod
        def poll(cls, context):
            obj = context.active_object
            return obj is not None and obj.get("dsl_source_file", "") != ""
        
        def execute(self, context):
            obj = context.active_object
            source_file = obj.get("dsl_source_file", "")
            
            if not source_file:
                self.report({'ERROR'}, "Object has no DSL source file")
                return {'CANCELLED'}
            
            try:
                from procedural_human.dsl.generator import regenerate_dsl_object
                result = regenerate_dsl_object(obj)
                
                if result:
                    self.report({'INFO'}, f"Refreshed {obj.name}")
                    return {'FINISHED'}
                else:
                    self.report({'ERROR'}, "Failed to refresh object")
                    return {'CANCELLED'}
            except Exception as e:
                self.report({'ERROR'}, str(e))
                return {'CANCELLED'}
    
    
    class DSL_OT_OpenSourceFile(Operator):
        """Open the DSL source file in text editor"""
        bl_idname = "dsl.open_source_file"
        bl_label = "Open DSL Source"
        
        @classmethod
        def poll(cls, context):
            obj = context.active_object
            return obj is not None and obj.get("dsl_source_file", "") != ""
        
        def execute(self, context):
            obj = context.active_object
            source_file = obj.get("dsl_source_file", "")
            
            if not source_file or not os.path.exists(source_file):
                self.report({'ERROR'}, "Source file not found")
                return {'CANCELLED'}
            
            filename = os.path.basename(source_file)
            text = bpy.data.texts.get(filename)
            
            if not text:
                text = bpy.data.texts.load(source_file)
            
            for area in context.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    area.spaces.active.text = text
                    break
            
            self.report({'INFO'}, f"Loaded {filename}")
            return {'FINISHED'}
    
    
    class DSL_OT_ScanFiles(Operator):
        """Scan DSL directory for definition files"""
        bl_idname = "dsl.scan_files"
        bl_label = "Scan DSL Files"
        
        def execute(self, context):
            instances = scan_dsl_files()
            total = sum(len(v) for v in instances.values())
            self.report({'INFO'}, f"Found {len(instances)} DSL files with {total} instances")
            return {'FINISHED'}
    
    
    class DSL_OT_StartWatcher(Operator):
        """Start watching DSL files for changes"""
        bl_idname = "dsl.start_watcher"
        bl_label = "Start DSL Watcher"
        
        def execute(self, context):
            watcher = start_watching()
            self.report({'INFO'}, f"Watching {len(watcher.get_watched_files())} files")
            return {'FINISHED'}
    
    
    class DSL_OT_StopWatcher(Operator):
        """Stop watching DSL files"""
        bl_idname = "dsl.stop_watcher"
        bl_label = "Stop DSL Watcher"
        
        def execute(self, context):
            from procedural_human.dsl.watcher import stop_watching
            stop_watching()
            self.report({'INFO'}, "DSL watcher stopped")
            return {'FINISHED'}


_standard_classes = []

if BLENDER_AVAILABLE:
    _standard_classes = [
        DSL_OT_CreateInstance,
        DSL_OT_RefreshFromSource,
        DSL_OT_OpenSourceFile,
        DSL_OT_ScanFiles,
        DSL_OT_StartWatcher,
        DSL_OT_StopWatcher,
    ]


def register():
    """Register DSL operators."""
    if not BLENDER_AVAILABLE:
        return
    
    for cls in _standard_classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister DSL operators."""
    if not BLENDER_AVAILABLE:
        return
    
    for cls in reversed(_standard_classes):
        bpy.utils.unregister_class(cls)

