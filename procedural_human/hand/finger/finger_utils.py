"""
Finger utility functions for Procedural Human Generator
"""

import bpy
from mathutils import Vector
from procedural_human.utils import get_numeric_value, create_geometry_nodes_modifier
from . import finger_nodes
from . import finger_proportions as proportions
from procedural_human.hand.finger.finger_types import (
    FingerType,
    ensure_finger_type,
)
from procedural_human.hand.finger.finger import FingerData


def realize_finger_geometry(finger_object):
    """
    Apply Geometry Nodes modifier to finger object to get final mesh

    Args:
        finger_object: Finger object with Geometry Nodes modifier

    Returns:
        finger_object with modifier applied
    """

    modifier = None
    for mod in finger_object.modifiers:
        if mod.type == "NODES":
            modifier = mod
            break

    if not modifier:
        raise RuntimeError("No Geometry Nodes modifier found on finger object")

    bpy.context.view_layer.objects.active = finger_object
    bpy.context.view_layer.update()

    depsgraph = bpy.context.evaluated_depsgraph_get()
    finger_eval = finger_object.evaluated_get(depsgraph)

    if not finger_eval.data or len(finger_eval.data.vertices) == 0:
        raise RuntimeError("Geometry Nodes modifier did not produce any geometry")

    finger_object.data = finger_eval.data.copy()

    finger_object.modifiers.remove(modifier)

    bpy.context.view_layer.update()
    return finger_object


def create_finger_geometry(
    finger_type=FingerType.INDEX,
    radius=0.007,
    nail_size=0.003,
    taper_factor=0.15,
    curl_direction="Y",
    total_length=1.0,
):
    """
    Create a standalone finger with variable segments and fingernail using Geometry Nodes

    Args:
        finger_type: One of "THUMB", "INDEX", "MIDDLE", "RING", "LITTLE"
        radius: Base finger radius
        nail_size: Fingernail size
        taper_factor: How much radius decreases per segment
        curl_direction: Curl direction axis ("X", "Y", or "Z")
        total_length: Total finger length in blender units (default 1.0)
        create_armature: Whether to create armature and bones
        create_animation: Whether to create keyframe animation
    """

    radius = get_numeric_value(radius, 0.007)
    nail_size = get_numeric_value(nail_size, 0.003)
    taper_factor = get_numeric_value(taper_factor, 0.15)
    total_length = get_numeric_value(total_length, 1.0)

    finger_enum = ensure_finger_type(finger_type)

    finger_data = proportions.get_finger_proportions(finger_enum)
    num_segments = finger_data["segments"]
    segment_lengths = proportions.get_segment_lengths_blender_units(
        finger_enum, total_length
    )

    mesh = bpy.data.meshes.new("FingerMesh")
    mesh.from_pydata([(0, 0, 0)], [], [])
    finger = bpy.data.objects.new("Finger", mesh)
    bpy.context.collection.objects.link(finger)

    modifier, node_group = create_geometry_nodes_modifier(finger, "FingerShape")

    try:
        finger_nodes.create_finger_nodes(
            node_group,
            num_segments=num_segments,
            segment_lengths=segment_lengths,
            radius=radius,
            nail_size=nail_size,
            taper_factor=taper_factor,
            curl_direction=curl_direction,
            finger_type=finger_enum,
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

    bpy.context.view_layer.objects.active = finger
    bpy.context.view_layer.update()

    depsgraph = bpy.context.evaluated_depsgraph_get()
    finger_eval = finger.evaluated_get(depsgraph)

    if not finger_eval.data:

        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        finger_eval = finger.evaluated_get(depsgraph)

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

    if curl_direction == "Y":
        axis_idx = 2
    elif curl_direction == "X":
        axis_idx = 2
    else:
        axis_idx = 1

    current_length = (
        max(bbox, key=lambda v: v[axis_idx])[axis_idx]
        - min(bbox, key=lambda v: v[axis_idx])[axis_idx]
    )
    if current_length > 0:
        scale_factor = 1.0 / current_length
        finger.scale = (scale_factor, scale_factor, scale_factor)

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
    armature.location = finger.location

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

    bpy.ops.object.mode_set(mode="OBJECT")

    armature_mod = finger.modifiers.new(name="Armature", type="ARMATURE")
    armature_mod.object = armature

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

    return ik_target
