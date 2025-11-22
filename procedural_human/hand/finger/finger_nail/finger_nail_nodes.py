"""
Geometry Node helpers for fingernail creation and attachment.
"""

import bpy

from procedural_human.hand.finger.finger_nail import NAIL_SAMPLE_COUNT
from procedural_human.utils import setup_node_group_interface
from procedural_human.hand.finger.finger_nail.finger_nail_proportions import (
    get_fingernail_proportions,
)
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_types import (
    ensure_finger_type,
)

DEFAULT_NAIL_SIZE = 0.003
OFFSET_RATIO = 0.1
THICKNESS_RATIO = 0.25


def create_fingernail_node_group(
    name,
    curl_direction,
    distal_seg_radius,
    nail_width_ratio,
    nail_height_ratio,
):
    """
    Create a reusable node group for a fingernail.
    Uses Raycast to attach precisely to the mesh surface.
    """
    nail_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(nail_group)

    
    radius_socket = nail_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    radius_socket.default_value = distal_seg_radius
    

    width_socket = nail_group.interface.new_socket(
        name="Nail Width Ratio", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    width_socket.default_value = nail_width_ratio

    height_socket = nail_group.interface.new_socket(
        name="Nail Height Ratio", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    height_socket.default_value = nail_height_ratio

    
    input_node = nail_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-1400, 0)

    output_node = nail_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (1000, 0)

    
    
    
    
    
    if curl_direction == "X":
        length_axis_vec = (0, 0, 1) 
        curl_axis_vec = (1, 0, 0)   
        side_axis_vec = (0, 1, 0)   
        length_idx, curl_idx, side_idx = 2, 0, 1
    elif curl_direction == "Y":
        length_axis_vec = (0, 0, 1) 
        curl_axis_vec = (0, 1, 0)   
        side_axis_vec = (1, 0, 0)   
        length_idx, curl_idx, side_idx = 2, 1, 0
    else:  
        length_axis_vec = (0, 1, 0) 
        curl_axis_vec = (0, 0, 1)   
        side_axis_vec = (1, 0, 0)   
        length_idx, curl_idx, side_idx = 1, 2, 0

    
    bounding_box = nail_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.location = (-1200, 200)
    nail_group.links.new(input_node.outputs["Geometry"], bounding_box.inputs["Geometry"])
    
    sep_bbox = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    sep_bbox.location = (-1000, 200)
    nail_group.links.new(bounding_box.outputs["Max"], sep_bbox.inputs["Vector"])
    
    
    
    
    
    
    
    
    
    
    
    length_pos = nail_group.nodes.new("ShaderNodeMath")
    length_pos.operation = "MULTIPLY" 
    
    
    
    
    
    width_calc = nail_group.nodes.new("ShaderNodeMath")
    width_calc.operation = "MULTIPLY"
    width_calc.location = (-1000, -200)
    nail_group.links.new(input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value], width_calc.inputs[0])
    nail_group.links.new(input_node.outputs["Nail Width Ratio"], width_calc.inputs[1])
    
    height_calc = nail_group.nodes.new("ShaderNodeMath")
    height_calc.operation = "MULTIPLY"
    height_calc.location = (-800, -200)
    nail_group.links.new(width_calc.outputs["Value"], height_calc.inputs[0])
    nail_group.links.new(input_node.outputs["Nail Height Ratio"], height_calc.inputs[1])
    
    
    tip_pos_val = sep_bbox.outputs["Z"] if length_idx == 2 else (sep_bbox.outputs["Y"] if length_idx == 1 else sep_bbox.outputs["X"])
    
    target_length_pos = nail_group.nodes.new("ShaderNodeMath")
    target_length_pos.operation = "SUBTRACT"
    target_length_pos.location = (-600, 100)
    nail_group.links.new(tip_pos_val, target_length_pos.inputs[0])
    
    half_height = nail_group.nodes.new("ShaderNodeMath")
    half_height.operation = "MULTIPLY"
    half_height.inputs[1].default_value = 0.5
    half_height.location = (-600, -100)
    nail_group.links.new(height_calc.outputs["Value"], half_height.inputs[0])
    
    nail_group.links.new(half_height.outputs["Value"], target_length_pos.inputs[1])
    
    
    
    
    
    base_pos_combine = nail_group.nodes.new("ShaderNodeCombineXYZ")
    base_pos_combine.location = (-400, 100)
    if length_idx == 0: nail_group.links.new(target_length_pos.outputs["Value"], base_pos_combine.inputs["X"])
    elif length_idx == 1: nail_group.links.new(target_length_pos.outputs["Value"], base_pos_combine.inputs["Y"])
    elif length_idx == 2: nail_group.links.new(target_length_pos.outputs["Value"], base_pos_combine.inputs["Z"])
    
    
    offset_dist = nail_group.nodes.new("ShaderNodeMath")
    offset_dist.operation = "MULTIPLY"
    offset_dist.inputs[1].default_value = 2.0
    nail_group.links.new(input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value], offset_dist.inputs[0])
    
    offset_vec = nail_group.nodes.new("ShaderNodeCombineXYZ")
    offset_vec.inputs[0].default_value = curl_axis_vec[0]
    offset_vec.inputs[1].default_value = curl_axis_vec[1]
    offset_vec.inputs[2].default_value = curl_axis_vec[2]
    
    offset_scaled = nail_group.nodes.new("ShaderNodeVectorMath")
    offset_scaled.operation = "SCALE"
    nail_group.links.new(offset_vec.outputs["Vector"], offset_scaled.inputs[0])
    nail_group.links.new(offset_dist.outputs["Value"], offset_scaled.inputs[3]) 
    
    ray_start = nail_group.nodes.new("ShaderNodeVectorMath")
    ray_start.operation = "ADD"
    nail_group.links.new(base_pos_combine.outputs["Vector"], ray_start.inputs[0])
    nail_group.links.new(offset_scaled.outputs["Vector"], ray_start.inputs[1])
    
    
    ray_dir = nail_group.nodes.new("ShaderNodeVectorMath")
    ray_dir.operation = "SCALE"
    ray_dir.inputs[0].default_value = curl_axis_vec
    ray_dir.inputs[3].default_value = -1.0
    
    
    raycast = nail_group.nodes.new("GeometryNodeRaycast")
    raycast.location = (0, 0)
    nail_group.links.new(input_node.outputs["Geometry"], raycast.inputs["Target Geometry"])
    nail_group.links.new(ray_start.outputs["Vector"], raycast.inputs["Source Position"])
    nail_group.links.new(ray_dir.outputs["Vector"], raycast.inputs["Ray Direction"])
    
    
    
    
    
    nail_sphere = nail_group.nodes.new("GeometryNodeMeshUVSphere")
    nail_sphere.location = (-400, -500)
    nail_sphere.inputs["Radius"].default_value = 1.0
    nail_sphere.inputs["Segments"].default_value = NAIL_SAMPLE_COUNT
    
    
    
    
    
    thickness_calc = nail_group.nodes.new("ShaderNodeMath")
    thickness_calc.operation = "MULTIPLY"
    thickness_calc.inputs[1].default_value = THICKNESS_RATIO
    nail_group.links.new(width_calc.outputs["Value"], thickness_calc.inputs[0])
    
    scale_vec = nail_group.nodes.new("ShaderNodeCombineXYZ")
    
    
    
    
    
    
    
    
    inputs = [None, None, None]
    inputs[curl_idx] = thickness_calc.outputs["Value"]
    inputs[side_idx] = width_calc.outputs["Value"]
    inputs[length_idx] = height_calc.outputs["Value"]
    
    nail_group.links.new(inputs[0], scale_vec.inputs["X"])
    nail_group.links.new(inputs[1], scale_vec.inputs["Y"])
    nail_group.links.new(inputs[2], scale_vec.inputs["Z"])
    
    transform_shape = nail_group.nodes.new("GeometryNodeTransform")
    transform_shape.location = (-200, -500)
    nail_group.links.new(nail_sphere.outputs["Mesh"], transform_shape.inputs["Geometry"])
    nail_group.links.new(scale_vec.outputs["Vector"], transform_shape.inputs["Scale"])
    
    
    
    final_pos = nail_group.nodes.new("GeometryNodeSetPosition")
    final_pos.location = (300, -300)
    nail_group.links.new(transform_shape.outputs["Geometry"], final_pos.inputs["Geometry"])
    
    
    
    
    
    
    
    
    offset_out_val = nail_group.nodes.new("ShaderNodeMath")
    offset_out_val.operation = "MULTIPLY"
    offset_out_val.inputs[1].default_value = OFFSET_RATIO * 0.1 
    nail_group.links.new(input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value], offset_out_val.inputs[0])
    
    offset_out_vec = nail_group.nodes.new("ShaderNodeVectorMath")
    offset_out_vec.operation = "SCALE"
    offset_out_vec.inputs[0].default_value = curl_axis_vec
    nail_group.links.new(offset_out_val.outputs["Value"], offset_out_vec.inputs[3])
    
    final_loc = nail_group.nodes.new("ShaderNodeVectorMath")
    final_loc.operation = "ADD"
    nail_group.links.new(raycast.outputs["Hit Position"], final_loc.inputs[0])
    nail_group.links.new(offset_out_vec.outputs["Vector"], final_loc.inputs[1])
    
    
    switch_loc = nail_group.nodes.new("ShaderNodeMix")
    switch_loc.data_type = "VECTOR"
    nail_group.links.new(raycast.outputs["Is Hit"], switch_loc.inputs["Factor"])
    
    
    
    
    fallback_loc = nail_group.nodes.new("ShaderNodeVectorMath")
    fallback_loc.operation = "ADD"
    nail_group.links.new(base_pos_combine.outputs["Vector"], fallback_loc.inputs[0])
    
    fallback_offset = nail_group.nodes.new("ShaderNodeVectorMath")
    fallback_offset.operation = "SCALE"
    fallback_offset.inputs[0].default_value = curl_axis_vec
    
    rad_1_1 = nail_group.nodes.new("ShaderNodeMath")
    rad_1_1.operation = "MULTIPLY"
    rad_1_1.inputs[1].default_value = 1.1
    nail_group.links.new(input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value], rad_1_1.inputs[0])
    nail_group.links.new(rad_1_1.outputs["Value"], fallback_offset.inputs[3])
    
    nail_group.links.new(fallback_offset.outputs["Vector"], fallback_loc.inputs[1])
    
    nail_group.links.new(fallback_loc.outputs["Vector"], switch_loc.inputs[4]) 
    nail_group.links.new(final_loc.outputs["Vector"], switch_loc.inputs[5]) 
    
    nail_group.links.new(switch_loc.outputs["Result"], final_pos.inputs["Offset"])
    
    
    join_geo = nail_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.location = (800, 0)
    nail_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
    nail_group.links.new(final_pos.outputs["Geometry"], join_geo.inputs["Geometry"])
    
    nail_group.links.new(join_geo.outputs["Geometry"], output_node.inputs["Geometry"])

    return nail_group


def attach_fingernail_to_distal_segment(
    node_group,
    distal_transform_node,
    curl_direction,
    distal_seg_radius,
    finger_type,
    nail_size=DEFAULT_NAIL_SIZE,
):
    """
    Build and attach a fingernail node group for the distal segment.
    """
    finger_enum = ensure_finger_type(finger_type)
    nail_props = get_fingernail_proportions(finger_enum)

    
    size_multiplier = 1.0
    if nail_size and nail_size > 0:
        size_multiplier = max(0.25, min(2.5, nail_size / DEFAULT_NAIL_SIZE))

    width_ratio = max(0.05, nail_props["width_ratio"] * size_multiplier)
    height_ratio = max(0.5, nail_props["height_ratio"])

    nail_group = create_fingernail_node_group(
        f"{finger_enum.value}_Fingernail",
        curl_direction,
        distal_seg_radius,
        width_ratio,
        height_ratio,
    )

    nail_instance = node_group.nodes.new("GeometryNodeGroup")
    nail_instance.node_tree = nail_group
    nail_instance.label = f"{finger_enum.label} Nail"
    nail_instance.location = (
        distal_transform_node.location[0] + 200.0,
        distal_transform_node.location[1],
    )

    
    if FingerSegmentProperties.SEGMENT_RADIUS.value in nail_instance.inputs:
        nail_instance.inputs[
            FingerSegmentProperties.SEGMENT_RADIUS.value
        ].default_value = distal_seg_radius
    if "Nail Width Ratio" in nail_instance.inputs:
        nail_instance.inputs["Nail Width Ratio"].default_value = width_ratio
    if "Nail Height Ratio" in nail_instance.inputs:
        nail_instance.inputs["Nail Height Ratio"].default_value = height_ratio

    if FingerSegmentProperties.SEGMENT_RADIUS.value in distal_transform_node.outputs:
        node_group.links.new(
            distal_transform_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
            nail_instance.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        )
    node_group.links.new(
        distal_transform_node.outputs["Geometry"], nail_instance.inputs["Geometry"]
    )
    return nail_instance

