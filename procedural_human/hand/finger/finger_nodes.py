"""
Finger Geometry Nodes setup for Procedural Human Generator
"""

import bpy
from procedural_human.hand.finger.finger import FingerData
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
    ProfileType,
    get_profile_data,
)
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
    finger: FingerData,
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
    finger_type = ensure_finger_type(finger.finger_type)

    input_node = node_group.nodes.new("NodeGroupInput")
    input_node.label = "Input"
    output_node = node_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"

    input_node.location = (-1000, 0)
    output_node.location = (1200, 0)

    if finger.segment_lengths is None:
        segment_lengths = [
            finger.total_length / finger.num_segments
        ] * finger.num_segments

    starting_point = node_group.nodes.new("GeometryNodeCurvePrimitiveLine")
    starting_point.label = "Starting Axis"
    starting_point.location = (-700, 400)
    starting_point.inputs["Start"].default_value = (0.0, 0.0, 0.0)
    starting_point.inputs["End"].default_value = (0.0, 0.0, 0.0)

    segment_types = [SegmentType.PROXIMAL, SegmentType.MIDDLE, SegmentType.DISTAL]
    segment_profile_meta = {}

    for seg_type in SegmentType:

        segment_profile_meta[seg_type] = {
            "start": 1.0,
            "end": 0.85,
        }

    segment_node_instances = []
    previous_segment_output = starting_point.outputs["Curve"]
    next_segment_radius = None

    for seg_idx in range(finger.num_segments):
        seg_length = finger.segment_lengths[seg_idx]
        base_radius = seg_length * 0.5
        seg_radius = base_radius * (1.0 - seg_idx * finger.taper_factor)
        if finger.num_segments == 2:
            segment_enum = SegmentType.PROXIMAL if seg_idx == 0 else SegmentType.DISTAL
        else:
            segment_enum = (
                segment_types[seg_idx]
                if seg_idx < len(segment_types)
                else segment_types[-1]
            )
        if isinstance(segment_enum, SegmentType):
            seg_name = segment_enum.value.capitalize()
        else:
            seg_name = str(segment_enum)

        segment_group = create_finger_segment_node_group(
            f"{finger_type.value}_{seg_name}_Segment_Group",
            seg_length,
            seg_radius,
            segment_type=segment_enum,
        )

        segment_instance = node_group.nodes.new("GeometryNodeGroup")
        segment_instance.node_tree = segment_group
        segment_instance.label = f"{seg_name} Segment"
        segment_instance.location = (-400, 200 - seg_idx * 300)

        node_group.links.new(
            previous_segment_output, segment_instance.inputs["Geometry"]
        )
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_LENGTH.value
        ].default_value = seg_length
        if next_segment_radius is None:
            segment_radius_scale = seg_radius
        else:
            segment_radius_scale = next_segment_radius
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_RADIUS.value
        ].default_value = segment_radius_scale

        profile_ratios = segment_profile_meta[segment_enum]
        continuity_ratio = (
            profile_ratios["end"] / profile_ratios["start"]
            if profile_ratios["start"] != 0
            else 1.0
        )
        next_segment_radius = segment_radius_scale * continuity_ratio

        segment_node_instances.append(
            (seg_name, segment_instance, seg_idx, segment_radius_scale, seg_length)
        )

        previous_segment_output = segment_instance.outputs["Geometry"]

    distal_seg_name, distal_node, distal_idx, distal_seg_radius, distal_seg_length = (
        segment_node_instances[-1]
    )
    nail_instance = attach_fingernail_to_distal_segment(
        node_group=node_group,
        distal_transform_node=distal_node,
        curl_direction=finger.curl_direction,
        distal_seg_radius=distal_seg_radius,
        finger_type=finger_type,
        nail_size=finger.nail_size,
    )

    node_group.links.new(
        nail_instance.outputs["Geometry"], output_node.inputs["Geometry"]
    )

    return node_group
