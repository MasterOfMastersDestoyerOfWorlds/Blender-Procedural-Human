"""
Finger Geometry Nodes setup for Procedural Human Generator
"""

from dataclasses import dataclass
import bpy
from procedural_human.blender_const import NODE_WIDTH
from procedural_human.geo_node_groups.closures import (
    FloatCurveClosure,
    create_float_curve_closure,
    create_flat_float_curve_closure,
)
from procedural_human.hand.finger.finger import FingerData
from procedural_human.hand.finger.finger_segment.finger_segment_const import (
    SEGMENT_SAMPLE_COUNT,
)
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
)
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
    JointSegmentProperties,
)
from procedural_human.hand.finger.finger_segment.joint_segment_nodes import (
    create_joint_between_segments,
)
from procedural_human.hand.finger.finger_types import (
    ensure_finger_type,
)
from procedural_human.hand.finger.finger_nail.finger_nail_nodes import (
    attach_fingernail_to_distal_segment,
)
from procedural_human.hand.finger.finger_segment.finger_segment_nodes import (
    create_finger_segment_node_group,
)
from procedural_human.utils import setup_node_group_interface


@dataclass
class SegmentNodeData:
    name: str
    node: object
    index: int
    radius: float
    length: float
    frame: object
    x_closure: FloatCurveClosure
    y_closure: FloatCurveClosure
    abs_x: float
    abs_y: float


@dataclass
class JointNodeData:
    name: str
    node: object
    index: int
    closures: list
    abs_x: float
    abs_y: float


def create_finger_nodes(
    node_group,
    finger: FingerData,
):
    setup_node_group_interface(node_group)
    finger_type = ensure_finger_type(finger.finger_type)

    input_node = node_group.nodes.new("NodeGroupInput")
    input_node.label = "Input"
    output_node = node_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"

    input_node.location = (-1000, 0)
    output_node.location = (1200, 0)

    if finger.segment_lengths is None:
        segment_lengths = [
            finger.total_length / finger.num_segments
        ] * finger.num_segments

    starting_point = node_group.nodes.new("GeometryNodeCurvePrimitiveLine")
    starting_point.label = "Starting Axis"
    starting_point.location = (-700, 400)
    starting_point.inputs["Start"].default_value = (0.0, 0.0, 0.0)
    starting_point.inputs["End"].default_value = (0.0, 0.0, 0.0)

    segment_types = [SegmentType.PROXIMAL, SegmentType.MIDDLE, SegmentType.DISTAL]
    segment_profile_meta = {}

    for seg_type in SegmentType:
        segment_profile_meta[seg_type] = {
            "start": 1.0,
            "end": 0.85,
        }

    segment_node_instances = []
    previous_segment_output = starting_point.outputs["Curve"]
    next_segment_radius = None

    segment_offset = 300

    segment_radii = []
    continuity_ratio = (
        segment_profile_meta[SegmentType.PROXIMAL]["end"]
        / segment_profile_meta[SegmentType.PROXIMAL]["start"]
    )

    for seg_idx in range(finger.num_segments):
        if seg_idx == 0:
            seg_length = finger.segment_lengths[seg_idx]
            seg_radius = seg_length * 0.5
        else:
            prev_radius = segment_radii[seg_idx - 1]
            seg_radius = prev_radius * continuity_ratio
        segment_radii.append(seg_radius)

    for seg_idx in range(finger.num_segments):
        seg_length = finger.segment_lengths[seg_idx]
        seg_radius = segment_radii[seg_idx]
        if finger.num_segments == 2:
            segment_enum = SegmentType.PROXIMAL if seg_idx == 0 else SegmentType.DISTAL
        else:
            segment_enum = (
                segment_types[seg_idx]
                if seg_idx < len(segment_types)
                else segment_types[-1]
            )
        if isinstance(segment_enum, SegmentType):
            seg_name = segment_enum.value.capitalize()
        else:
            seg_name = str(segment_enum)

        segment_group = create_finger_segment_node_group(
            f"{finger_type.value}_{seg_name}_Segment_Group",
            seg_length,
            seg_radius,
            segment_type=segment_enum,
        )

        x_closure: FloatCurveClosure = create_float_curve_closure(
            node_group.nodes,
            node_group.links,
            label=f"{seg_name} X Profile",
            location=(-500, segment_offset),
        )

        y_closure: FloatCurveClosure = create_float_curve_closure(
            node_group.nodes,
            node_group.links,
            label=f"{seg_name} Y Profile",
            location=(-500, x_closure.min_y() - 100),
        )

        segment_instance = node_group.nodes.new("GeometryNodeGroup")
        segment_instance.node_tree = segment_group
        segment_instance.label = f"{seg_name} Segment"
        segment_abs_x = x_closure.out_node.location[0] + x_closure.out_node.width + 100
        segment_abs_y = y_closure.out_node.location[1]
        segment_instance.location = (segment_abs_x, segment_abs_y)

        node_frame = node_group.nodes.new("NodeFrame")
        node_frame.location = (-500, segment_offset)
        node_frame.label = f"{seg_name}"
        node_frame.label_size = 30

        frame_nodes = [segment_instance]
        frame_nodes.extend(x_closure.nodes())
        frame_nodes.extend(y_closure.nodes())
        for node in frame_nodes:
            node.parent = node_frame

        segment_offset = y_closure.min_y() - 300

        node_group.links.new(
            x_closure.output_socket, segment_instance.inputs["X Float Curve"]
        )
        node_group.links.new(
            y_closure.output_socket, segment_instance.inputs["Y Float Curve"]
        )

        sample_count = SEGMENT_SAMPLE_COUNT
        if hasattr(bpy.context, "scene") and hasattr(
            bpy.context.scene, "procedural_finger_segment_sample_count"
        ):
            sample_count = bpy.context.scene.procedural_finger_segment_sample_count

        node_group.links.new(
            previous_segment_output, segment_instance.inputs["Geometry"]
        )
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_LENGTH.value
        ].default_value = seg_length
        segment_instance.inputs[
            FingerSegmentProperties.SAMPLE_COUNT.value
        ].default_value = sample_count
        if next_segment_radius is None:
            segment_radius_scale = seg_radius
        else:
            segment_radius_scale = next_segment_radius
        segment_instance.inputs[
            FingerSegmentProperties.SEGMENT_RADIUS.value
        ].default_value = segment_radius_scale

        profile_ratios = segment_profile_meta[segment_enum]
        continuity_ratio = (
            profile_ratios["end"] / profile_ratios["start"]
            if profile_ratios["start"] != 0
            else 1.0
        )
        current_end_radius = segment_radius_scale * continuity_ratio

        segment_node_instances.append(
            SegmentNodeData(
                name=seg_name,
                node=segment_instance,
                index=seg_idx,
                radius=segment_radius_scale,
                length=seg_length,
                frame=node_frame,
                x_closure=x_closure,
                y_closure=y_closure,
                abs_x=segment_abs_x,
                abs_y=segment_abs_y,
            )
        )

        previous_segment_output = segment_instance.outputs["Geometry"]
        next_segment_radius = current_end_radius

    joint_node_instances = []
    joint_offset = segment_offset

    for joint_idx in range(finger.num_segments - 1):
        prev_segment = segment_node_instances[joint_idx]
        next_segment = segment_node_instances[joint_idx + 1]

        joint_group = create_joint_between_segments(joint_index=joint_idx)

        joint_abs_x = (prev_segment.abs_x + next_segment.abs_x) / 2
        joint_abs_y = (prev_segment.abs_y + next_segment.abs_y) / 2

        curve_labels = ["0°", "90°", "180°", "270°"]
        joint_closures = []

        for i, angle_label in enumerate(curve_labels):
            closure = create_flat_float_curve_closure(
                node_group.nodes,
                node_group.links,
                label=f"Joint {joint_idx} {angle_label}",
                location=(-500, joint_offset),
                value=0.5,
            )
            joint_closures.append(closure)
            joint_offset = closure.min_y() - 100

        joint_instance = node_group.nodes.new("GeometryNodeGroup")
        joint_instance.node_tree = joint_group
        joint_instance.label = f"Joint {joint_idx}"
        joint_instance.location = (joint_abs_x, joint_abs_y)

        node_group.links.new(
            prev_segment.node.outputs["Geometry"],
            joint_instance.inputs[JointSegmentProperties.PREV_SEGMENT.value]
        )
        node_group.links.new(
            next_segment.node.outputs["Geometry"],
            joint_instance.inputs[JointSegmentProperties.NEXT_SEGMENT.value]
        )

        node_group.links.new(
            joint_closures[0].output_socket,
            joint_instance.inputs[JointSegmentProperties.CURVE_0.value]
        )
        node_group.links.new(
            joint_closures[1].output_socket,
            joint_instance.inputs[JointSegmentProperties.CURVE_90.value]
        )
        node_group.links.new(
            joint_closures[2].output_socket,
            joint_instance.inputs[JointSegmentProperties.CURVE_180.value]
        )
        node_group.links.new(
            joint_closures[3].output_socket,
            joint_instance.inputs[JointSegmentProperties.CURVE_270.value]
        )

        joint_node_instances.append(
            JointNodeData(
                name=f"Joint_{joint_idx}",
                node=joint_instance,
                index=joint_idx,
                closures=joint_closures,
                abs_x=joint_abs_x,
                abs_y=joint_abs_y,
            )
        )

        joint_offset -= 200

    join_geo = node_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.label = "Join All"
    join_geo.location = (1000, 0)
    node_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])

    for segment in segment_node_instances:
        node_group.links.new(
            segment.node.outputs["Geometry"], join_geo.inputs["Geometry"]
        )

    for joint in joint_node_instances:
        node_group.links.new(
            joint.node.outputs["Geometry"], join_geo.inputs["Geometry"]
        )

    node_group.links.new(join_geo.outputs["Geometry"], output_node.inputs["Geometry"])

    distal_segment = segment_node_instances[-1]
    nail_instance = attach_fingernail_to_distal_segment(
        node_group=node_group,
        distal_transform_node=distal_segment.node,
        curl_direction=finger.curl_direction,
        distal_seg_radius=distal_segment.radius,
        finger_type=finger_type,
        nail_size=finger.nail_size,
        parent_frame=distal_segment.frame,
    )

    node_group.links.new(nail_instance.outputs["Geometry"], join_geo.inputs["Geometry"])

    return node_group
