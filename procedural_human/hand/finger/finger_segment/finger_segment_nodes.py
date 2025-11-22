import bpy
import math
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
)
from procedural_human.utils import setup_node_group_interface
from procedural_human.geo_node_groups.radial import create_dual_profile_radial_group


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
    sample_count_socket.default_value = 64

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
    
    # Radial Profile Lookup
    radial_group = create_dual_profile_radial_group()
    radial_instance = segment_group.nodes.new("GeometryNodeGroup")
    radial_instance.node_tree = radial_group
    radial_instance.label = "Radial Profile (Dual)"
    radial_instance.location = (1400, -200)
    
    segment_group.links.new(length_clamp.outputs["Result"], radial_instance.inputs["Factor"])
    segment_group.links.new(theta_node.outputs["Value"], radial_instance.inputs["Angle"])
    segment_group.links.new(input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value], radial_instance.inputs["Radius"])

    # Set Grid Resolution from Sample Count
    sample_count_node = segment_group.nodes.new("FunctionNodeInputInt") # Not strictly needed if direct link
    # Just link input directly
    segment_group.links.new(input_node.outputs[FingerSegmentProperties.SAMPLE_COUNT.value], grid.inputs["Vertices Y"])

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

    # The radial instance output is a single Offset value (radius offset)
    # We need to convert this back to X/Y coordinates: X=Offset*cos, Y=Offset*sin
    # BUT wait, the previous logic had separate X and Y offsets?
    # Original Logic: 
    # x_offset = X(t) * Radius * cos(theta)
    # y_offset = Y(t) * Radius * sin(theta)
    # Final Pos = (x_offset, y_offset, z)
    
    # The NEW create_dual_profile_radial_group returns:
    # Offset = Radius * sqrt((X(t)*cos)^2 + (Y(t)*sin)^2)
    # This is the MAGNITUDE (radius) at that angle.
    # So Final X = Offset * cos(theta)
    # Final Y = Offset * sin(theta)
    # Let's implement this reconstruction.
    
    cos_theta = segment_group.nodes.new("ShaderNodeMath")
    cos_theta.label = "cos(θ)"
    cos_theta.location = (1600, -100)
    cos_theta.operation = "COSINE"
    segment_group.links.new(theta_node.outputs["Value"], cos_theta.inputs[0])
    
    sin_theta = segment_group.nodes.new("ShaderNodeMath")
    sin_theta.label = "sin(θ)"
    sin_theta.location = (1600, -250)
    sin_theta.operation = "SINE"
    segment_group.links.new(theta_node.outputs["Value"], sin_theta.inputs[0])
    
    final_x = segment_group.nodes.new("ShaderNodeMath")
    final_x.label = "Final X"
    final_x.location = (1800, -100)
    final_x.operation = "MULTIPLY"
    segment_group.links.new(radial_instance.outputs["Offset"], final_x.inputs[0])
    segment_group.links.new(cos_theta.outputs["Value"], final_x.inputs[1])
    
    final_y = segment_group.nodes.new("ShaderNodeMath")
    final_y.label = "Final Y"
    final_y.location = (1800, -250)
    final_y.operation = "MULTIPLY"
    segment_group.links.new(radial_instance.outputs["Offset"], final_y.inputs[0])
    segment_group.links.new(sin_theta.outputs["Value"], final_y.inputs[1])

    final_pos = segment_group.nodes.new("ShaderNodeCombineXYZ")
    final_pos.label = "Final Position"
    final_pos.location = (2000, -300)
    segment_group.links.new(final_x.outputs["Value"], final_pos.inputs["X"])
    segment_group.links.new(final_y.outputs["Value"], final_pos.inputs["Y"])
    segment_group.links.new(z_position.outputs["Value"], final_pos.inputs["Z"])
    
    apply_shape = segment_group.nodes.new("GeometryNodeSetPosition")
    apply_shape.label = "Apply Shape"
    apply_shape.location = (2200, 0)
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
