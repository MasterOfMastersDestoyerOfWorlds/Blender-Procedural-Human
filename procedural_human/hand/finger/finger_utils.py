"""
Finger utility functions for Procedural Human Generator
"""

import bpy
from mathutils import Vector
from procedural_human.utils import get_numeric_value, create_geometry_nodes_modifier, get_property_value
from . import finger_nodes
from . import finger_proportions as proportions
from procedural_human.hand.finger.finger_types import (
    FingerType,
    ensure_finger_type,
)
from procedural_human.hand.finger.finger import FingerData


def realize_finger_geometry(finger: FingerData):
    """
    Apply Geometry Nodes modifier to finger object to get final mesh

    Args:
        finger_object: Finger object with Geometry Nodes modifier

    Returns:
        finger_object with modifier applied
    """

    modifier = None
    for mod in finger.blend_obj.modifiers:
        if mod.type == "NODES":
            modifier = mod
            break

    if not modifier:
        raise RuntimeError("No Geometry Nodes modifier found on finger object")

    bpy.context.view_layer.objects.active = finger.blend_obj
    bpy.context.view_layer.update()

    depsgraph = bpy.context.evaluated_depsgraph_get()
    finger_eval = finger.blend_obj.evaluated_get(depsgraph)

    if not finger_eval.data or len(finger_eval.data.vertices) == 0:
        raise RuntimeError("Geometry Nodes modifier did not produce any geometry")

    finger.blend_obj.data = finger_eval.data.copy()

    finger.blend_obj.modifiers.remove(modifier)

    bpy.context.view_layer.update()
    finger.blend_obj.finger_data.is_realized = True
    return finger.blend_obj


def create_finger_geometry(
    finger: FingerData,
):
    """
    Create a standalone finger with variable segments and fingernail using Geometry Nodes

    Args:
        finger: Finger data
    """

    modifier, node_group = create_geometry_nodes_modifier(finger.blend_obj, "FingerShape")

    try:
        finger_nodes.create_finger_nodes(
            node_group,
            finger,
        )

        print(f"Node group created with {len(node_group.nodes)} nodes")
        print(f"Node group links: {len(node_group.links)}")

        output_nodes = [n for n in node_group.nodes if n.type == "GROUP_OUTPUT"]
        if output_nodes:
            output_node = output_nodes[0]
            if "Geometry" not in output_node.inputs:
                print(
                    f"Warning: Output node inputs: {[inp.name for inp in output_node.inputs]}"
                )
        else:
            print("Warning: No GROUP_OUTPUT node found in node group")

    except Exception as e:
        print(f"Error creating finger nodes: {e}")
        import traceback

        traceback.print_exc()
        raise RuntimeError(f"Failed to create finger Geometry Nodes: {e}") 

    bpy.context.view_layer.objects.active = finger.blend_obj
    bpy.context.view_layer.update()

    depsgraph = bpy.context.evaluated_depsgraph_get()
    finger_eval = finger.blend_obj.evaluated_get(depsgraph)

    if not finger_eval.data:

        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        finger_eval = finger.blend_obj.evaluated_get(depsgraph)

        if not finger_eval.data:

            print(f"Modifier: {modifier.name}, Type: {modifier.type}")
            print(f"Node group: {node_group.name}")
            print(f"Node group nodes: {len(node_group.nodes)}")
            raise RuntimeError(
                "Geometry Nodes modifier did not produce any geometry. Check node setup."
            )

    if len(finger_eval.data.vertices) == 0:
        raise RuntimeError(
            "Geometry Nodes modifier produced empty geometry (0 vertices). Check node connections."
        )

    bbox = [
        finger_eval.matrix_world @ Vector(corner) for corner in finger_eval.bound_box
    ]

    if finger.curl_direction == "Y":
        axis_idx = 2
    elif finger.curl_direction == "X":
        axis_idx = 2
    else:
        axis_idx = 1

    current_length = (
        max(bbox, key=lambda v: v[axis_idx])[axis_idx]
        - min(bbox, key=lambda v: v[axis_idx])[axis_idx]
    )
    if current_length > 0:
        scale_factor = 1.0 / current_length
        finger.blend_obj.scale = (scale_factor, scale_factor, scale_factor)

    bpy.context.view_layer.update()

    return finger


def create_finger_armature(finger: FingerData):
    """
    Create armature with bones for finger segments

    Args:
        finger: Finger mesh object
        num_segments: Number of segments
        segment_lengths: List of segment lengths
        curl_direction: Curl direction axis
    """

    armature_data = bpy.data.armatures.new("Finger_Armature")
    armature = bpy.data.objects.new("Finger_Armature", armature_data)
    bpy.context.collection.objects.link(armature)

    armature.parent = finger.blend_obj
    armature.location = finger.blend_obj.location

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="EDIT")

    if finger.curl_direction == "Y":
        bone_direction = Vector((0, 0, 1))
        bone_roll_axis = Vector((0, 1, 0))
    elif finger.curl_direction == "X":
        bone_direction = Vector((0, 0, 1))
        bone_roll_axis = Vector((1, 0, 0))
    else:
        bone_direction = Vector((0, 1, 0))
        bone_roll_axis = Vector((0, 0, 1))

    bones = []
    cumulative_length = 0.0

    for seg_idx in range(finger.num_segments):
        seg_length = finger.segment_lengths[seg_idx]
        bone_name = f"Finger_Segment_{seg_idx + 1}"

        bone = armature_data.edit_bones.new(bone_name)
        bone.head = bone_direction * cumulative_length
        bone.tail = bone_direction * (cumulative_length + seg_length)

        bone.roll = 0.0

        if seg_idx > 0:
            bone.parent = armature_data.edit_bones[f"Finger_Segment_{seg_idx}"]
            bone.use_connect = True

        bones.append(bone)
        cumulative_length += seg_length

    bpy.ops.object.mode_set(mode="OBJECT")

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    for seg_idx in range(finger.num_segments):
        bone_name = f"Finger_Segment_{seg_idx + 1}"
        if bone_name in armature.pose.bones:
            bone = armature.pose.bones[bone_name]
            bone.rotation_euler = (0.0, 0.0, 0.0)
            
            
            bone.use_ik_limit_x = True
            bone.use_ik_limit_y = True
            bone.use_ik_limit_z = True
            
            
            import math
            bone.ik_min_x = math.radians(-150)
            bone.ik_max_x = math.radians(10)
            
            bone.ik_min_y = math.radians(-10)
            bone.ik_max_y = math.radians(10)
            
            bone.ik_min_z = math.radians(-5)
            bone.ik_max_z = math.radians(5)

    bpy.ops.object.mode_set(mode="OBJECT")

    armature_mod = finger.blend_obj.modifiers.new(name="Armature", type="ARMATURE")
    armature_mod.object = armature

    finger.blend_obj.finger_data.has_armature = True
    return armature


def paint_finger_weights(finger: FingerData):
    """
    Paint weights for finger segments with smooth joint falloff

    Args:
        finger: Finger mesh object
        num_segments: Number of segments
        segment_lengths: List of segment lengths
    """

    bpy.context.view_layer.objects.active = finger.blend_obj
    bpy.ops.object.mode_set(mode="OBJECT")

    vertex_groups = []
    for seg_idx in range(finger.num_segments):
        vg_name = f"Finger_Segment_{seg_idx + 1}"
        vg: bpy.types.VertexGroup = finger.blend_obj.vertex_groups.new(name=vg_name)
        vertex_groups.append(vg)

    mesh: bpy.types.Mesh = finger.blend_obj.data
    cumulative_length = 0.0

    for vert_idx, vert in enumerate(mesh.vertices):

        vert_z = vert.co.z

        current_length = 0.0
        weights = [0.0] * finger.num_segments

        for seg_idx in range(finger.num_segments):
            seg_length = finger.segment_lengths[seg_idx]
            seg_start = current_length
            seg_end = current_length + seg_length
            seg_center = (seg_start + seg_end) / 2

            dist_from_center = abs(vert_z - seg_center)
            max_dist = seg_length / 2

            if dist_from_center <= max_dist:

                weight = 1.0 - (dist_from_center / max_dist) * 0.5
            elif seg_idx < finger.num_segments - 1 and vert_z > seg_end:

                next_seg_start = seg_end
                blend_dist = seg_length * 0.1
                if vert_z < next_seg_start + blend_dist:
                    weight = 1.0 - (vert_z - seg_end) / blend_dist
                else:
                    weight = 0.0
            else:
                weight = 0.0

            weights[seg_idx] = max(0.0, min(1.0, weight))
            current_length = seg_end

        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:

            nearest_seg = min(
                range(finger.num_segments),
                key=lambda i: abs(
                    vert_z
                    - (sum(finger.segment_lengths[:i]) + finger.segment_lengths[i] / 2)
                ),
            )
            weights[nearest_seg] = 1.0

        for seg_idx, weight in enumerate(weights):
            if weight > 0.001:
                vertex_groups[seg_idx].add([vert_idx], weight, "REPLACE")

    finger.blend_obj.finger_data.has_weights = True

def setup_finger_ik(armature, finger: FingerData):
    """
    Setup Inverse Kinematics for finger

    Args:
        armature: Armature object
        num_segments: Number of segments
        segment_lengths: List of segment lengths
    """

    tip_bone_name = f"Finger_Segment_{finger.num_segments}"

    bpy.ops.object.empty_add(
        type="PLAIN_AXES", location=(0, 0, sum(finger.segment_lengths))
    )
    ik_target = bpy.context.object
    ik_target.name = "Finger_IK_Target"
    ik_target.parent = armature.parent

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    tip_bone = armature.pose.bones[tip_bone_name]

    ik_constraint = tip_bone.constraints.new(type="IK")
    ik_constraint.target = ik_target
    ik_constraint.chain_count = finger.num_segments
    ik_constraint.iterations = 20

    bpy.ops.object.mode_set(mode="OBJECT")
    if ik_target:
        armature["finger_ik_target"] = ik_target.name
    armature["finger_segment_lengths"] = list(finger.segment_lengths)
    finger.blend_obj.finger_data.has_ik = True
    return ik_target
