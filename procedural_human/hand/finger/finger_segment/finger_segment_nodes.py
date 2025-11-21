import bpy
import math
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_segment.finger_segment_curve_utils import (
    get_default_profile_curve,
)
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
    ProfileType,
)
from procedural_human.utils import setup_node_group_interface


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

    x_profile_property_name = f"procedural_segment_{segment_type.value}_x_profile"
    if hasattr(scene, x_profile_property_name):
        x_profile_obj = getattr(scene, x_profile_property_name)
    else:
        x_profile_obj = None

    if not x_profile_obj:
        x_profile_name = f"{segment_type.value}_{ProfileType.X_PROFILE.value}"
        if x_profile_name in bpy.data.objects:
            x_profile_obj = bpy.data.objects[x_profile_name]
        else:
            x_profile_obj = get_default_profile_curve(
                segment_type, ProfileType.X_PROFILE, segment_length, 1.0
            )
            bpy.context.scene.collection.objects.link(x_profile_obj)

    y_profile_property_name = f"procedural_segment_{segment_type.value}_y_profile"
    if hasattr(scene, y_profile_property_name):
        y_profile_obj = getattr(scene, y_profile_property_name)
    else:
        y_profile_obj = None

    if not y_profile_obj:
        y_profile_name = f"{segment_type.value}_{ProfileType.Y_PROFILE.value}"
        if y_profile_name in bpy.data.objects:
            y_profile_obj = bpy.data.objects[y_profile_name]
        else:
            y_profile_obj = get_default_profile_curve(
                segment_type, ProfileType.Y_PROFILE, segment_length, 1.0
            )
            bpy.context.scene.collection.objects.link(y_profile_obj)

    x_profile_info = segment_group.nodes.new("GeometryNodeObjectInfo")
    x_profile_info.label = "X Profile"
    x_profile_info.location = (-200, -200)
    x_profile_info.inputs["Object"].default_value = x_profile_obj
    x_profile_info.transform_space = "ORIGINAL"

    y_profile_info = segment_group.nodes.new("GeometryNodeObjectInfo")
    y_profile_info.label = "Y Profile"
    y_profile_info.location = (-200, -350)
    y_profile_info.inputs["Object"].default_value = y_profile_obj
    y_profile_info.transform_space = "ORIGINAL"

    # Calculate Grid Resolution
    # Get point counts from profiles
    domain_size_x = segment_group.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_x.label = "X Point Count"
    domain_size_x.location = (-50, -50)
    domain_size_x.component = 'CURVE'
    segment_group.links.new(x_profile_info.outputs["Geometry"], domain_size_x.inputs["Geometry"])
    
    domain_size_y = segment_group.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_y.label = "Y Point Count"
    domain_size_y.location = (-50, -300)
    domain_size_y.component = 'CURVE'
    segment_group.links.new(y_profile_info.outputs["Geometry"], domain_size_y.inputs["Geometry"])
    
    max_points = segment_group.nodes.new("ShaderNodeMath")
    max_points.label = "Max Points"
    max_points.location = (150, -150)
    max_points.operation = 'MAXIMUM'
    segment_group.links.new(domain_size_x.outputs["Point Count"], max_points.inputs[0])
    segment_group.links.new(domain_size_y.outputs["Point Count"], max_points.inputs[1])
    
    final_count = segment_group.nodes.new("ShaderNodeMath")
    final_count.label = "Final Sample Count"
    final_count.location = (350, -50)
    final_count.operation = 'MAXIMUM'
    segment_group.links.new(max_points.outputs["Value"], final_count.inputs[0])
    segment_group.links.new(input_node.outputs[FingerSegmentProperties.SAMPLE_COUNT.value], final_count.inputs[1])

    grid = segment_group.nodes.new("GeometryNodeMeshGrid")
    grid.label = "Parameter Grid"
    grid.location = (550, -100)
    grid.inputs["Vertices X"].default_value = 64
    # grid.inputs["Vertices Y"].default_value = 64 # Driven by logic
    segment_group.links.new(final_count.outputs["Value"], grid.inputs["Vertices Y"])
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

    # Sample X profile - using position vectors
    sample_x = segment_group.nodes.new("GeometryNodeSampleCurve")
    sample_x.label = "Sample X Profile"
    sample_x.location = (1000, -180)
    sample_x.mode = "FACTOR"
    sample_x.data_type = "FLOAT_VECTOR"
    segment_group.links.new(
        x_profile_info.outputs["Geometry"], sample_x.inputs["Curves"]
    )
    segment_group.links.new(length_clamp.outputs["Result"], sample_x.inputs["Factor"])
    
    # Extract X component as radius
    separate_x_sample = segment_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_x_sample.label = "Extract X Radius"
    separate_x_sample.location = (1200, -180)
    segment_group.links.new(sample_x.outputs["Position"], separate_x_sample.inputs["Vector"])

    # Sample Y profile - using position vectors
    sample_y = segment_group.nodes.new("GeometryNodeSampleCurve")
    sample_y.label = "Sample Y Profile"
    sample_y.location = (1000, -360)
    sample_y.mode = "FACTOR"
    sample_y.data_type = "FLOAT_VECTOR"
    segment_group.links.new(
        y_profile_info.outputs["Geometry"], sample_y.inputs["Curves"]
    )
    segment_group.links.new(length_clamp.outputs["Result"], sample_y.inputs["Factor"])
    
    # Extract Y component as radius
    separate_y_sample = segment_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_y_sample.label = "Extract Y Radius"
    separate_y_sample.location = (1200, -360)
    segment_group.links.new(sample_y.outputs["Position"], separate_y_sample.inputs["Vector"])

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

    sin_theta = segment_group.nodes.new("ShaderNodeMath")
    sin_theta.label = "sin(θ)"
    sin_theta.location = (1400, -300)
    sin_theta.operation = "SINE"
    segment_group.links.new(theta_node.outputs["Value"], sin_theta.inputs[0])

    x_radius_abs = segment_group.nodes.new("ShaderNodeMath")
    x_radius_abs.label = "X Radius Abs"
    x_radius_abs.location = (1400, -180)
    x_radius_abs.operation = "ABSOLUTE"
    segment_group.links.new(separate_x_sample.outputs["X"], x_radius_abs.inputs[0])

    y_radius_abs = segment_group.nodes.new("ShaderNodeMath")
    y_radius_abs.label = "Y Radius Abs"
    y_radius_abs.location = (1400, -360)
    y_radius_abs.operation = "ABSOLUTE"
    segment_group.links.new(separate_y_sample.outputs["Y"], y_radius_abs.inputs[0])

    x_radius_scale = segment_group.nodes.new("ShaderNodeMath")
    x_radius_scale.label = "Scale X Radius"
    x_radius_scale.location = (1400, -160)
    x_radius_scale.operation = "MULTIPLY"
    segment_group.links.new(x_radius_abs.outputs["Value"], x_radius_scale.inputs[0])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        x_radius_scale.inputs[1],
    )

    y_radius_scale = segment_group.nodes.new("ShaderNodeMath")
    y_radius_scale.label = "Scale Y Radius"
    y_radius_scale.location = (1400, -340)
    y_radius_scale.operation = "MULTIPLY"
    segment_group.links.new(y_radius_abs.outputs["Value"], y_radius_scale.inputs[0])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        y_radius_scale.inputs[1],
    )

    x_offset = segment_group.nodes.new("ShaderNodeMath")
    x_offset.label = "X Offset"
    x_offset.location = (1800, -120)
    x_offset.operation = "MULTIPLY"
    segment_group.links.new(x_radius_scale.outputs["Value"], x_offset.inputs[0])
    segment_group.links.new(cos_theta.outputs["Value"], x_offset.inputs[1])

    y_offset = segment_group.nodes.new("ShaderNodeMath")
    y_offset.label = "Y Offset"
    y_offset.location = (1800, -300)
    y_offset.operation = "MULTIPLY"
    segment_group.links.new(y_radius_scale.outputs["Value"], y_offset.inputs[0])
    segment_group.links.new(sin_theta.outputs["Value"], y_offset.inputs[1])

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

    combine_pos = segment_group.nodes.new("ShaderNodeCombineXYZ")
    combine_pos.label = "Final Position"
    combine_pos.location = (1800, -300)
    segment_group.links.new(x_offset.outputs["Value"], combine_pos.inputs["X"])
    segment_group.links.new(y_offset.outputs["Value"], combine_pos.inputs["Y"])
    segment_group.links.new(z_position.outputs["Value"], combine_pos.inputs["Z"])

    set_position = segment_group.nodes.new("GeometryNodeSetPosition")
    set_position.label = "Apply Shape"
    set_position.location = (2000, 0)
    segment_group.links.new(grid.outputs["Mesh"], set_position.inputs["Geometry"])
    segment_group.links.new(
        combine_pos.outputs["Vector"], set_position.inputs["Position"]
    )

    set_shade_smooth = segment_group.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.label = "Smooth Shading"
    set_shade_smooth.location = (2200, 0)
    set_shade_smooth.inputs["Shade Smooth"].default_value = True
    segment_group.links.new(
        set_position.outputs["Geometry"], set_shade_smooth.inputs["Geometry"]
    )

    join_geo = segment_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.label = "Join With Previous"
    join_geo.location = (2400, 0)
    segment_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
    segment_group.links.new(
        set_shade_smooth.outputs["Geometry"], join_geo.inputs["Geometry"]
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
