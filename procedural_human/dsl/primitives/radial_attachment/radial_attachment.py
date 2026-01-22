import math
from typing import Optional, Literal
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from procedural_human.decorators.dsl_primitive_decorator import (
    dsl_helper,
    dsl_primitive,
)
from procedural_human.dsl.primitives.dual_radial.dual_radial import DualRadial
from procedural_human.dsl.primitives.primitives import GenerationContext, ProfileType
import bpy
from procedural_human.dsl.primitives.radial_attachment.finger_nail_nodes import (
    create_fingernail_node_group,
)
from procedural_human.geo_node_groups.closures import create_float_curve_closure


@dsl_primitive
@dataclass
class RadialAttachment:
    """
    Terminal attachment (like fingernail) that attaches to segment end.

    Maps to: procedural_human/hand/finger/finger_nail/finger_nail_nodes.py

    Args:
        type: The profile type to use for the attachment
        size_ratio: Width ratio of nail relative to segment radius
        curl_axis: Curl direction axis (X, Y, or Z) - center of radial attachment
        attachment_position: Position along segment (0-1) to sample radius for sizing (default 0.8)
        wrap_amount: Angular coverage around curl axis in radians (0 to 2π, default π/2)
        height_position: Position along segment length (0-1) to derive height from curve (default 0.5)
        max_thickness_mm: Maximum thickness of the attachment in millimeters (default 1.0)
    """

    type: type = DualRadial
    size_ratio: float = 0.3
    curl_axis: Literal["X", "Y", "Z"] = "Y"
    attachment_position: float = 0.8
    wrap_amount: float = math.pi / 2  # π/2 radians = 90 degrees
    height_position: float = 0.5
    max_thickness_mm: float = 1.0
    _naming_context: Optional[List[str]] = field(default=None, repr=False)

    def get_profile_names(self) -> List[str]:
        """Return the profile curve names based on attachment type."""
        if self.type == DualRadial or isinstance(self.type, DualRadial):
            return DualRadial().get_profile_names()
        return []

    def generate(
        self,
        context: GenerationContext,
        segment_result: Dict,
        attr_name: str = "",
    ) -> Dict:
        """Generate attachment geometry using raycast positioning.

        Segment radius is determined automatically via raycast on the input geometry.
        Creates Angle Profile and Height Profile closures for shaping.
        """

        node_group = context.node_group
        y_offset = context.get_next_y_offset()

        attachment_label = f"Attachment_{attr_name}" if attr_name else "Attachment"
        attachment_label = (
            attachment_label.strip("_")
            .replace("_attachment", "")
            .replace("attachment_", "")
        )
        if attr_name:
            attachment_label = f"Attachment_{attr_name.lstrip('_').title()}"
        frame = node_group.nodes.new("NodeFrame")
        frame.label = attachment_label
        frame.label_size = 30
        angle_closure = create_float_curve_closure(
            node_group.nodes,
            node_group.links,
            label=f"{attachment_label} Angle Profile",
            location=(-500, y_offset),
        )
        height_closure = create_float_curve_closure(
            node_group.nodes,
            node_group.links,
            label=f"{attachment_label} Height Profile",
            location=(-500, angle_closure.min_y() - 100),
        )
        max_thickness_world = self.max_thickness_mm * 0.001

        nail_group = create_fingernail_node_group(
            name=f"{context.instance_name}_{attachment_label}_Group",
            curl_direction=self.curl_axis,
            nail_width_ratio=self.size_ratio,
            attachment_position=self.attachment_position,
            wrap_amount=self.wrap_amount,
            height_position=self.height_position,
            max_thickness=max_thickness_world,
        )

        attachment_instance = node_group.nodes.new("GeometryNodeGroup")
        attachment_instance.node_tree = nail_group
        attachment_instance.label = attachment_label
        attachment_instance.location = (
            angle_closure.out_node.location[0] + angle_closure.out_node.width + 100,
            height_closure.out_node.location[1],
        )
        for node in (
            [attachment_instance] + angle_closure.nodes() + height_closure.nodes()
        ):
            node.parent = frame
        node_group.links.new(
            segment_result["instance"].outputs["Geometry"],
            attachment_instance.inputs["Geometry"],
        )
        node_group.links.new(
            angle_closure.output_socket,
            attachment_instance.inputs["Angle Float Curve"],
        )
        node_group.links.new(
            height_closure.output_socket,
            attachment_instance.inputs["Height Float Curve"],
        )
        attachment_instance.inputs["Nail Width Ratio"].default_value = self.size_ratio
        attachment_instance.inputs["Attachment Position"].default_value = (
            self.attachment_position
        )
        attachment_instance.inputs["Wrap Amount"].default_value = self.wrap_amount
        attachment_instance.inputs["Height Position"].default_value = (
            self.height_position
        )
        attachment_instance.inputs["Max Thickness"].default_value = max_thickness_world
        context.current_y_offset = height_closure.min_y() - 300

        return {
            "node_group": nail_group,
            "instance": attachment_instance,
            "attachment": self,
            "closures": {"angle": angle_closure, "height": height_closure},
            "frame": frame,
        }


@dsl_primitive
@dataclass
class AttachedStructure:
    """Result of AttachRaycast() - segment with terminal attachment."""

    segment: Any
    attachment: RadialAttachment
    attr_name: str = ""

    def generate(
        self, context: GenerationContext, segment_result: Dict, attr_name: str = ""
    ) -> Dict:
        """Generate attachment on segment end."""
        attachment_name = attr_name or self.attr_name or "attachment"
        if hasattr(self.attachment, "generate"):
            return self.attachment.generate(
                context, segment_result, attr_name=attachment_name
            )
        return {}


@dsl_helper
def AttachRaycast(segment: Any, attachment: RadialAttachment) -> AttachedStructure:
    """Attach a terminal to the end of a segment using raycast positioning."""
    return AttachedStructure(segment=segment, attachment=attachment)
