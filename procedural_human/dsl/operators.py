"""
Dynamic operators for DSL procedural generation.
"""

import os
from typing import Dict, List, Optional, Type, Any

import bpy
from bpy.types import Operator

from procedural_human.decorators.operator_decorator import procedural_operator


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
    
    from procedural_human.dsl.executor import get_dsl_instances
    
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


def get_dsl_instance_enum_items(self, context):
    """Get enum items for DSL instances."""
    if not _dsl_instances_cache:
        scan_dsl_files()
    
    items = []
    for file_path, instance_names in _dsl_instances_cache.items():
        file_name = os.path.basename(file_path).replace('.py', '')
        for name in instance_names:
            identifier = f"{file_path}|{name}"
            items.append((identifier, f"{name} ({file_name})", f"Create {name} from {file_name}.py"))
    
    if not items:
        items.append(("NONE", "No DSL instances found", "Scan for DSL files first"))
    
    return items


@procedural_operator
class DSLCreateInstance(Operator):
    """Create a procedural object from DSL definition"""
    
    dsl_instance: bpy.props.EnumProperty(
        name="DSL Instance",
        description="Select DSL instance to create",
        items=get_dsl_instance_enum_items,
    )
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'
    
    def invoke(self, context, event):
        scan_dsl_files()
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        if self.dsl_instance == "NONE" or "|" not in self.dsl_instance:
            self.report({'ERROR'}, "No valid DSL instance selected")
            return {'CANCELLED'}
        
        file_path, instance_name = self.dsl_instance.split("|", 1)
        
        try:
            from procedural_human.dsl.generator import generate_from_dsl_file
            from procedural_human.dsl.watcher import DSLFileWatcher
            
            generated = generate_from_dsl_file(
                file_path, context, instance_filter=[instance_name])
            
            if generated:
                obj = generated[0].blend_obj
                context.view_layer.objects.active = obj
                obj.select_set(True)
                
                watcher = DSLFileWatcher.get_instance()
                watcher.watch_file(file_path, [obj.name])
                
                self.report({'INFO'}, f"Created {instance_name}")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Failed to generate {instance_name}")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}


@procedural_operator
class DSLRefreshFromSource(Operator):
    """Refresh object from its DSL source file"""
    
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


@procedural_operator
class DSLOpenSourceFile(Operator):
    """Open the DSL source file in text editor"""
    
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


@procedural_operator
class DSLScanFiles(Operator):
    """Scan DSL directory for definition files"""
    
    def execute(self, context):
        instances = scan_dsl_files()
        total = sum(len(v) for v in instances.values())
        self.report({'INFO'}, f"Found {len(instances)} DSL files with {total} instances")
        return {'FINISHED'}


@procedural_operator
class DSLStartWatcher(Operator):
    """Start watching DSL files for changes"""
    
    def execute(self, context):
        from procedural_human.dsl.watcher import start_watching
        watcher = start_watching()
        self.report({'INFO'}, f"Watching {len(watcher.get_watched_files())} files")
        return {'FINISHED'}


@procedural_operator
class DSLStopWatcher(Operator):
    """Stop watching DSL files"""
    
    def execute(self, context):
        from procedural_human.dsl.watcher import stop_watching
        stop_watching()
        self.report({'INFO'}, "DSL watcher stopped")
        return {'FINISHED'}
