"""
Geometry Node helpers for fingernail creation and attachment.
"""

import bpy

from procedural_human.blender_const import NODE_WIDTH
from procedural_human.dsl.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.utils import setup_node_group_interface
from procedural_human.utils.node_layout import auto_layout_nodes


DEFAULT_NAIL_SIZE = 0.003
OFFSET_RATIO = 0.1
THICKNESS_RATIO = 0.25


def create_fingernail_node_group(
    name,
    curl_direction,
    nail_width_ratio,
    nail_height_ratio,
    attachment_position=0.8,
):
    """
    Create a reusable node group for a fingernail.
    Uses Raycast to attach precisely to the mesh surface.
    Segment radius is determined automatically via raycast on input geometry
    at the specified attachment position along the segment.
    """
    nail_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(nail_group)

    width_socket = nail_group.interface.new_socket(
        name="Nail Width Ratio", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    width_socket.default_value = nail_width_ratio

    height_socket = nail_group.interface.new_socket(
        name="Nail Height Ratio", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    height_socket.default_value = nail_height_ratio

    attach_pos_socket = nail_group.interface.new_socket(
        name="Attachment Position", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    attach_pos_socket.default_value = attachment_position
    attach_pos_socket.min_value = 0.0
    attach_pos_socket.max_value = 1.0

    input_node = nail_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"

    output_node = nail_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"

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

    # Get bounding box of input geometry
    bounding_box = nail_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.label = "Segment Bounds"
    nail_group.links.new(
        input_node.outputs["Geometry"], bounding_box.inputs["Geometry"]
    )

    sep_bbox = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    sep_bbox.label = "Max XYZ"
    nail_group.links.new(bounding_box.outputs["Max"], sep_bbox.inputs["Vector"])

    sep_bbox_min = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    sep_bbox_min.label = "Min XYZ"
    nail_group.links.new(bounding_box.outputs["Min"], sep_bbox_min.inputs["Vector"])

    # === Calculate sample Z position based on Attachment Position ===
    # segment_length = max_z - min_z
    seg_length = nail_group.nodes.new("ShaderNodeMath")
    seg_length.label = "Segment Length"
    seg_length.operation = "SUBTRACT"
    nail_group.links.new(sep_bbox.outputs["Z"], seg_length.inputs[0])
    nail_group.links.new(sep_bbox_min.outputs["Z"], seg_length.inputs[1])

    # sample_z = min_z + (length * attachment_position)
    sample_z = nail_group.nodes.new("ShaderNodeMath")
    sample_z.label = "Sample Z"
    sample_z.operation = "MULTIPLY_ADD"
    nail_group.links.new(seg_length.outputs["Value"], sample_z.inputs[0])
    nail_group.links.new(input_node.outputs["Attachment Position"], sample_z.inputs[1])
    nail_group.links.new(sep_bbox_min.outputs["Z"], sample_z.inputs[2])

    # === Raycast to measure segment radius at sample position ===
    # Create ray origin at sample Z, offset far in X direction
    radius_ray_origin = nail_group.nodes.new("ShaderNodeCombineXYZ")
    radius_ray_origin.label = "Radius Ray Origin"
    radius_ray_origin.inputs["X"].default_value = 100.0
    radius_ray_origin.inputs["Y"].default_value = 0.0
    # Link sample Z position to ray origin Z
    nail_group.links.new(sample_z.outputs["Value"], radius_ray_origin.inputs["Z"])

    # Raycast toward center to find segment surface
    radius_raycast = nail_group.nodes.new("GeometryNodeRaycast")
    radius_raycast.label = "Measure Radius"
    radius_raycast.inputs["Ray Direction"].default_value = (-1.0, 0.0, 0.0)
    radius_raycast.inputs["Ray Length"].default_value = 200.0
    nail_group.links.new(
        input_node.outputs["Geometry"], radius_raycast.inputs["Target Geometry"]
    )
    nail_group.links.new(
        radius_ray_origin.outputs["Vector"], radius_raycast.inputs["Source Position"]
    )

    # Extract radius from hit X coordinate (absolute value)
    radius_hit_sep = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    radius_hit_sep.label = "Hit Position"
    nail_group.links.new(
        radius_raycast.outputs["Hit Position"], radius_hit_sep.inputs["Vector"]
    )

    segment_radius = nail_group.nodes.new("ShaderNodeMath")
    segment_radius.label = "Segment Radius"
    segment_radius.operation = "ABSOLUTE"
    nail_group.links.new(radius_hit_sep.outputs["X"], segment_radius.inputs[0])

    length_pos = nail_group.nodes.new("ShaderNodeMath")
    length_pos.operation = "MULTIPLY"

    width_calc = nail_group.nodes.new("ShaderNodeMath")
    width_calc.label = "Nail Width"
    width_calc.operation = "MULTIPLY"
    nail_group.links.new(
        segment_radius.outputs["Value"],
        width_calc.inputs[0],
    )
    nail_group.links.new(input_node.outputs["Nail Width Ratio"], width_calc.inputs[1])

    height_calc = nail_group.nodes.new("ShaderNodeMath")
    height_calc.label = "Nail Height"
    height_calc.operation = "MULTIPLY"
    nail_group.links.new(width_calc.outputs["Value"], height_calc.inputs[0])
    nail_group.links.new(input_node.outputs["Nail Height Ratio"], height_calc.inputs[1])

    # Use sample_z position for nail placement (not tip/max Z)
    # sample_z is calculated based on Attachment Position input
    target_length_pos = nail_group.nodes.new("ShaderNodeMath")
    target_length_pos.label = "Target Length Pos"
    target_length_pos.operation = "SUBTRACT"
    nail_group.links.new(sample_z.outputs["Value"], target_length_pos.inputs[0])

    half_height = nail_group.nodes.new("ShaderNodeMath")
    half_height.label = "Half Height"
    half_height.operation = "MULTIPLY"
    half_height.inputs[1].default_value = 0.5
    nail_group.links.new(height_calc.outputs["Value"], half_height.inputs[0])

    nail_group.links.new(half_height.outputs["Value"], target_length_pos.inputs[1])

    base_pos_combine = nail_group.nodes.new("ShaderNodeCombineXYZ")
    base_pos_combine.label = "Base Position"
    if length_idx == 0:
        nail_group.links.new(
            target_length_pos.outputs["Value"], base_pos_combine.inputs["X"]
        )
    elif length_idx == 1:
        nail_group.links.new(
            target_length_pos.outputs["Value"], base_pos_combine.inputs["Y"]
        )
    elif length_idx == 2:
        nail_group.links.new(
            target_length_pos.outputs["Value"], base_pos_combine.inputs["Z"]
        )

    offset_dist = nail_group.nodes.new("ShaderNodeMath")
    offset_dist.operation = "MULTIPLY"
    offset_dist.inputs[1].default_value = 2.0
    nail_group.links.new(
        segment_radius.outputs["Value"],
        offset_dist.inputs[0],
    )

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
    raycast.label = "Surface Raycast"
    nail_group.links.new(
        input_node.outputs["Geometry"], raycast.inputs["Target Geometry"]
    )
    nail_group.links.new(ray_start.outputs["Vector"], raycast.inputs["Source Position"])
    nail_group.links.new(ray_dir.outputs["Vector"], raycast.inputs["Ray Direction"])

    nail_sphere = nail_group.nodes.new("GeometryNodeMeshUVSphere")
    nail_sphere.label = "Nail Sphere"
    nail_sphere.inputs["Radius"].default_value = 1.0
    nail_sphere.inputs["Segments"].default_value = SEGMENT_SAMPLE_COUNT

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
    transform_shape.label = "Scale Nail"
    nail_group.links.new(
        nail_sphere.outputs["Mesh"], transform_shape.inputs["Geometry"]
    )
    nail_group.links.new(scale_vec.outputs["Vector"], transform_shape.inputs["Scale"])

    final_pos = nail_group.nodes.new("GeometryNodeSetPosition")
    final_pos.label = "Position Nail"
    nail_group.links.new(
        transform_shape.outputs["Geometry"], final_pos.inputs["Geometry"]
    )

    offset_out_val = nail_group.nodes.new("ShaderNodeMath")
    offset_out_val.operation = "MULTIPLY"
    offset_out_val.inputs[1].default_value = OFFSET_RATIO * 0.1
    nail_group.links.new(
        segment_radius.outputs["Value"],
        offset_out_val.inputs[0],
    )

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
    nail_group.links.new(
        segment_radius.outputs["Value"],
        rad_1_1.inputs[0],
    )
    nail_group.links.new(rad_1_1.outputs["Value"], fallback_offset.inputs[3])

    nail_group.links.new(fallback_offset.outputs["Vector"], fallback_loc.inputs[1])

    nail_group.links.new(fallback_loc.outputs["Vector"], switch_loc.inputs[4])
    nail_group.links.new(final_loc.outputs["Vector"], switch_loc.inputs[5])

    nail_group.links.new(switch_loc.outputs["Result"], final_pos.inputs["Offset"])

    join_geo = nail_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.label = "Join Geometry"
    nail_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
    nail_group.links.new(final_pos.outputs["Geometry"], join_geo.inputs["Geometry"])

    nail_group.links.new(join_geo.outputs["Geometry"], output_node.inputs["Geometry"])

    # Auto-layout all nodes based on their connections
    auto_layout_nodes(nail_group)

    return nail_group