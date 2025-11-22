import bpy
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)


def create_float_curve_profile_node_group(
    axis_name,
    parent_input_node,
    parent_node_group,
    length_clamp_node,
    angle_param_node,
    segment_length,
    segment_type,
):
    """
    Creates a node group that uses a Float Curve to define the profile offset.
    Replaces the geometry-based profile lookup.
    """

    group_name = f"{axis_name} Float Curve Profile"

    
    profile_group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    
    profile_group.interface.new_socket(
        name="Length Clamp", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    profile_group.interface.new_socket(
        name="Sin Theta", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    profile_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    
    profile_group.interface.new_socket(
        name="Y Profile", in_out="INPUT", socket_type="NodeSocketGeometry"
    )

    profile_group.interface.new_socket(
        name="Offset", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )
    profile_group.interface.new_socket(
        name="Point Count", in_out="OUTPUT", socket_type="NodeSocketInt"
    )
    profile_group.interface.new_socket(
        name="Y Profile", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )

    
    input_node = profile_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-800, 0)

    
    float_curve = profile_group.nodes.new("ShaderNodeFloatCurve")
    float_curve.label = f"{axis_name} Profile Shape"
    float_curve.location = (-400, 0)
    
    
    
    
    
    
    
    
    curve_points = float_curve.mapping.curves[0].points
    
    curve_points[0].location = (0.0, 1.0)
    curve_points[1].location = (1.0, 1.0)
    
    
    
    profile_group.links.new(
        input_node.outputs["Length Clamp"], float_curve.inputs["Value"]
    )

    
    mult_radius = profile_group.nodes.new("ShaderNodeMath")
    mult_radius.label = "Scale by Radius"
    mult_radius.location = (-200, 0)
    mult_radius.operation = "MULTIPLY"
    
    profile_group.links.new(float_curve.outputs["Value"], mult_radius.inputs[0])
    profile_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        mult_radius.inputs[1]
    )

    
    final_mult = profile_group.nodes.new("ShaderNodeMath")
    final_mult.label = "Apply Angle Factor"
    final_mult.location = (0, 0)
    final_mult.operation = "MULTIPLY"

    profile_group.links.new(mult_radius.outputs["Value"], final_mult.inputs[0])
    profile_group.links.new(input_node.outputs["Sin Theta"], final_mult.inputs[1])

    
    output_node = profile_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (200, 0)

    profile_group.links.new(final_mult.outputs["Value"], output_node.inputs["Offset"])
    
    
    profile_group.links.new(
        input_node.outputs["Y Profile"], output_node.inputs["Y Profile"]
    )

    
    
    zero_int = profile_group.nodes.new("FunctionNodeInputInt")
    zero_int.integer = 0
    zero_int.location = (0, -200)
    profile_group.links.new(zero_int.outputs["Integer"], output_node.inputs["Point Count"])

    
    profile_instance = parent_node_group.nodes.new("GeometryNodeGroup")
    profile_instance.node_tree = profile_group
    profile_instance.label = group_name
    
    
    
    profile_instance.location = (0, 0) 

    
    parent_node_group.links.new(
        length_clamp_node.outputs["Result"],
        profile_instance.inputs["Length Clamp"],
    )
    parent_node_group.links.new(
        parent_input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        profile_instance.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
    )
    parent_node_group.links.new(
        angle_param_node.outputs["Value"],
        profile_instance.inputs["Sin Theta"],
    )
    
    
    

    return profile_instance


