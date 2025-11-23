import bpy
import math

from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)


def create_single_profile_radial_group():
    """
    Creates a node group for radial geometry with a single profile curve.
    """
    group_name = "Radial Profile (Single)"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    group.interface.new_socket(
        name="Factor", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    group.interface.new_socket(
        name="Radius", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    group.interface.new_socket(
        name="Offset", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )

    input_node = group.nodes.new("NodeGroupInput")
    input_node.location = (-400, 0)

    float_curve = group.nodes.new("ShaderNodeFloatCurve")
    float_curve.location = (-200, 0)

    group.links.new(input_node.outputs["Factor"], float_curve.inputs["Value"])

    mult = group.nodes.new("ShaderNodeMath")
    mult.operation = "MULTIPLY"
    mult.location = (0, 0)

    group.links.new(float_curve.outputs["Value"], mult.inputs[0])
    group.links.new(input_node.outputs["Radius"], mult.inputs[1])

    output_node = group.nodes.new("NodeGroupOutput")
    output_node.location = (200, 0)

    group.links.new(mult.outputs["Value"], output_node.inputs["Offset"])

    return group
