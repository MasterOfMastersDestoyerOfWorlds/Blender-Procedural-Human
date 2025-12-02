"""
Joint Segment Nodes for smooth transitions between finger segments.

Joint segments create organic transitions at knuckle locations by:
- Receiving geometry from both adjacent segments
- Sampling radius at specified positions on each segment using raycast
- Creating smooth blended geometry using quad radial profiles
"""

from enum import Enum
import bpy
from procedural_human.geo_node_groups.quad_radial import create_quad_profile_radial_group
from procedural_human.dsl.finger_segment_const import (
    SEGMENT_SAMPLE_COUNT,
)

class JointSegmentProperties(Enum):
    PREV_SEGMENT = "Previous Segment"
    NEXT_SEGMENT = "Next Segment" 
    PREV_SEGMENT_START = "Prev Segment Start"
    NEXT_SEGMENT_START = "Next Segment Start"
    CURVE_0 = "0° Float Curve"
    CURVE_90 = "90° Float Curve"
    CURVE_180 = "180° Float Curve"
    CURVE_270 = "270° Float Curve"
    SAMPLE_COUNT = "Sample Count"

DEFAULT_PREV_START = 0.8
DEFAULT_NEXT_START = 0.2
JOINT_SAMPLE_COUNT = 8


def create_joint_segment_node_group(
    name: str,
    prev_start: float = DEFAULT_PREV_START,
    next_start: float = DEFAULT_NEXT_START,
):
    joint_group = bpy.data.node_groups.new(name, "GeometryNodeTree")

    joint_group.interface.new_socket(
        name=JointSegmentProperties.PREV_SEGMENT.value,
        in_out="INPUT",
        socket_type="NodeSocketGeometry",
    )
    joint_group.interface.new_socket(
        name=JointSegmentProperties.NEXT_SEGMENT.value,
        in_out="INPUT",
        socket_type="NodeSocketGeometry",
    )

    prev_start_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.PREV_SEGMENT_START.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    prev_start_socket.default_value = prev_start
    prev_start_socket.min_value = 0.0
    prev_start_socket.max_value = 1.0

    next_start_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.NEXT_SEGMENT_START.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    next_start_socket.default_value = next_start
    next_start_socket.min_value = 0.0
    next_start_socket.max_value = 1.0

    joint_group.interface.new_socket(
        name=JointSegmentProperties.CURVE_0.value,
        in_out="INPUT",
        socket_type="NodeSocketClosure",
    )
    joint_group.interface.new_socket(
        name=JointSegmentProperties.CURVE_90.value,
        in_out="INPUT",
        socket_type="NodeSocketClosure",
    )
    joint_group.interface.new_socket(
        name=JointSegmentProperties.CURVE_180.value,
        in_out="INPUT",
        socket_type="NodeSocketClosure",
    )
    joint_group.interface.new_socket(
        name=JointSegmentProperties.CURVE_270.value,
        in_out="INPUT",
        socket_type="NodeSocketClosure",
    )

    sample_count_socket = joint_group.interface.new_socket(
        name=JointSegmentProperties.SAMPLE_COUNT.value,
        in_out="INPUT",
        socket_type="NodeSocketInt",
    )
    sample_count_socket.default_value = JOINT_SAMPLE_COUNT

    joint_group.interface.new_socket(
        name="Geometry",
        in_out="OUTPUT",
        socket_type="NodeSocketGeometry",
    )

    input_node = joint_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-1800, 0)

    prev_bbox = joint_group.nodes.new("GeometryNodeBoundBox")
    prev_bbox.label = "Prev Bounds"
    prev_bbox.location = (-1600, 300)
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.PREV_SEGMENT.value],
        prev_bbox.inputs["Geometry"]
    )

    next_bbox = joint_group.nodes.new("GeometryNodeBoundBox")
    next_bbox.label = "Next Bounds"
    next_bbox.location = (-1600, -100)
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.NEXT_SEGMENT.value],
        next_bbox.inputs["Geometry"]
    )

    prev_max = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    prev_max.label = "Prev Max"
    prev_max.location = (-1400, 350)
    joint_group.links.new(prev_bbox.outputs["Max"], prev_max.inputs["Vector"])

    prev_min = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    prev_min.label = "Prev Min"
    prev_min.location = (-1400, 250)
    joint_group.links.new(prev_bbox.outputs["Min"], prev_min.inputs["Vector"])

    next_max = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    next_max.label = "Next Max"
    next_max.location = (-1400, -50)
    joint_group.links.new(next_bbox.outputs["Max"], next_max.inputs["Vector"])

    next_min = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    next_min.label = "Next Min"
    next_min.location = (-1400, -150)
    joint_group.links.new(next_bbox.outputs["Min"], next_min.inputs["Vector"])

    prev_length = joint_group.nodes.new("ShaderNodeMath")
    prev_length.label = "Prev Length"
    prev_length.operation = "SUBTRACT"
    prev_length.location = (-1200, 300)
    joint_group.links.new(prev_max.outputs["Z"], prev_length.inputs[0])
    joint_group.links.new(prev_min.outputs["Z"], prev_length.inputs[1])

    next_length = joint_group.nodes.new("ShaderNodeMath")
    next_length.label = "Next Length"
    next_length.operation = "SUBTRACT"
    next_length.location = (-1200, -100)
    joint_group.links.new(next_max.outputs["Z"], next_length.inputs[0])
    joint_group.links.new(next_min.outputs["Z"], next_length.inputs[1])

    prev_sample_z = joint_group.nodes.new("ShaderNodeMath")
    prev_sample_z.label = "Prev Sample Z"
    prev_sample_z.operation = "MULTIPLY_ADD"
    prev_sample_z.location = (-1000, 300)
    joint_group.links.new(prev_length.outputs["Value"], prev_sample_z.inputs[0])
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.PREV_SEGMENT_START.value],
        prev_sample_z.inputs[1]
    )
    joint_group.links.new(prev_min.outputs["Z"], prev_sample_z.inputs[2])

    next_sample_z = joint_group.nodes.new("ShaderNodeMath")
    next_sample_z.label = "Next Sample Z"
    next_sample_z.operation = "MULTIPLY_ADD"
    next_sample_z.location = (-1000, -100)
    joint_group.links.new(next_length.outputs["Value"], next_sample_z.inputs[0])
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.NEXT_SEGMENT_START.value],
        next_sample_z.inputs[1]
    )
    joint_group.links.new(next_min.outputs["Z"], next_sample_z.inputs[2])

    prev_ray_origin = joint_group.nodes.new("ShaderNodeCombineXYZ")
    prev_ray_origin.label = "Prev Ray Origin"
    prev_ray_origin.location = (-800, 350)
    prev_ray_origin.inputs["X"].default_value = 100.0
    prev_ray_origin.inputs["Y"].default_value = 0.0
    joint_group.links.new(prev_sample_z.outputs["Value"], prev_ray_origin.inputs["Z"])

    prev_raycast = joint_group.nodes.new("GeometryNodeRaycast")
    prev_raycast.label = "Prev Raycast"
    prev_raycast.location = (-600, 350)
    prev_raycast.inputs["Ray Direction"].default_value = (-1.0, 0.0, 0.0)
    prev_raycast.inputs["Ray Length"].default_value = 200.0
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.PREV_SEGMENT.value],
        prev_raycast.inputs["Target Geometry"]
    )
    joint_group.links.new(prev_ray_origin.outputs["Vector"], prev_raycast.inputs["Source Position"])

    prev_hit_sep = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    prev_hit_sep.label = "Prev Hit X"
    prev_hit_sep.location = (-400, 350)
    joint_group.links.new(prev_raycast.outputs["Hit Position"], prev_hit_sep.inputs["Vector"])

    prev_radius = joint_group.nodes.new("ShaderNodeMath")
    prev_radius.label = "Prev Radius"
    prev_radius.operation = "ABSOLUTE"
    prev_radius.location = (-200, 350)
    joint_group.links.new(prev_hit_sep.outputs["X"], prev_radius.inputs[0])

    next_ray_origin = joint_group.nodes.new("ShaderNodeCombineXYZ")
    next_ray_origin.label = "Next Ray Origin"
    next_ray_origin.location = (-800, -50)
    next_ray_origin.inputs["X"].default_value = 100.0
    next_ray_origin.inputs["Y"].default_value = 0.0
    joint_group.links.new(next_sample_z.outputs["Value"], next_ray_origin.inputs["Z"])

    next_raycast = joint_group.nodes.new("GeometryNodeRaycast")
    next_raycast.label = "Next Raycast"
    next_raycast.location = (-600, -50)
    next_raycast.inputs["Ray Direction"].default_value = (-1.0, 0.0, 0.0)
    next_raycast.inputs["Ray Length"].default_value = 200.0
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.NEXT_SEGMENT.value],
        next_raycast.inputs["Target Geometry"]
    )
    joint_group.links.new(next_ray_origin.outputs["Vector"], next_raycast.inputs["Source Position"])

    next_hit_sep = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    next_hit_sep.label = "Next Hit X"
    next_hit_sep.location = (-400, -50)
    joint_group.links.new(next_raycast.outputs["Hit Position"], next_hit_sep.inputs["Vector"])

    next_radius = joint_group.nodes.new("ShaderNodeMath")
    next_radius.label = "Next Radius"
    next_radius.operation = "ABSOLUTE"
    next_radius.location = (-200, -50)
    joint_group.links.new(next_hit_sep.outputs["X"], next_radius.inputs[0])

    joint_length = joint_group.nodes.new("ShaderNodeMath")
    joint_length.label = "Joint Length"
    joint_length.operation = "SUBTRACT"
    joint_length.location = (0, 100)
    joint_group.links.new(next_sample_z.outputs["Value"], joint_length.inputs[0])
    joint_group.links.new(prev_sample_z.outputs["Value"], joint_length.inputs[1])

    grid = joint_group.nodes.new("GeometryNodeMeshGrid")
    grid.label = "Joint Grid"
    grid.location = (200, -200)
    grid.inputs["Vertices X"].default_value = SEGMENT_SAMPLE_COUNT
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.SAMPLE_COUNT.value],
        grid.inputs["Vertices Y"]
    )

    grid_pos = joint_group.nodes.new("GeometryNodeInputPosition")
    grid_pos.label = "Grid Position"
    grid_pos.location = (400, -300)

    sep_grid = joint_group.nodes.new("ShaderNodeSeparateXYZ")
    sep_grid.label = "Grid XY"
    sep_grid.location = (600, -300)
    joint_group.links.new(grid_pos.outputs["Position"], sep_grid.inputs["Vector"])

    t_param = joint_group.nodes.new("ShaderNodeMath")
    t_param.label = "t (0-1)"
    t_param.operation = "ADD"
    t_param.inputs[1].default_value = 0.5
    t_param.location = (800, -350)
    joint_group.links.new(sep_grid.outputs["Y"], t_param.inputs[0])

    t_clamp = joint_group.nodes.new("ShaderNodeClamp")
    t_clamp.label = "Clamp t"
    t_clamp.location = (1000, -350)
    joint_group.links.new(t_param.outputs["Value"], t_clamp.inputs["Value"])

    radius_lerp = joint_group.nodes.new("ShaderNodeMix")
    radius_lerp.data_type = "FLOAT"
    radius_lerp.label = "Lerp Radius"
    radius_lerp.location = (200, 200)
    joint_group.links.new(t_clamp.outputs["Result"], radius_lerp.inputs["Factor"])
    joint_group.links.new(prev_radius.outputs["Value"], radius_lerp.inputs["A"])
    joint_group.links.new(next_radius.outputs["Value"], radius_lerp.inputs["B"])

    quad_radial = create_quad_profile_radial_group("Joint")
    quad_instance = joint_group.nodes.new("GeometryNodeGroup")
    quad_instance.node_tree = quad_radial
    quad_instance.label = "Quad Radial"
    quad_instance.location = (600, 100)

    joint_group.links.new(radius_lerp.outputs["Result"], quad_instance.inputs["Radius"])
    joint_group.links.new(prev_sample_z.outputs["Value"], quad_instance.inputs["Z Position"])
    joint_group.links.new(joint_length.outputs["Value"], quad_instance.inputs["Segment Length"])
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.CURVE_0.value],
        quad_instance.inputs["0° Float Curve"]
    )
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.CURVE_90.value],
        quad_instance.inputs["90° Float Curve"]
    )
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.CURVE_180.value],
        quad_instance.inputs["180° Float Curve"]
    )
    joint_group.links.new(
        input_node.outputs[JointSegmentProperties.CURVE_270.value],
        quad_instance.inputs["270° Float Curve"]
    )

    set_pos = joint_group.nodes.new("GeometryNodeSetPosition")
    set_pos.label = "Apply Position"
    set_pos.location = (800, 0)
    joint_group.links.new(grid.outputs["Mesh"], set_pos.inputs["Geometry"])
    joint_group.links.new(quad_instance.outputs["Position"], set_pos.inputs["Position"])

    output_node = joint_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (1000, 0)
    joint_group.links.new(set_pos.outputs["Geometry"], output_node.inputs["Geometry"])

    return joint_group


def create_joint_between_segments(
    joint_index: int,
    prev_start: float = DEFAULT_PREV_START,
    next_start: float = DEFAULT_NEXT_START,
):
    joint_name = f"Joint_{joint_index}_Segment_Group"
    return create_joint_segment_node_group(
        name=joint_name,
        prev_start=prev_start,
        next_start=next_start,
    )
