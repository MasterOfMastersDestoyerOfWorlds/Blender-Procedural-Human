import bpy
import math
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_segment.finger_segment_curve_utils import (
    get_default_profile_curve,
    get_default_profile_curve_from_data,
)
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
    ProfileType,
)
from procedural_human.utils import setup_node_group_interface

from procedural_human.hand.finger.finger_segment.profile_curve_group import (
    create_profile_curve_offset_node_group,
)
from procedural_human.hand.finger.finger_segment.spatial_resampler import (
    create_spatial_profile_offset_node_group,
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
    sample_count_socket.default_value = 16

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

    add_length = segment_group.nodes.new("ShaderNodeMath")
    add_length.label = "End Z = Start Z + Length"
    add_length.location = (-800, 200)
    add_length.operation = "ADD"
    segment_group.links.new(separate_xyz.outputs["Z"], add_length.inputs[0])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_LENGTH.value],
        add_length.inputs[1],
    )

    combine_end = segment_group.nodes.new("ShaderNodeCombineXYZ")
    combine_end.label = "End Point"
    combine_end.location = (-600, 200)
    combine_end.inputs["X"].default_value = 0.0
    combine_end.inputs["Y"].default_value = 0.0
    segment_group.links.new(add_length.outputs["Value"], combine_end.inputs["Z"])

    combine_start = segment_group.nodes.new("ShaderNodeCombineXYZ")
    combine_start.label = "Start Point"
    combine_start.location = (-600, 0)
    combine_start.inputs["X"].default_value = 0.0
    combine_start.inputs["Y"].default_value = 0.0
    segment_group.links.new(separate_xyz.outputs["Z"], combine_start.inputs["Z"])

    scene = bpy.context.scene

    grid = segment_group.nodes.new("GeometryNodeMeshGrid")
    grid.label = "Parameter Grid"
    grid.location = (550, -100)
    grid.inputs["Vertices X"].default_value = 64
    # grid.inputs["Vertices Y"].default_value = 64 # Driven by logic
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0

    grid_pos = segment_group.nodes.new("GeometryNodeInputPosition")
    grid_pos.label = "Grid Position"
    grid_pos.location = (200, -250)

    separate_grid = segment_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_grid.label = "Separate Grid Coords"
    separate_grid.location = (400, -250)
    segment_group.links.new(
        grid_pos.outputs["Position"], separate_grid.inputs["Vector"]
    )

    angle_param = segment_group.nodes.new("ShaderNodeMath")
    angle_param.label = "Angle Param"
    angle_param.location = (600, -150)
    angle_param.operation = "ADD"
    angle_param.inputs[1].default_value = 0.5
    segment_group.links.new(separate_grid.outputs["X"], angle_param.inputs[0])

    length_param = segment_group.nodes.new("ShaderNodeMath")
    length_param.label = "Length Param"
    length_param.location = (600, -350)
    length_param.operation = "ADD"
    length_param.inputs[1].default_value = 0.5
    segment_group.links.new(separate_grid.outputs["Y"], length_param.inputs[0])

    angle_clamp = segment_group.nodes.new("ShaderNodeClamp")
    angle_clamp.label = "Clamp Angle"
    angle_clamp.location = (800, -150)
    angle_clamp.inputs["Value"].default_value = 1.0
    segment_group.links.new(angle_param.outputs["Value"], angle_clamp.inputs["Value"])

    length_clamp = segment_group.nodes.new("ShaderNodeClamp")
    length_clamp.label = "Clamp Length"
    length_clamp.location = (800, -350)
    length_clamp.inputs["Value"].default_value = 1.0
    segment_group.links.new(length_param.outputs["Value"], length_clamp.inputs["Value"])

    theta_node = segment_group.nodes.new("ShaderNodeMath")
    theta_node.label = "Angle θ"
    theta_node.location = (1200, -150)
    theta_node.operation = "MULTIPLY"
    theta_node.inputs[1].default_value = 2 * math.pi
    segment_group.links.new(angle_clamp.outputs["Result"], theta_node.inputs[0])

    cos_theta = segment_group.nodes.new("ShaderNodeMath")
    cos_theta.label = "cos(θ)"
    cos_theta.location = (1400, -120)
    cos_theta.operation = "COSINE"
    segment_group.links.new(theta_node.outputs["Value"], cos_theta.inputs[0])

    x_profile_offset_group = create_spatial_profile_offset_node_group(
        "X",
        input_node,
        segment_group,
        length_clamp,
        cos_theta,
        segment_length,
        segment_type,
    )

    sin_theta = segment_group.nodes.new("ShaderNodeMath")
    sin_theta.label = "sin(θ)"
    sin_theta.location = (1400, -300)
    sin_theta.operation = "SINE"
    segment_group.links.new(theta_node.outputs["Value"], sin_theta.inputs[0])

    y_profile_offset_group = create_profile_curve_offset_node_group(
        "Y",
        input_node,
        segment_group,
        length_clamp,
        sin_theta,
        segment_length,
        segment_type,
    )

    max_points = segment_group.nodes.new("ShaderNodeMath")
    max_points.label = "Max Points"
    max_points.location = (150, -150)
    max_points.operation = "MAXIMUM"
    segment_group.links.new(
        x_profile_offset_group.outputs["Point Count"], max_points.inputs[0]
    )
    segment_group.links.new(
        y_profile_offset_group.outputs["Point Count"], max_points.inputs[1]
    )

    final_count = segment_group.nodes.new("ShaderNodeMath")
    final_count.label = "Final Sample Count"
    final_count.location = (350, -50)
    final_count.operation = "MAXIMUM"
    segment_group.links.new(max_points.outputs["Value"], final_count.inputs[0])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SAMPLE_COUNT.value],
        final_count.inputs[1],
    )
    segment_group.links.new(final_count.outputs["Value"], grid.inputs["Vertices Y"])

    z_offset = segment_group.nodes.new("ShaderNodeMath")
    z_offset.label = "Length Offset"
    z_offset.location = (1400, -480)
    z_offset.operation = "MULTIPLY"
    segment_group.links.new(length_clamp.outputs["Result"], z_offset.inputs[0])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_LENGTH.value],
        z_offset.inputs[1],
    )

    z_position = segment_group.nodes.new("ShaderNodeMath")
    z_position.label = "Z Position"
    z_position.location = (1600, -480)
    z_position.operation = "ADD"
    segment_group.links.new(separate_xyz.outputs["Z"], z_position.inputs[0])
    segment_group.links.new(z_offset.outputs["Value"], z_position.inputs[1])

    final_pos = segment_group.nodes.new("ShaderNodeCombineXYZ")
    final_pos.label = "Final Position"
    final_pos.location = (1800, -300)
    segment_group.links.new(
        x_profile_offset_group.outputs["Offset"], final_pos.inputs["X"]
    )
    segment_group.links.new(
        y_profile_offset_group.outputs["Offset"], final_pos.inputs["Y"]
    )
    segment_group.links.new(z_position.outputs["Value"], final_pos.inputs["Z"])
    apply_shape = segment_group.nodes.new("GeometryNodeSetPosition")
    apply_shape.label = "Apply Shape"
    apply_shape.location = (2000, 0)
    segment_group.links.new(grid.outputs["Mesh"], apply_shape.inputs["Geometry"])
    segment_group.links.new(final_pos.outputs["Vector"], apply_shape.inputs["Position"])

    join_geo = segment_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.label = "Join With Previous"
    join_geo.location = (2400, 0)
    segment_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
    segment_group.links.new(
        apply_shape.outputs["Geometry"], join_geo.inputs["Geometry"]
    )

    output_node = segment_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (2600, 0)
    segment_group.links.new(
        join_geo.outputs["Geometry"], output_node.inputs["Geometry"]
    )
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        output_node.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
    )

    return segment_group
