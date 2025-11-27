import bpy
import math
from procedural_human.geo_node_groups.closures import create_float_curve_closure
from procedural_human.hand.finger.finger_segment.finger_segment_const import (
    SEGMENT_SAMPLE_COUNT,
)
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
)
from procedural_human.utils import setup_node_group_interface
from procedural_human.geo_node_groups.dual_radial import (
    create_dual_profile_radial_group,
)


def create_finger_segment_node_group(
    name,
    segment_length,
    seg_radius,
    segment_type=SegmentType.PROXIMAL,
):
    """
    Create a reusable node group for a finger segment using X/Y profile curves.

    Uses angle-based interpolation for organic cross-sections:
    radius(θ) = sqrt((X(t)*cos(θ))² + (Y(t)*sin(θ))²)

    Args:
        name: Name for the node group
        segment_length: Length of the segment in Blender units
        seg_radius: Base radius of the segment
        segment_type: Type of segment (SegmentType enum)

    Returns:
        Node group for the finger segment
    """

    segment_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(segment_group)

    length_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_LENGTH.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    length_socket.default_value = segment_length

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

    sample_count_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SAMPLE_COUNT.value,
        in_out="INPUT",
        socket_type="NodeSocketInt",
    )
    sample_count_socket.default_value = SEGMENT_SAMPLE_COUNT

    segment_group.interface.new_socket(
        name="X Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )
    segment_group.interface.new_socket(
        name="Y Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )

    input_node = segment_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-1400, 0)

    bbox_node = segment_group.nodes.new("GeometryNodeBoundBox")
    bbox_node.label = "Find Endpoint"
    bbox_node.location = (-1200, 200)
    segment_group.links.new(
        input_node.outputs["Geometry"], bbox_node.inputs["Geometry"]
    )

    separate_xyz = segment_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.label = "Extract Z"
    separate_xyz.location = (-1000, 200)
    segment_group.links.new(bbox_node.outputs["Max"], separate_xyz.inputs["Vector"])

    grid = segment_group.nodes.new("GeometryNodeMeshGrid")
    grid.label = "Parameter Grid"
    grid.location = (550, -100)
    grid.inputs["Vertices X"].default_value = SEGMENT_SAMPLE_COUNT
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0

    radial_suffix = (
        segment_type.value.title()
        if hasattr(segment_type, "value")
        else str(segment_type).title()
    )

    radial_group = create_dual_profile_radial_group(suffix=radial_suffix)
    radial_instance = segment_group.nodes.new("GeometryNodeGroup")
    radial_instance.node_tree = radial_group
    radial_instance.label = "Radial Profile (Dual)"
    radial_instance.location = (1400, -200)

    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        radial_instance.inputs["Radius"],
    )
    segment_group.links.new(
        separate_xyz.outputs["Z"],
        radial_instance.inputs["Z Position"],
    )
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_LENGTH.value],
        radial_instance.inputs["Segment Length"],
    )



    segment_group.links.new(input_node.outputs["X Float Curve"], radial_instance.inputs["X Float Curve"])

    segment_group.links.new(input_node.outputs["Y Float Curve"], radial_instance.inputs["Y Float Curve"])

    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SAMPLE_COUNT.value],
        grid.inputs["Vertices Y"],
    )

    apply_shape = segment_group.nodes.new("GeometryNodeSetPosition")
    apply_shape.label = "Apply Shape"
    apply_shape.location = (2200, 0)
    segment_group.links.new(grid.outputs["Mesh"], apply_shape.inputs["Geometry"])
    segment_group.links.new(
        radial_instance.outputs["Position"], apply_shape.inputs["Position"]
    )

    output_node = segment_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (2600, 0)
    segment_group.links.new(
        apply_shape.outputs["Geometry"], output_node.inputs["Geometry"]
    )
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        output_node.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
    )

    return segment_group
