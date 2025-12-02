from typing import Optional
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


@dsl_primitive
@dataclass
class RadialAttachment:
    """
    Terminal attachment (like fingernail) that attaches to segment end.

    Maps to: procedural_human/hand/finger/finger_nail/finger_nail_nodes.py
    """

    type: type = DualRadial
    size_ratio: float = 0.3
    rotation: str = "Y"
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
        """Generate attachment geometry using raycast positioning."""

        node_group = context.node_group
        segment = segment_result["segment"]

        attachment_label = f"Attachment_{attr_name}" if attr_name else "Attachment"
        attachment_label = (
            attachment_label.strip("_")
            .replace("_attachment", "")
            .replace("attachment_", "")
        )
        if attr_name:
            attachment_label = f"Attachment_{attr_name.lstrip('_').title()}"

        nail_group = create_fingernail_node_group(
            name=f"{context.instance_name}_{attachment_label}_Group",
            curl_direction=self.rotation,
            distal_seg_radius=segment.radius,
            nail_width_ratio=self.size_ratio,
            nail_height_ratio=0.7,
        )

        attachment_instance = node_group.nodes.new("GeometryNodeGroup")
        attachment_instance.node_tree = nail_group
        attachment_instance.label = attachment_label
        attachment_instance.location = (
            segment_result["abs_x"] + 200,
            segment_result["abs_y"],
        )

        if segment_result.get("frame"):
            attachment_instance.parent = segment_result["frame"]

        node_group.links.new(
            segment_result["instance"].outputs["Geometry"],
            attachment_instance.inputs["Geometry"],
        )

        attachment_instance.inputs["SegmentRadius"].default_value = segment.radius
        attachment_instance.inputs["Nail Width Ratio"].default_value = self.size_ratio
        attachment_instance.inputs["Nail Height Ratio"].default_value = 0.7

        return {
            "node_group": nail_group,
            "instance": attachment_instance,
            "attachment": self,
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
