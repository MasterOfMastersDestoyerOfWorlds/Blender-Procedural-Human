import bpy
import math

from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group


def create_single_profile_radial_group():
    """
    Creates a node group for radial geometry with a single profile curve.
    """
    group_name = "Radial Profile (Single)"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    input_node.label = "Inputs"

    float_curve = group.nodes.new("ShaderNodeFloatCurve")
    float_curve.label = "Profile Curve"

    group.links.new(input_node.outputs["Factor"], float_curve.inputs["Value"])

    mult = group.nodes.new("ShaderNodeMath")
    mult.label = "Scale by Radius"
    mult.operation = "MULTIPLY"

    group.links.new(float_curve.outputs["Value"], mult.inputs[0])
    group.links.new(input_node.outputs["Radius"], mult.inputs[1])

    output_node = group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"

    group.links.new(mult.outputs["Value"], output_node.inputs["Offset"])

    auto_layout_nodes(group)
    return group
