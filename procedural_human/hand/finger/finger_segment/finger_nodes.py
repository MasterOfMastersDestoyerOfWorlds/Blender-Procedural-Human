"""
Finger Geometry Nodes setup for Procedural Human Generator
"""

import bpy
from procedural_human.hand.finger_segment.finger_types import (
    FingerSegmentProperties,
    FingerType,
    ensure_finger_type,
)
from procedural_human.hand.finger_segment.finger_nail.finger_nail_nodes import (
    attach_fingernail_to_distal_segment,
)
from procedural_human.utils import setup_node_group_interface


def _create_finger_segment_node_group(
    name,
    start_ratio,
    segment_ratio,
    seg_radius,
):
    """
    Create a reusable node group for a finger segment

    Args:
        name: Name for the node group
        seg_length: Length of the segment
        seg_radius: Radius of the segment
        length_axis: Axis along which the finger extends (0=X, 1=Y, 2=Z)
        segment_ratio: Fraction of total finger length represented by this segment

    Returns:
        Node group for the finger segment
    """
    # Create node group
    segment_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(segment_group)

    # Additional input sockets for ratios and radius
    start_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.START_RATIO.value, in_out="INPUT", socket_type="NodeSocketFloat"
    )
    start_socket.default_value = start_ratio

    ratio_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RATIO.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    ratio_socket.default_value = segment_ratio

    radius_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    radius_socket.default_value = seg_radius

    radius_output = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="OUTPUT",
        socket_type="NodeSocketFloat",
    )

    # Input/Output nodes
    input_node = segment_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-600, 0)

    output_node = segment_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (500, 0)

    # Trim curve to isolate this segment
    trim_curve = segment_group.nodes.new("GeometryNodeTrimCurve")
    trim_curve.label = "Segment Span"
    trim_curve.location = (-200, 0)
    trim_curve.mode = "FACTOR"
    segment_group.links.new(input_node.outputs["Geometry"], trim_curve.inputs["Curve"])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.START_RATIO.value], trim_curve.inputs["Start"]
    )

    end_math = segment_group.nodes.new("ShaderNodeMath")
    end_math.label = "End Ratio"
    end_math.location = (-350, -150)
    end_math.operation = "ADD"
    segment_group.links.new(input_node.outputs[FingerSegmentProperties.START_RATIO.value], end_math.inputs[0])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RATIO.value],
        end_math.inputs[1],
    )
    segment_group.links.new(end_math.outputs["Value"], trim_curve.inputs["End"])

    # Profile circle for cylinder
    curve_circle = segment_group.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.label = "Segment Profile"
    curve_circle.location = (-200, -250)
    curve_circle.inputs["Resolution"].default_value = 16
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        curve_circle.inputs["Radius"],
    )

    # Convert trimmed curve to mesh using profile
    curve_to_mesh = segment_group.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.label = "Segment Mesh"
    curve_to_mesh.location = (200, 0)
    curve_to_mesh.inputs["Fill Caps"].default_value = True
    segment_group.links.new(trim_curve.outputs["Curve"], curve_to_mesh.inputs["Curve"])
    segment_group.links.new(
        curve_circle.outputs["Curve"], curve_to_mesh.inputs["Profile Curve"]
    )

    segment_group.links.new(
        curve_to_mesh.outputs["Mesh"], output_node.inputs["Geometry"]
    )
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        output_node.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
    )

    return segment_group


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
    else:
        total_length = sum(segment_lengths)

    # Base axis curve - all segments grow from this geometry
    axis_curve = node_group.nodes.new("GeometryNodeCurvePrimitiveLine")
    axis_curve.label = "Finger Axis"
    axis_curve.location = (-700, 400)
    start_point = [0.0, 0.0, 0.0]
    end_point = [0.0, 0.0, 0.0]
    end_point[length_axis] = total_length
    axis_curve.inputs["Start"].default_value = tuple(start_point)
    axis_curve.inputs["End"].default_value = tuple(end_point)

    segment_names = ["Proximal", "Middle", "Distal"]
    segment_node_instances = []
    cumulative_length = 0.0

    for seg_idx in range(num_segments):
        seg_length = segment_lengths[seg_idx]
        base_radius = seg_length * 0.5
        seg_radius = base_radius * (1.0 - seg_idx * taper_factor)

        start_ratio = (cumulative_length / total_length) if total_length > 0 else 0.0
        segment_ratio = (seg_length / total_length) if total_length > 0 else 0.0

        if num_segments == 2:
            seg_name = "Proximal" if seg_idx == 0 else "Distal"
        else:
            seg_name = (
                segment_names[seg_idx]
                if seg_idx < len(segment_names)
                else f"Segment {seg_idx}"
            )

        segment_group = _create_finger_segment_node_group(
            f"{finger_type.value}_{seg_name}_Segment_Group",
            start_ratio,
            segment_ratio,
            seg_radius,
        )

        segment_instance = node_group.nodes.new("GeometryNodeGroup")
        segment_instance.node_tree = segment_group
        segment_instance.label = f"{seg_name} Segment"
        segment_instance.location = (-400, 200 - seg_idx * 300)

        node_group.links.new(
            axis_curve.outputs["Curve"], segment_instance.inputs["Geometry"]
        )
        segment_instance.inputs[FingerSegmentProperties.START_RATIO.value].default_value = start_ratio
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_RATIO.value
        ].default_value = segment_ratio
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_RADIUS.value
        ].default_value = seg_radius

        segment_node_instances.append((seg_name, segment_instance, seg_idx, seg_radius))
        cumulative_length += seg_length

    # Attach fingernail to distal segment via helper in the fingernail module
    distal_seg_name, distal_node, distal_idx, distal_seg_radius = (
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

    # Join ALL segments (proximal, middle, distal+nail) - THIS IS THE FINAL OPERATION
    join_all = node_group.nodes.new("GeometryNodeJoinGeometry")
    join_all.label = "Join All Finger Parts (FINAL)"
    join_all.location = (0, 0)

    # Connect all segment outputs to final join
    for idx, (seg_name, segment_node, seg_idx, seg_radius) in enumerate(
        segment_node_instances
    ):
        if idx == len(segment_node_instances) - 1:
            # Last segment (distal) - use the nail instance output instead
            node_group.links.new(
                nail_instance.outputs["Geometry"], join_all.inputs["Geometry"]
            )
        else:
            # Other segments (proximal, middle)
            node_group.links.new(
                segment_node.outputs["Geometry"], join_all.inputs["Geometry"]
            )

    # Connect final join to output
    node_group.links.new(join_all.outputs["Geometry"], output_node.inputs["Geometry"])

    return node_group
