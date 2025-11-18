"""
Finger Geometry Nodes setup for Procedural Human Generator
"""

import bpy
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import SegmentType
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_types import (
    FingerType,
    ensure_finger_type,
)
from procedural_human.hand.finger.finger_nail.finger_nail_nodes import (
    attach_fingernail_to_distal_segment,
)
from procedural_human.hand.finger.finger_segment.finger_segment_nodes import (
    create_finger_segment_node_group,
)
from procedural_human.utils import setup_node_group_interface


def create_finger_nodes(
    node_group,
    num_segments=3,
    segment_lengths=None,
    radius=0.007,
    nail_size=0.003,
    taper_factor=0.15,
    curl_direction="Y",
    finger_type=FingerType.INDEX,
):
    """
    Create complete finger geometry with variable segments and fingernail

    Args:
        node_group: Geometry node group to populate
        num_segments: Number of segments (2 or 3)
        segment_lengths: List of segment lengths in blender units
        radius: Base finger radius
        nail_size: Fingernail size
        taper_factor: How much radius decreases per segment
        curl_direction: Curl direction axis ("X", "Y", or "Z")
    """
    setup_node_group_interface(node_group)
    finger_type = ensure_finger_type(finger_type)

    # Input/Output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    input_node.label = "Input"
    output_node = node_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"

    # Position nodes
    input_node.location = (-1000, 0)
    output_node.location = (1200, 0)

    # Determine axis mapping based on curl direction
    # Default: Z is up (finger length), Y is curl direction (forward/back)
    if curl_direction == "X":
        length_axis = 2  # Z
    elif curl_direction == "Y":
        length_axis = 2  # Z
    else:  # Z
        length_axis = 1  # Y

    # Calculate segment lengths if not provided
    if segment_lengths is None:
        total_length = 1.0
        segment_lengths = [total_length / num_segments] * num_segments

    # Create starting axis point at origin (Z=0)
    # This will be the input for the first segment
    starting_point = node_group.nodes.new("GeometryNodeCurvePrimitiveLine")
    starting_point.label = "Starting Axis"
    starting_point.location = (-700, 400)
    starting_point.inputs["Start"].default_value = (0.0, 0.0, 0.0)
    starting_point.inputs["End"].default_value = (0.0, 0.0, 0.0)  # Zero-length line at origin

    segment_types = [SegmentType.PROXIMAL, SegmentType.MIDDLE, SegmentType.DISTAL]
    segment_node_instances = []
    previous_segment_output = starting_point.outputs["Curve"]

    for seg_idx in range(num_segments):
        seg_length = segment_lengths[seg_idx]
        base_radius = seg_length * 0.5
        seg_radius = base_radius * (1.0 - seg_idx * taper_factor)

        if num_segments == 2:
            seg_name = "Proximal" if seg_idx == 0 else "Distal"
        else:
            seg_name = (
                segment_types[seg_idx]
                if seg_idx < len(segment_types)
                else f"Segment {seg_idx}"
            )

        segment_group = create_finger_segment_node_group(
            f"{finger_type.value}_{seg_name}_Segment_Group",
            seg_length,
            seg_radius,
            segment_type=segment_types[seg_idx],
        )

        segment_instance = node_group.nodes.new("GeometryNodeGroup")
        segment_instance.node_tree = segment_group
        segment_instance.label = f"{seg_name} Segment"
        segment_instance.location = (-400, 200 - seg_idx * 300)

        # Chain: connect previous segment's output to this segment's input
        node_group.links.new(
            previous_segment_output, segment_instance.inputs["Geometry"]
        )
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_LENGTH.value
        ].default_value = seg_length
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_RADIUS.value
        ].default_value = seg_radius

        segment_node_instances.append((seg_name, segment_instance, seg_idx, seg_radius, seg_length))
        
        # Update previous output for next iteration
        previous_segment_output = segment_instance.outputs["Geometry"]

    # Attach fingernail to distal segment via helper in the fingernail module
    distal_seg_name, distal_node, distal_idx, distal_seg_radius, distal_seg_length = (
        segment_node_instances[-1]
    )
    nail_instance = attach_fingernail_to_distal_segment(
        node_group=node_group,
        distal_transform_node=distal_node,
        curl_direction=curl_direction,
        distal_seg_radius=distal_seg_radius,
        finger_type=finger_type,
        nail_size=nail_size,
    )

    # Since segments are chained, the nail_instance already contains all geometry
    # Just connect it directly to output
    node_group.links.new(nail_instance.outputs["Geometry"], output_node.inputs["Geometry"])

    return node_group
