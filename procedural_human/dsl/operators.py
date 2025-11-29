"""
Dynamic operators for DSL procedural generation.
"""

import os
from typing import Dict, List, Optional, Type, Any

import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import *

_dsl_instances_cache: Dict[str, List[str]] = {}


def get_dsl_files() -> List[str]:
    """Get all DSL definition files - from registry first, then fallback to file scan."""
    from procedural_human.decorators.dsl_definition_decorator import (
        get_dsl_files as get_registered_files,
    )
    
    registered = get_registered_files()
    if registered:
        return registered
    
    dsl_dir = os.path.dirname(__file__)
    internal_modules = {
        '__init__.py', 'primitives.py', 'naming.py',
        'executor.py', 'generator.py', 'watcher.py', 
        'operators.py', 'panel.py', 'dsl_utils.py',
    }
    
    dsl_files = []
    for filename in os.listdir(dsl_dir):
        if filename.endswith('.py') and filename not in internal_modules:
            if not filename.endswith('_float_curve_presets.py'):
                dsl_files.append(os.path.join(dsl_dir, filename))
    
    return dsl_files


def scan_dsl_files() -> Dict[str, List[str]]:
    """Scan DSL files and extract instance names - uses registry when available."""
    global _dsl_instances_cache
    _dsl_instances_cache.clear()
    
    from procedural_human.decorators.dsl_definition_decorator import (
        scan_registered_dsl_files,
        get_all_dsl_definitions,
    )
    from procedural_human.dsl.executor import get_dsl_instances
    
    registry = get_all_dsl_definitions()
    if registry:
        _dsl_instances_cache = scan_registered_dsl_files()
        return _dsl_instances_cache
    
    for file_path in get_dsl_files():
        try:
            instances = get_dsl_instances(file_path)
            _dsl_instances_cache[file_path] = instances
        except Exception as e:
            logger.info(f"Error scanning DSL file {file_path}: {e}")
    
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


@procedural_operator
class DSLCreateInstance(Operator):
    """Create a procedural object from DSL definition"""
    
    file_path: StringProperty(
        name="File Path",
        description="Path to the DSL file",
        default="",
    )
    
    instance_name: StringProperty(
        name="Instance Name", 
        description="Name of the DSL instance to create",
        default="",
    )
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'
    
    def execute(self, context):
        if not self.file_path or not self.instance_name:
            self.report({'ERROR'}, "No DSL instance specified")
            return {'CANCELLED'}
        
        try:
            from procedural_human.dsl.generator import generate_from_dsl_file
            from procedural_human.dsl.watcher import DSLFileWatcher
            
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


@procedural_operator
class DSLRealizeGeometry(Operator):
    """Apply geometry nodes modifier to realize procedural geometry"""
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.get("dsl_source_file", "") != ""
    
    def execute(self, context):
        from procedural_human.dsl.dsl_utils import realize_dsl_geometry
        
        obj = context.active_object
        
        if realize_dsl_geometry(obj):
            self.report({'INFO'}, f"Realized geometry for {obj.name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to realize geometry")
            return {'CANCELLED'}


@procedural_operator
class DSLAddArmature(Operator):
    """Add armature and bones based on DSL definition"""
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.get("dsl_source_file", "") != ""
    
    def execute(self, context):
        from procedural_human.dsl.dsl_utils import (
            get_bone_info_from_object,
            create_dsl_armature,
            setup_dsl_ik,
            paint_dsl_weights,
            create_ik_target,
        )
        
        obj = context.active_object
        
        bone_info = get_bone_info_from_object(obj)
        if not bone_info:
            self.report({'ERROR'}, "No bone information found in DSL definition")
            return {'CANCELLED'}
        
        arm_obj = create_dsl_armature(obj, bone_info)
        if not arm_obj:
            self.report({'ERROR'}, "Failed to create armature")
            return {'CANCELLED'}
        
        setup_dsl_ik(arm_obj, bone_info)
        
        paint_dsl_weights(obj, arm_obj, bone_info)
        
        if bone_info:
            last_bone_idx = max(b.get("index", 0) for b in bone_info)
            last_bone_name = f"Bone_{last_bone_idx}"
            create_ik_target(arm_obj, last_bone_name, chain_length=len(bone_info))
        
        self.report({'INFO'}, f"Created armature with {len(bone_info)} bones")
        return {'FINISHED'}


@procedural_operator
class DSLRealizeAndAnimate(Operator):
    """Realize geometry, add armature, bones, weights, and IK in one step"""
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.get("dsl_source_file", "") != ""
    
    def execute(self, context):
        from procedural_human.dsl.dsl_utils import (
            realize_dsl_geometry,
            get_bone_info_from_object,
            create_dsl_armature,
            setup_dsl_ik,
            paint_dsl_weights,
            create_ik_target,
        )
        
        obj = context.active_object
        
        bone_info = get_bone_info_from_object(obj)
        if not bone_info:
            self.report({'ERROR'}, "No bone information found in DSL definition")
            return {'CANCELLED'}
        
        if not realize_dsl_geometry(obj):
            self.report({'ERROR'}, "Failed to realize geometry")
            return {'CANCELLED'}
        
        arm_obj = create_dsl_armature(obj, bone_info)
        if not arm_obj:
            self.report({'ERROR'}, "Failed to create armature")
            return {'CANCELLED'}
        
        setup_dsl_ik(arm_obj, bone_info)
        
        paint_dsl_weights(obj, arm_obj, bone_info)
        
        if bone_info:
            last_bone_idx = max(b.get("index", 0) for b in bone_info)
            last_bone_name = f"Bone_{last_bone_idx}"
            create_ik_target(arm_obj, last_bone_name, chain_length=len(bone_info))
        
        self.report({'INFO'}, f"Created animated object with {len(bone_info)} bones")
        return {'FINISHED'}
