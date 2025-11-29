"""
DSL utility functions for armature, weight painting, and IK setup.

These functions create armature bones and weight paint geometry
based on bone information extracted from DSL generation.
"""

from typing import Dict, List, Any, Optional
import math
from procedural_human.logger import *


def create_dsl_armature(obj: Any, bone_info: List[Dict], name_prefix: str = "") -> Any:
    """
    Create an armature with bones based on DSL generation bone info.
    
    Args:
        obj: The Blender mesh object to parent to the armature
        bone_info: List of bone dicts from GenerationResult.bones
            Each dict has: index, ik_limits, length, radius, parent_index, axis
        name_prefix: Optional prefix for bone names
        
    Returns:
        The created armature object
    """
    import bpy
    
    if not bone_info:
        return None
    
    arm_name = f"{obj.name}_Armature"
    armature = bpy.data.armatures.new(arm_name)
    arm_obj = bpy.data.objects.new(arm_name, armature)
    
    bpy.context.collection.objects.link(arm_obj)
    arm_obj.location = obj.location
    
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    z_offset = 0.0
    bones_created = {}
    
    for bone_data in sorted(bone_info, key=lambda x: x.get("index", 0)):
        idx = bone_data.get("index", 0)
        length = bone_data.get("length", 1.0)
        axis = bone_data.get("axis", "Z")
        parent_idx = bone_data.get("parent_index")
        
        bone_name = f"{name_prefix}Bone_{idx}" if name_prefix else f"Bone_{idx}"
        bone = armature.edit_bones.new(bone_name)
        
        bone.head = (0, 0, z_offset)
        bone.tail = (0, 0, z_offset + length)
        
        if parent_idx is not None and parent_idx in bones_created:
            parent_bone = armature.edit_bones.get(bones_created[parent_idx])
            if parent_bone:
                bone.parent = parent_bone
                bone.use_connect = True
        
        bones_created[idx] = bone_name
        z_offset += length
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    obj.parent = arm_obj
    modifier = obj.modifiers.new(name="Armature", type='ARMATURE')
    modifier.object = arm_obj
    
    return arm_obj


def setup_dsl_ik(arm_obj: Any, bone_info: List[Dict]) -> None:
    """
    Set up IK constraints on armature bones based on DSL IKLimits.
    
    Args:
        arm_obj: The armature object
        bone_info: List of bone dicts from GenerationResult.bones
    """
    import bpy
    
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return
    
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    
    for bone_data in bone_info:
        idx = bone_data.get("index", 0)
        ik_limits = bone_data.get("ik_limits")
        bone_name = f"Bone_{idx}"
        
        pose_bone = arm_obj.pose.bones.get(bone_name)
        if not pose_bone:
            continue
        
        if ik_limits and hasattr(ik_limits, 'to_radians'):
            limits_rad = ik_limits.to_radians()
            
            pose_bone.use_ik_limit_x = True
            pose_bone.use_ik_limit_y = True
            pose_bone.use_ik_limit_z = True
            
            pose_bone.ik_min_x = limits_rad['x'][0]
            pose_bone.ik_max_x = limits_rad['x'][1]
            pose_bone.ik_min_y = limits_rad['y'][0]
            pose_bone.ik_max_y = limits_rad['y'][1]
            pose_bone.ik_min_z = limits_rad['z'][0]
            pose_bone.ik_max_z = limits_rad['z'][1]
    
    bpy.ops.object.mode_set(mode='OBJECT')


def create_ik_target(arm_obj: Any, target_bone_name: str, chain_length: int = 3) -> Any:
    """
    Create an IK target empty and constraint for the armature.
    
    Args:
        arm_obj: The armature object
        target_bone_name: Name of the bone to apply IK to (usually last bone)
        chain_length: Number of bones in the IK chain
        
    Returns:
        The created IK target empty object
    """
    import bpy
    
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return None
    
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = arm_obj.pose.bones.get(target_bone_name)
    if not pose_bone:
        bpy.ops.object.mode_set(mode='OBJECT')
        return None
    
    target_name = f"{arm_obj.name}_IK_Target"
    target = bpy.data.objects.new(target_name, None)
    target.empty_display_type = 'SPHERE'
    target.empty_display_size = 0.1
    bpy.context.collection.objects.link(target)
    
    bone_tail_world = arm_obj.matrix_world @ pose_bone.tail
    target.location = bone_tail_world
    
    ik_constraint = pose_bone.constraints.new('IK')
    ik_constraint.target = target
    ik_constraint.chain_count = chain_length
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return target


def paint_dsl_weights(obj: Any, arm_obj: Any, bone_info: List[Dict]) -> None:
    """
    Paint vertex weights on the object based on bone positions.
    
    Creates vertex groups for each bone and assigns weights based on
    vertex proximity to bone segments.
    
    Args:
        obj: The mesh object to paint weights on
        arm_obj: The armature object
        bone_info: List of bone dicts from GenerationResult.bones
    """
    import bpy
    import bmesh
    
    if not obj or obj.type != 'MESH':
        return
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return
    
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    
    if not mesh:
        return
    
    z_positions = []
    z_offset = 0.0
    for bone_data in sorted(bone_info, key=lambda x: x.get("index", 0)):
        length = bone_data.get("length", 1.0)
        z_positions.append((z_offset, z_offset + length, bone_data.get("index", 0)))
        z_offset += length
    
    for bone_data in bone_info:
        idx = bone_data.get("index", 0)
        bone_name = f"Bone_{idx}"
        
        if bone_name not in obj.vertex_groups:
            obj.vertex_groups.new(name=bone_name)
    
    for vert in mesh.vertices:
        v_z = vert.co.z
        
        weights = []
        for z_start, z_end, idx in z_positions:
            bone_name = f"Bone_{idx}"
            
            if z_start <= v_z <= z_end:
                local_pos = (v_z - z_start) / (z_end - z_start) if z_end > z_start else 0.5
                weight = 1.0 - abs(local_pos - 0.5) * 0.5
                weights.append((bone_name, weight))
            elif v_z < z_start:
                dist = z_start - v_z
                if dist < 0.5:
                    weight = 1.0 - dist * 2
                    weights.append((bone_name, weight * 0.5))
            elif v_z > z_end:
                dist = v_z - z_end
                if dist < 0.5:
                    weight = 1.0 - dist * 2
                    weights.append((bone_name, weight * 0.5))
        
        if weights:
            total = sum(w for _, w in weights)
            for bone_name, weight in weights:
                vg = obj.vertex_groups.get(bone_name)
                if vg:
                    vg.add([vert.index], weight / total, 'REPLACE')
    
    eval_obj.to_mesh_clear()


def realize_dsl_geometry(obj: Any) -> bool:
    """
    Apply geometry nodes modifier to realize the procedural geometry.
    
    Args:
        obj: The mesh object with geometry nodes modifier
        
    Returns:
        True if successful, False otherwise
    """
    import bpy
    
    if not obj or obj.type != 'MESH':
        return False
    
    geo_mod = None
    for mod in obj.modifiers:
        if mod.type == 'NODES':
            geo_mod = mod
            break
    
    if not geo_mod:
        return False
    
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=geo_mod.name)
    
    return True


def get_bone_info_from_object(obj: Any) -> List[Dict]:
    """
    Extract bone info from a DSL-generated object's bones list.
    
    Looks for a 'bones' attribute containing Bone objects with
    geometry references and IK limits.
    
    Args:
        obj: The mesh object with DSL custom properties
        
    Returns:
        List of bone info dicts, or empty list if not available
    """
    source_file = obj.get("dsl_source_file", "")
    instance_name = obj.get("dsl_instance_name", "")
    
    logger.info(f"[Bone Debug] Getting bone info for: source={source_file}, instance={instance_name}")
    
    if not source_file or not instance_name:
        logger.info("[Bone Debug] Missing source_file or instance_name")
        return []
    
    from procedural_human.dsl.executor import execute_dsl_file
    
    result = execute_dsl_file(source_file)
    if instance_name not in result.instances:
        logger.info(f"[Bone Debug] Instance '{instance_name}' not in result.instances: {list(result.instances.keys())}")
        return []
    
    instance = result.instances[instance_name]
    logger.info(f"[Bone Debug] Found instance: {type(instance).__name__}")
    
    bones_list = getattr(instance, 'bones', None)
    
    if bones_list is None:
        logger.info(f"[Bone Debug] No 'bones' attribute found on instance")
        logger.info(f"[Bone Debug] Available attributes: {[a for a in dir(instance) if not a.startswith('__') and not callable(getattr(instance, a, None))]}")
        return []
    
    if not isinstance(bones_list, (list, tuple)):
        logger.info(f"[Bone Debug] 'bones' is not a list: {type(bones_list)}")
        return []
    
    logger.info(f"[Bone Debug] Found bones list with {len(bones_list)} items")
    
    from procedural_human.dsl.primitives import Bone
    
    bone_info_list = []
    for idx, bone in enumerate(bones_list):
        if not isinstance(bone, Bone):
            logger.info(f"[Bone Debug] Item {idx} is not a Bone: {type(bone)}")
            continue
        
        info = bone.get_bone_info(idx)
        logger.info(f"[Bone Debug] Bone {idx}: length={info['length']}, ik={info['ik_limits']}")
        bone_info_list.append(info)
    
    logger.info(f"[Bone Debug] Total bones extracted: {len(bone_info_list)}")
    return bone_info_list

