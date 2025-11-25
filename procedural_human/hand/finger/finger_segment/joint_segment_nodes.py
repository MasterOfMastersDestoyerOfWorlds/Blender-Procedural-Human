"""
Joint Segment Nodes for smooth transitions between finger segments.

Joint segments create organic transitions at knuckle locations by:
- Overlapping with neighboring segments
- Blending radii smoothly between segments
- Creating bulging geometry for realistic joint appearance
"""

import bpy
import math
from procedural_human.geo_node_groups.closures import create_float_curve_closure
from procedural_human.hand.finger.finger_segment.finger_segment_const import (
    SEGMENT_SAMPLE_COUNT,
)
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    JointSegmentProperties,
)
from procedural_human.utils import setup_node_group_interface


# Default joint configuration
DEFAULT_JOINT_OVERLAP = 0.15  # 15% overlap into each neighboring segment
DEFAULT_JOINT_BLEND = 0.5  # Smoothness of transition (0=sharp, 1=very smooth)
DEFAULT_JOINT_THICKNESS = 1.1  # Joint is 10% thicker than average of neighbors
JOINT_SAMPLE_COUNT = 8  # Samples along joint length


def create_joint_segment_node_group(
    name: str,
    start_radius: float,
    end_radius: float,
    overlap_amount: float = DEFAULT_JOINT_OVERLAP,
    blend_factor: float = DEFAULT_JOINT_BLEND,
    thickness_ratio: float = DEFAULT_JOINT_THICKNESS,
):
    """
    Create a node group for a joint segment that smoothly connects two regular segments.

    The joint creates a bulging transition between segments, simulating the appearance
    of knuckles and joints in a finger.

    Args:
        name: Name for the node group
        start_radius: Radius at the start (from previous segment's end)
        end_radius: Radius at the end (to next segment's start)
        overlap_amount: How much the joint extends into neighboring segments (0-0.5)
        blend_factor: Smoothness of the radius blend (0=linear, 1=very smooth)
        thickness_ratio: Multiplier for joint thickness (>1 for bulging joints)

    Returns:
        Node group for the joint segment
    """
    joint_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(joint_group)

    # Input sockets
    start_radius_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.START_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    start_radius_socket.default_value = start_radius

    end_radius_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.END_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    end_radius_socket.default_value = end_radius

    overlap_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.OVERLAP_AMOUNT.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    overlap_socket.default_value = overlap_amount
    overlap_socket.min_value = 0.0
    overlap_socket.max_value = 0.5

    blend_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.BLEND_FACTOR.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    blend_socket.default_value = blend_factor
    blend_socket.min_value = 0.0
    blend_socket.max_value = 1.0

    thickness_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.THICKNESS_RATIO.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    thickness_socket.default_value = thickness_ratio
    thickness_socket.min_value = 0.5
    thickness_socket.max_value = 2.0

    sample_count_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.SAMPLE_COUNT.value,
        in_out="INPUT",
        socket_type="NodeSocketInt",
    )
    sample_count_socket.default_value = JOINT_SAMPLE_COUNT

    # Output sockets
    end_radius_output = joint_group.interface.new_socket(
        name=JointSegmentProperties.END_RADIUS.value,
        in_out="OUTPUT",
        socket_type="NodeSocketFloat",
    )

    # Create nodes
    input_node = joint_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-1400, 0)

    # Get Z position from input geometry's bounding box
    bbox_node = joint_group.nodes.new("GeometryNodeBoundBox")
    bbox_node.label = "Find Endpoint"
    bbox_node.location = (-1200, 200)
    joint_group.links.new(
        input_node.outputs["Geometry"], bbox_node.inputs["Geometry"]
    )

    separate_xyz = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.label = "Extract Z"
    separate_xyz.location = (-1000, 200)
    joint_group.links.new(bbox_node.outputs["Max"], separate_xyz.inputs["Vector"])

    # Calculate joint length based on overlap
    # Joint length = 2 * overlap_amount * average_radius
    avg_radius = joint_group.nodes.new("ShaderNodeMath")
    avg_radius.label = "Average Radius"
    avg_radius.operation = "ADD"
    avg_radius.location = (-1000, -100)
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.START_RADIUS.value],
        avg_radius.inputs[0],
    )
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.END_RADIUS.value],
        avg_radius.inputs[1],
    )

    avg_radius_div = joint_group.nodes.new("ShaderNodeMath")
    avg_radius_div.label = "Avg Radius / 2"
    avg_radius_div.operation = "DIVIDE"
    avg_radius_div.inputs[1].default_value = 2.0
    avg_radius_div.location = (-800, -100)
    joint_group.links.new(avg_radius.outputs["Value"], avg_radius_div.inputs[0])

    # Joint length = overlap * 4 * avg_radius (spans 2x overlap on each side)
    joint_length = joint_group.nodes.new("ShaderNodeMath")
    joint_length.label = "Joint Length"
    joint_length.operation = "MULTIPLY"
    joint_length.location = (-600, -100)
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.OVERLAP_AMOUNT.value],
        joint_length.inputs[0],
    )
    joint_group.links.new(avg_radius_div.outputs["Value"], joint_length.inputs[1])

    joint_length_scale = joint_group.nodes.new("ShaderNodeMath")
    joint_length_scale.label = "Scale Joint Length"
    joint_length_scale.operation = "MULTIPLY"
    joint_length_scale.inputs[1].default_value = 4.0
    joint_length_scale.location = (-400, -100)
    joint_group.links.new(joint_length.outputs["Value"], joint_length_scale.inputs[0])

    # Create parameter grid for the joint surface
    grid = joint_group.nodes.new("GeometryNodeMeshGrid")
    grid.label = "Joint Parameter Grid"
    grid.location = (0, -200)
    grid.inputs["Vertices X"].default_value = SEGMENT_SAMPLE_COUNT
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.SAMPLE_COUNT.value],
        grid.inputs["Vertices Y"],
    )

    # Get grid position for parameter extraction
    grid_pos = joint_group.nodes.new("GeometryNodeInputPosition")
    grid_pos.label = "Grid Position"
    grid_pos.location = (200, -300)

    separate_grid = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_grid.label = "Separate Grid Coords"
    separate_grid.location = (400, -300)
    joint_group.links.new(grid_pos.outputs["Position"], separate_grid.inputs["Vector"])

    # Normalize parameters to 0-1 range
    angle_param = joint_group.nodes.new("ShaderNodeMath")
    angle_param.label = "Angle Param"
    angle_param.operation = "ADD"
    angle_param.inputs[1].default_value = 0.5
    angle_param.location = (600, -200)
    joint_group.links.new(separate_grid.outputs["X"], angle_param.inputs[0])

    length_param = joint_group.nodes.new("ShaderNodeMath")
    length_param.label = "Length Param (t)"
    length_param.operation = "ADD"
    length_param.inputs[1].default_value = 0.5
    length_param.location = (600, -400)
    joint_group.links.new(separate_grid.outputs["Y"], length_param.inputs[0])

    # Clamp parameters
    angle_clamp = joint_group.nodes.new("ShaderNodeClamp")
    angle_clamp.label = "Clamp Angle"
    angle_clamp.location = (800, -200)
    joint_group.links.new(angle_param.outputs["Value"], angle_clamp.inputs["Value"])

    length_clamp = joint_group.nodes.new("ShaderNodeClamp")
    length_clamp.label = "Clamp Length"
    length_clamp.location = (800, -400)
    joint_group.links.new(length_param.outputs["Value"], length_clamp.inputs["Value"])

    # Convert angle parameter to radians (0-1 -> 0-2π)
    theta_node = joint_group.nodes.new("ShaderNodeMath")
    theta_node.label = "Angle θ"
    theta_node.operation = "MULTIPLY"
    theta_node.inputs[1].default_value = 2 * math.pi
    theta_node.location = (1000, -200)
    joint_group.links.new(angle_clamp.outputs["Result"], theta_node.inputs[0])

    # Smoothstep blend for the length parameter
    # Creates smooth transition: smoothstep(t) = t² * (3 - 2t)
    t_squared = joint_group.nodes.new("ShaderNodeMath")
    t_squared.label = "t²"
    t_squared.operation = "POWER"
    t_squared.inputs[1].default_value = 2.0
    t_squared.location = (1000, -500)
    joint_group.links.new(length_clamp.outputs["Result"], t_squared.inputs[0])

    three_minus_2t = joint_group.nodes.new("ShaderNodeMath")
    three_minus_2t.label = "3 - 2t"
    three_minus_2t.operation = "MULTIPLY"
    three_minus_2t.inputs[1].default_value = -2.0
    three_minus_2t.location = (1000, -650)
    joint_group.links.new(length_clamp.outputs["Result"], three_minus_2t.inputs[0])

    add_three = joint_group.nodes.new("ShaderNodeMath")
    add_three.label = "+ 3"
    add_three.operation = "ADD"
    add_three.inputs[1].default_value = 3.0
    add_three.location = (1200, -650)
    joint_group.links.new(three_minus_2t.outputs["Value"], add_three.inputs[0])

    smoothstep = joint_group.nodes.new("ShaderNodeMath")
    smoothstep.label = "Smoothstep"
    smoothstep.operation = "MULTIPLY"
    smoothstep.location = (1400, -550)
    joint_group.links.new(t_squared.outputs["Value"], smoothstep.inputs[0])
    joint_group.links.new(add_three.outputs["Value"], smoothstep.inputs[1])

    # Interpolate blend factor to control smoothness
    blend_lerp = joint_group.nodes.new("ShaderNodeMix")
    blend_lerp.data_type = "FLOAT"
    blend_lerp.label = "Blend Linear/Smooth"
    blend_lerp.location = (1600, -500)
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.BLEND_FACTOR.value],
        blend_lerp.inputs["Factor"],
    )
    joint_group.links.new(length_clamp.outputs["Result"], blend_lerp.inputs[4])  # A (linear)
    joint_group.links.new(smoothstep.outputs["Value"], blend_lerp.inputs[5])  # B (smooth)

    # Interpolate radius between start and end
    radius_lerp = joint_group.nodes.new("ShaderNodeMix")
    radius_lerp.data_type = "FLOAT"
    radius_lerp.label = "Lerp Radius"
    radius_lerp.location = (1800, -400)
    joint_group.links.new(blend_lerp.outputs["Result"], radius_lerp.inputs["Factor"])
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.START_RADIUS.value],
        radius_lerp.inputs[4],  # A
    )
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.END_RADIUS.value],
        radius_lerp.inputs[5],  # B
    )

    # Create joint bulge profile using a sine wave centered at t=0.5
    # bulge = sin(π * t) gives 0->1->0 bulge
    pi_t = joint_group.nodes.new("ShaderNodeMath")
    pi_t.label = "π * t"
    pi_t.operation = "MULTIPLY"
    pi_t.inputs[1].default_value = math.pi
    pi_t.location = (1400, -750)
    joint_group.links.new(length_clamp.outputs["Result"], pi_t.inputs[0])

    sin_bulge = joint_group.nodes.new("ShaderNodeMath")
    sin_bulge.label = "sin(π*t)"
    sin_bulge.operation = "SINE"
    sin_bulge.location = (1600, -750)
    joint_group.links.new(pi_t.outputs["Value"], sin_bulge.inputs[0])

    # Scale bulge by (thickness_ratio - 1) so thickness_ratio=1 means no bulge
    thickness_minus_one = joint_group.nodes.new("ShaderNodeMath")
    thickness_minus_one.label = "Thickness - 1"
    thickness_minus_one.operation = "SUBTRACT"
    thickness_minus_one.inputs[1].default_value = 1.0
    thickness_minus_one.location = (1600, -900)
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.THICKNESS_RATIO.value],
        thickness_minus_one.inputs[0],
    )

    bulge_scale = joint_group.nodes.new("ShaderNodeMath")
    bulge_scale.label = "Bulge Scale"
    bulge_scale.operation = "MULTIPLY"
    bulge_scale.location = (1800, -800)
    joint_group.links.new(sin_bulge.outputs["Value"], bulge_scale.inputs[0])
    joint_group.links.new(thickness_minus_one.outputs["Value"], bulge_scale.inputs[1])

    # Add 1 to get final radius multiplier
    bulge_mult = joint_group.nodes.new("ShaderNodeMath")
    bulge_mult.label = "1 + Bulge"
    bulge_mult.operation = "ADD"
    bulge_mult.inputs[1].default_value = 1.0
    bulge_mult.location = (2000, -700)
    joint_group.links.new(bulge_scale.outputs["Value"], bulge_mult.inputs[0])

    # Apply bulge to interpolated radius
    final_radius = joint_group.nodes.new("ShaderNodeMath")
    final_radius.label = "Final Radius"
    final_radius.operation = "MULTIPLY"
    final_radius.location = (2200, -500)
    joint_group.links.new(radius_lerp.outputs["Result"], final_radius.inputs[0])
    joint_group.links.new(bulge_mult.outputs["Value"], final_radius.inputs[1])

    # Calculate X, Y positions using radius and angle
    cos_theta = joint_group.nodes.new("ShaderNodeMath")
    cos_theta.label = "cos(θ)"
    cos_theta.operation = "COSINE"
    cos_theta.location = (2000, -200)
    joint_group.links.new(theta_node.outputs["Value"], cos_theta.inputs[0])

    sin_theta = joint_group.nodes.new("ShaderNodeMath")
    sin_theta.label = "sin(θ)"
    sin_theta.operation = "SINE"
    sin_theta.location = (2000, -350)
    joint_group.links.new(theta_node.outputs["Value"], sin_theta.inputs[0])

    final_x = joint_group.nodes.new("ShaderNodeMath")
    final_x.label = "X = r * cos(θ)"
    final_x.operation = "MULTIPLY"
    final_x.location = (2400, -200)
    joint_group.links.new(final_radius.outputs["Value"], final_x.inputs[0])
    joint_group.links.new(cos_theta.outputs["Value"], final_x.inputs[1])

    final_y = joint_group.nodes.new("ShaderNodeMath")
    final_y.label = "Y = r * sin(θ)"
    final_y.operation = "MULTIPLY"
    final_y.location = (2400, -350)
    joint_group.links.new(final_radius.outputs["Value"], final_y.inputs[0])
    joint_group.links.new(sin_theta.outputs["Value"], final_y.inputs[1])

    # Calculate Z position: z_start + t * joint_length
    z_offset = joint_group.nodes.new("ShaderNodeMath")
    z_offset.label = "Z Offset"
    z_offset.operation = "MULTIPLY"
    z_offset.location = (2200, -100)
    joint_group.links.new(length_clamp.outputs["Result"], z_offset.inputs[0])
    joint_group.links.new(joint_length_scale.outputs["Value"], z_offset.inputs[1])

    final_z = joint_group.nodes.new("ShaderNodeMath")
    final_z.label = "Final Z"
    final_z.operation = "ADD"
    final_z.location = (2400, -100)
    joint_group.links.new(separate_xyz.outputs["Z"], final_z.inputs[0])
    joint_group.links.new(z_offset.outputs["Value"], final_z.inputs[1])

    # Combine into final position vector
    final_pos = joint_group.nodes.new("ShaderNodeCombineXYZ")
    final_pos.label = "Final Position"
    final_pos.location = (2600, -250)
    joint_group.links.new(final_x.outputs["Value"], final_pos.inputs["X"])
    joint_group.links.new(final_y.outputs["Value"], final_pos.inputs["Y"])
    joint_group.links.new(final_z.outputs["Value"], final_pos.inputs["Z"])

    # Apply position to grid
    apply_shape = joint_group.nodes.new("GeometryNodeSetPosition")
    apply_shape.label = "Apply Shape"
    apply_shape.location = (2800, -200)
    joint_group.links.new(grid.outputs["Mesh"], apply_shape.inputs["Geometry"])
    joint_group.links.new(final_pos.outputs["Vector"], apply_shape.inputs["Position"])

    # Join with input geometry
    join_geo = joint_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.label = "Join With Previous"
    join_geo.location = (3000, 0)
    joint_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
    joint_group.links.new(apply_shape.outputs["Geometry"], join_geo.inputs["Geometry"])

    # Output
    output_node = joint_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (3200, 0)
    joint_group.links.new(join_geo.outputs["Geometry"], output_node.inputs["Geometry"])
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.END_RADIUS.value],
        output_node.inputs[JointSegmentProperties.END_RADIUS.value],
    )

    return joint_group


def create_joint_between_segments(
    segment_before_radius: float,
    segment_after_radius: float,
    joint_index: int,
    overlap_amount: float = DEFAULT_JOINT_OVERLAP,
    blend_factor: float = DEFAULT_JOINT_BLEND,
    thickness_ratio: float = DEFAULT_JOINT_THICKNESS,
):
    """
    Create a joint node group configured for a specific location between segments.

    Args:
        segment_before_radius: End radius of the segment before this joint
        segment_after_radius: Start radius of the segment after this joint
        joint_index: Index of this joint (0 = between seg0 and seg1, etc.)
        overlap_amount: How much joint overlaps with neighbors
        blend_factor: Smoothness of transition
        thickness_ratio: Thickness multiplier for joint bulge

    Returns:
        Configured joint segment node group
    """
    joint_name = f"Joint_{joint_index}_Segment_Group"
    return create_joint_segment_node_group(
        name=joint_name,
        start_radius=segment_before_radius,
        end_radius=segment_after_radius,
        overlap_amount=overlap_amount,
        blend_factor=blend_factor,
        thickness_ratio=thickness_ratio,
    )

