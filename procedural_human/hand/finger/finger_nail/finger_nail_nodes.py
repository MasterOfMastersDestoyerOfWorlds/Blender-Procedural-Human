"""
Geometry Node helpers for fingernail creation and attachment.
"""

import bpy

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
    """
    nail_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(nail_group)

    # Add proportion sockets so they are visible in the node interface.
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

    # Input/Output nodes (expects distal segment geometry as input)
    input_node = nail_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-900, 0)

    output_node = nail_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (1000, 0)

    # Get bounding box of distal segment
    bounding_box = nail_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.label = "Distal Bounds"
    bounding_box.location = (-700, 0)

    separate_bbox_max = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_bbox_max.label = "Get Max XYZ"
    separate_bbox_max.location = (-500, 0)

    # Create nail sphere
    nail_sphere = nail_group.nodes.new("GeometryNodeMeshUVSphere")
    nail_sphere.label = "Nail Sphere"
    nail_sphere.location = (-700, -300)
    nail_sphere.inputs["Radius"].default_value = 1.0
    nail_sphere.inputs["Segments"].default_value = 16
    nail_sphere.inputs["Rings"].default_value = 8

    # Determine axis mapping
    if curl_direction == "X":
        length_axis = 2  # Z
        curl_axis = 0  # X
        side_axis = 1  # Y
    elif curl_direction == "Y":
        length_axis = 2  # Z
        curl_axis = 1  # Y
        side_axis = 0  # X
    else:  # Z
        length_axis = 1  # Y
        curl_axis = 2  # Z
        side_axis = 0  # X

    axis_inputs = {
        0: None,
        1: None,
        2: None,
    }

    # Build scale values based on proportions
    width_value = nail_group.nodes.new("ShaderNodeMath")
    width_value.label = "Width = Radius * Ratio"
    width_value.location = (-700, -500)
    width_value.operation = "MULTIPLY"
    nail_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        width_value.inputs[0],
    )
    nail_group.links.new(input_node.outputs["Nail Width Ratio"], width_value.inputs[1])

    height_value = nail_group.nodes.new("ShaderNodeMath")
    height_value.label = "Height From Width"
    height_value.location = (-500, -420)
    height_value.operation = "MULTIPLY"
    nail_group.links.new(width_value.outputs["Value"], height_value.inputs[0])
    nail_group.links.new(
        input_node.outputs["Nail Height Ratio"], height_value.inputs[1]
    )

    thickness_value = nail_group.nodes.new("ShaderNodeMath")
    thickness_value.label = "Thickness From Width"
    thickness_value.location = (-500, -540)
    thickness_value.operation = "MULTIPLY"
    thickness_value.inputs[1].default_value = THICKNESS_RATIO
    nail_group.links.new(width_value.outputs["Value"], thickness_value.inputs[0])

    combine_scale = nail_group.nodes.new("ShaderNodeCombineXYZ")
    combine_scale.label = "Scale Nail Dimensions"
    combine_scale.location = (-300, -300)
    axis_inputs[0] = combine_scale.inputs["X"]
    axis_inputs[1] = combine_scale.inputs["Y"]
    axis_inputs[2] = combine_scale.inputs["Z"]

    nail_group.links.new(width_value.outputs["Value"], axis_inputs[side_axis])
    nail_group.links.new(height_value.outputs["Value"], axis_inputs[length_axis])
    nail_group.links.new(thickness_value.outputs["Value"], axis_inputs[curl_axis])

    flatten_nail = nail_group.nodes.new("GeometryNodeTransform")
    flatten_nail.label = "Shape Nail"
    flatten_nail.location = (-100, -300)
    flatten_nail.inputs["Rotation"].default_value = (0.0, 0.0, 0.0)
    nail_group.links.new(combine_scale.outputs["Vector"], flatten_nail.inputs["Scale"])
    nail_group.links.new(nail_sphere.outputs["Mesh"], flatten_nail.inputs["Geometry"])

    # Calculate nail position (at tip of distal segment, centered, on opposite side of curl)
    length_max_output = (
        separate_bbox_max.outputs["X"]
        if length_axis == 0
        else (
            separate_bbox_max.outputs["Y"]
            if length_axis == 1
            else separate_bbox_max.outputs["Z"]
        )
    )

    curl_max_output = (
        separate_bbox_max.outputs["X"]
        if curl_axis == 0
        else (
            separate_bbox_max.outputs["Y"]
            if curl_axis == 1
            else separate_bbox_max.outputs["Z"]
        )
    )

    surface_offset = nail_group.nodes.new("ShaderNodeMath")
    surface_offset.label = "Surface Offset"
    surface_offset.location = (-300, -120)
    surface_offset.operation = "MULTIPLY"
    surface_offset.inputs[1].default_value = OFFSET_RATIO
    nail_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        surface_offset.inputs[0],
    )

    math_offset_curl = nail_group.nodes.new("ShaderNodeMath")
    math_offset_curl.label = "Offset From Surface"
    math_offset_curl.location = (-100, -120)
    math_offset_curl.operation = "ADD"

    combine_pos = nail_group.nodes.new("ShaderNodeCombineXYZ")
    combine_pos.label = "Nail Position"
    combine_pos.location = (100, -200)

    pos_axis_inputs = {
        0: combine_pos.inputs["X"],
        1: combine_pos.inputs["Y"],
        2: combine_pos.inputs["Z"],
    }

    nail_group.links.new(length_max_output, pos_axis_inputs[length_axis])
    pos_axis_inputs[side_axis].default_value = 0.0
    nail_group.links.new(curl_max_output, math_offset_curl.inputs[0])
    nail_group.links.new(surface_offset.outputs["Value"], math_offset_curl.inputs[1])
    nail_group.links.new(math_offset_curl.outputs["Value"], pos_axis_inputs[curl_axis])

    # Position nail
    position_nail = nail_group.nodes.new("GeometryNodeTransform")
    position_nail.label = "Place on Distal"
    position_nail.location = (300, -300)
    nail_group.links.new(
        flatten_nail.outputs["Geometry"], position_nail.inputs["Geometry"]
    )
    nail_group.links.new(
        combine_pos.outputs["Vector"], position_nail.inputs["Translation"]
    )

    # Join distal segment + nail
    join_nail = nail_group.nodes.new("GeometryNodeJoinGeometry")
    join_nail.label = "Join Distal + Nail"
    join_nail.location = (600, 0)
    nail_group.links.new(
        input_node.outputs["Geometry"], bounding_box.inputs["Geometry"]
    )
    nail_group.links.new(
        bounding_box.outputs["Max"], separate_bbox_max.inputs["Vector"]
    )
    nail_group.links.new(input_node.outputs["Geometry"], join_nail.inputs["Geometry"])
    nail_group.links.new(
        position_nail.outputs["Geometry"], join_nail.inputs["Geometry"]
    )
    nail_group.links.new(join_nail.outputs["Geometry"], output_node.inputs["Geometry"])

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

    # Interpret nail_size as a proportional scale relative to the default value.
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

    # Ensure exposed sockets reflect the proportions on this instance.
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


__all__ = [
    "attach_fingernail_to_distal_segment",
    "create_fingernail_node_group",
]
