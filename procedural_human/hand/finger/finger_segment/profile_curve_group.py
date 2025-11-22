import bpy
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_segment.finger_segment_curve_utils import (
    get_default_profile_curve_from_data,
)
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    ProfileType,
)


def create_profile_curve_offset_node_group(
    axis_name,
    parent_input_node,
    parent_node_group,
    length_clamp_node,
    angle_param_node,
    segment_length,
    segment_type,
):

    profile_offset_group = bpy.data.node_groups.new(
        f"{axis_name} Profile Curve Offset", "GeometryNodeTree"
    )
    profile_offset_group.interface.new_socket(
        name="Length Clamp",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    profile_offset_group.interface.new_socket(
        name="Sin Theta",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    profile_offset_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    profile_offset_group.interface.new_socket(
        name="Y Profile",
        in_out="INPUT",
        socket_type="NodeSocketGeometry",
    )
    profile_offset_group.interface.new_socket(
        name="Offset",
        in_out="OUTPUT",
        socket_type="NodeSocketFloat",
    )
    profile_offset_group.interface.new_socket(
        name="Point Count",
        in_out="OUTPUT",
        socket_type="NodeSocketInt",
    )
    profile_offset_group.interface.new_socket(
        name="Y Profile",
        in_out="OUTPUT",
        socket_type="NodeSocketGeometry",
    )

    input_node = profile_offset_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-1400, 0)

    scene = bpy.context.scene

    y_profile_obj = get_default_profile_curve_from_data(
        scene, segment_type, ProfileType.Y_PROFILE, segment_length, 1.0
    )

    y_profile_info = profile_offset_group.nodes.new("GeometryNodeObjectInfo")
    y_profile_info.label = "Y Profile"
    y_profile_info.location = (-200, -350)
    y_profile_info.inputs["Object"].default_value = y_profile_obj
    y_profile_info.transform_space = "ORIGINAL"

    domain_size_y = profile_offset_group.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_y.label = "Y Point Count"
    domain_size_y.location = (-50, -300)
    domain_size_y.component = "CURVE"
    profile_offset_group.links.new(
        y_profile_info.outputs["Geometry"], domain_size_y.inputs["Geometry"]
    )

    
    sample_y = profile_offset_group.nodes.new("GeometryNodeSampleCurve")
    sample_y.label = "Sample Y Profile"
    sample_y.location = (1000, -360)
    sample_y.mode = "FACTOR"
    sample_y.data_type = "FLOAT_VECTOR"
    profile_offset_group.links.new(
        y_profile_info.outputs["Geometry"], sample_y.inputs["Curves"]
    )
    profile_offset_group.links.new(
        input_node.outputs["Length Clamp"], sample_y.inputs["Factor"]
    )

    
    separate_y_sample = profile_offset_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_y_sample.label = "Extract Y Radius"
    separate_y_sample.location = (1200, -360)
    profile_offset_group.links.new(
        sample_y.outputs["Position"], separate_y_sample.inputs["Vector"]
    )

    y_radius_abs = profile_offset_group.nodes.new("ShaderNodeMath")
    y_radius_abs.label = "Y Radius Abs"
    y_radius_abs.location = (1400, -360)
    y_radius_abs.operation = "ABSOLUTE"
    profile_offset_group.links.new(
        separate_y_sample.outputs["Y"], y_radius_abs.inputs[0]
    )

    y_radius_scale = profile_offset_group.nodes.new("ShaderNodeMath")
    y_radius_scale.label = "Scale Y Radius"
    y_radius_scale.location = (1400, -340)
    y_radius_scale.operation = "MULTIPLY"
    profile_offset_group.links.new(
        y_radius_abs.outputs["Value"], y_radius_scale.inputs[0]
    )
    profile_offset_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        y_radius_scale.inputs[1],
    )

    y_offset = profile_offset_group.nodes.new("ShaderNodeMath")
    y_offset.label = "Y Offset"
    y_offset.location = (1800, -300)
    y_offset.operation = "MULTIPLY"
    profile_offset_group.links.new(y_radius_scale.outputs["Value"], y_offset.inputs[0])
    profile_offset_group.links.new(input_node.outputs["Sin Theta"], y_offset.inputs[1])
    output_node = profile_offset_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (2600, 0)
    profile_offset_group.links.new(
        y_offset.outputs["Value"], output_node.inputs["Offset"]
    )
    profile_offset_group.links.new(
        domain_size_y.outputs["Point Count"], output_node.inputs["Point Count"]
    )

    profile_offset_group.links.new(
        y_profile_info.outputs["Geometry"], output_node.inputs["Y Profile"]
    )

    profile_offset_group_instance = parent_node_group.nodes.new("GeometryNodeGroup")
    profile_offset_group_instance.node_tree = profile_offset_group
    profile_offset_group_instance.label = f"{axis_name} Profile Curve Offset"
    profile_offset_group_instance.location = (0, 0)
    parent_node_group.links.new(
        length_clamp_node.outputs["Result"],
        profile_offset_group_instance.inputs["Length Clamp"],
    )
    parent_node_group.links.new(
        parent_input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        profile_offset_group_instance.inputs[
            FingerSegmentProperties.SEGMENT_RADIUS.value
        ],
    )
    parent_node_group.links.new(
        angle_param_node.outputs["Value"],
        profile_offset_group_instance.inputs["Sin Theta"],
    )
    return profile_offset_group_instance
