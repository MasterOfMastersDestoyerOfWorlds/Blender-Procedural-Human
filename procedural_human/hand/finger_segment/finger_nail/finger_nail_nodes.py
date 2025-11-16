"""
Geometry Node helpers for fingernail creation and attachment.
"""

import bpy

from procedural_human.utils import setup_node_group_interface
from ..finger_types import ensure_finger_type

def create_fingernail_node_group(name, nail_radius, curl_direction, distal_seg_radius):
    """
    Create a reusable node group for a fingernail
    
    Args:
        name: Name for the node group
        nail_radius: Radius of the nail
        curl_direction: Curl direction axis ("X", "Y", or "Z")
        distal_seg_radius: Radius of the distal segment (for positioning)
    
    Returns:
        Node group for the fingernail
    """
    # Create node group
    nail_group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    setup_node_group_interface(nail_group)
    
    # Input/Output nodes (expects distal segment geometry as input)
    input_node = nail_group.nodes.new("NodeGroupInput")
    input_node.label = "Distal Segment Input"
    input_node.location = (-800, 0)
    
    output_node = nail_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (1000, 0)
    
    # Get bounding box of distal segment
    bounding_box = nail_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.label = "Distal Bounds"
    bounding_box.location = (-600, 0)
    
    separate_bbox_max = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_bbox_max.label = "Get Max XYZ"
    separate_bbox_max.location = (-400, 0)
    
    # Create nail sphere
    nail_sphere = nail_group.nodes.new("GeometryNodeMeshUVSphere")
    nail_sphere.label = "Nail Sphere"
    nail_sphere.location = (-600, -300)
    nail_sphere.inputs["Radius"].default_value = nail_radius
    nail_sphere.inputs["Segments"].default_value = 16
    nail_sphere.inputs["Rings"].default_value = 8
    
    # Determine scale based on curl direction
    scale = [1.5, 1.0, 1.0]
    if curl_direction == "Y":
        scale = [1.5, 0.3, 1.0]  # X=wide, Y=thin (curl), Z=normal (length)
    elif curl_direction == "X":
        scale = [0.3, 1.5, 1.0]  # X=thin (curl), Y=wide, Z=normal (length)
    else:  # Z
        scale = [1.5, 1.0, 0.3]  # X=wide, Y=normal (length), Z=thin (curl)
    
    # Flatten nail
    flatten_nail = nail_group.nodes.new("GeometryNodeTransform")
    flatten_nail.label = "Flatten Nail"
    flatten_nail.location = (-400, -300)
    flatten_nail.inputs["Scale"].default_value = tuple(scale)
    flatten_nail.inputs["Rotation"].default_value = (0.0, 0.0, 0.0)
    
    # Calculate nail position (at tip of distal segment, centered, on opposite side of curl)
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
    
    # Get max value for length axis (top of distal segment)
    length_max_output = separate_bbox_max.outputs["X"] if length_axis == 0 else (separate_bbox_max.outputs["Y"] if length_axis == 1 else separate_bbox_max.outputs["Z"])
    
    # Get max value for curl axis (opposite side of curl)
    curl_max_output = separate_bbox_max.outputs["X"] if curl_axis == 0 else (separate_bbox_max.outputs["Y"] if curl_axis == 1 else separate_bbox_max.outputs["Z"])
    
    # Add offset to curl axis to place nail on surface
    math_offset_curl = nail_group.nodes.new("ShaderNodeMath")
    math_offset_curl.label = "Offset to Surface"
    math_offset_curl.location = (-200, -100)
    math_offset_curl.operation = "ADD"
    math_offset_curl.inputs[1].default_value = distal_seg_radius * 0.1
    
    # Combine position (length at max, side at 0 center, curl at max + offset)
    combine_pos = nail_group.nodes.new("ShaderNodeCombineXYZ")
    combine_pos.label = "Nail Position"
    combine_pos.location = (0, -200)
    
    # Set axis values
    axis_inputs = {0: combine_pos.inputs["X"], 1: combine_pos.inputs["Y"], 2: combine_pos.inputs["Z"]}
    nail_group.links.new(length_max_output, axis_inputs[length_axis])
    axis_inputs[side_axis].default_value = 0.0  # Center on side axis
    nail_group.links.new(math_offset_curl.outputs["Value"], axis_inputs[curl_axis])
    
    # Position nail
    position_nail = nail_group.nodes.new("GeometryNodeTransform")
    position_nail.label = "Place on Distal"
    position_nail.location = (200, -300)
    
    # Join distal segment + nail
    join_nail = nail_group.nodes.new("GeometryNodeJoinGeometry")
    join_nail.label = "Join Distal + Nail"
    join_nail.location = (600, 0)
    
    # Connect nodes
    nail_group.links.new(input_node.outputs["Geometry"], bounding_box.inputs["Geometry"])
    nail_group.links.new(bounding_box.outputs["Max"], separate_bbox_max.inputs["Vector"])
    nail_group.links.new(curl_max_output, math_offset_curl.inputs[0])
    nail_group.links.new(nail_sphere.outputs["Mesh"], flatten_nail.inputs["Geometry"])
    nail_group.links.new(flatten_nail.outputs["Geometry"], position_nail.inputs["Geometry"])
    nail_group.links.new(combine_pos.outputs["Vector"], position_nail.inputs["Translation"])
    nail_group.links.new(input_node.outputs["Geometry"], join_nail.inputs["Geometry"])
    nail_group.links.new(position_nail.outputs["Geometry"], join_nail.inputs["Geometry"])
    nail_group.links.new(join_nail.outputs["Geometry"], output_node.inputs["Geometry"])
    
    return nail_group


def attach_fingernail_to_distal_segment(
    node_group,
    distal_transform_node,
    curl_direction,
    distal_seg_length,
    num_segments,
    taper_factor,
    finger_type,
    nail_size=0.003,
):
    """
    Build and attach a fingernail node group for the distal segment.
    """
    finger_enum = ensure_finger_type(finger_type)

    taper_multiplier = max(0.05, 1.0 - max(0, num_segments - 1) * taper_factor)
    distal_seg_radius = max(0.0005, (distal_seg_length * 0.5) * taper_multiplier)

    # Requirement: nail width is a third of the distal radius
    computed_nail_radius = distal_seg_radius / 3.0
    if nail_size > 0:
        computed_nail_radius = min(computed_nail_radius, nail_size)

    nail_group = create_fingernail_node_group(
        f"{finger_enum.value}_Fingernail",
        computed_nail_radius,
        curl_direction,
        distal_seg_radius,
    )

    nail_instance = node_group.nodes.new("GeometryNodeGroup")
    nail_instance.node_tree = nail_group
    nail_instance.label = f"{finger_enum.label} Nail"
    nail_instance.location = (
        distal_transform_node.location[0] + 200.0,
        distal_transform_node.location[1],
    )

    node_group.links.new(
        distal_transform_node.outputs["Geometry"], nail_instance.inputs["Geometry"]
    )

    return nail_instance


__all__ = [
    "attach_fingernail_to_distal_segment",
    "create_fingernail_node_group",
]
