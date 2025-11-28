"""
DSL primitive classes for procedural generation.

These classes map to geometry node groups in the codebase:
- DualRadial -> dual_radial.py (X, Y profile curves)
- QuadRadial -> quad_radial.py (0°, 90°, 180°, 270° curves)
- Joint -> joint_segment_nodes.py (uses QuadRadial)
- RadialAttachment -> finger_nail_nodes.py (terminal attachments)
- IKLimits -> finger_utils.py IK constraint setup

Each primitive has a generate() method that creates its own geometry nodes.
All primitives are registered via @dsl_primitive decorator for automatic namespace building.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Any, Dict, TYPE_CHECKING
from enum import Enum

from procedural_human.decorators.dsl_primitive_decorator import (
    dsl_primitive,
    dsl_helper,
)

if TYPE_CHECKING:
    import bpy


class ProfileType(Enum):
    """Types of profile curves based on radial type."""
    DUAL_X = "X"
    DUAL_Y = "Y"
    QUAD_0 = "0"
    QUAD_90 = "90"
    QUAD_180 = "180"
    QUAD_270 = "270"


@dataclass
class GenerationContext:
    """Context passed between generate() calls to share state."""
    node_group: Any
    naming_env: Any
    instance_name: str
    definition_name: str
    segment_results: Dict[int, Dict] = field(default_factory=dict)
    current_y_offset: float = 0
    node_spacing: float = 300
    current_attr_name: str = ""
    normalized_lengths: List[float] = field(default_factory=list)
    
    def get_next_y_offset(self) -> float:
        """Get next Y position and decrement for next call."""
        y = self.current_y_offset
        self.current_y_offset -= self.node_spacing
        return y


@dsl_primitive
@dataclass
class IKLimits:
    """
    Inverse Kinematics limits for bone constraints.
    
    Each axis tuple is (min_degrees, max_degrees).
    """
    x: Tuple[float, float] = (-10, 150)
    y: Tuple[float, float] = (-10, 10)
    z: Tuple[float, float] = (-5, 5)
    
    def to_radians(self) -> Dict[str, Tuple[float, float]]:
        """Convert limits to radians for Blender."""
        import math
        return {
            'x': (math.radians(self.x[0]), math.radians(self.x[1])),
            'y': (math.radians(self.y[0]), math.radians(self.y[1])),
            'z': (math.radians(self.z[0]), math.radians(self.z[1])),
        }


@dsl_primitive
@dataclass
class DualRadial:
    """
    Dual-axis radial profile segment.
    
    Uses X and Y profile curves for organic cross-sections.
    Maps to: procedural_human/geo_node_groups/dual_radial.py
    """
    ik: Optional[IKLimits] = None
    profile_type: str = "dual"
    length: float = 1.0
    radius: float = 1.0
    profile_lookup: Optional[int] = None
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    _index: Optional[int] = field(default=None, repr=False)
    
    def __call__(self, length: float = 1.0, radius: float = 1.0, 
                 profile_lookup: Optional[int] = None) -> 'DualRadial':
        """Create a segment instance with specific parameters."""
        instance = DualRadial(
            ik=self.ik,
            profile_type=self.profile_type,
            length=length,
            radius=radius,
            profile_lookup=profile_lookup,
        )
        instance._naming_context = self._naming_context
        instance._index = profile_lookup
        return instance
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names this type uses."""
        return [ProfileType.DUAL_X.value, ProfileType.DUAL_Y.value]
    
    def generate(self, context: GenerationContext, index: int) -> Dict:
        """
        Generate dual radial profile geometry nodes.
        
        Returns dict with:
        - node_group: The created segment node group
        - instance: The node group instance in the parent
        - closures: Dict of profile closures (X, Y)
        - frame: NodeFrame containing the nodes
        """
        import bpy
        from procedural_human.geo_node_groups.dual_radial import create_dual_profile_radial_group
        from procedural_human.geo_node_groups.closures import create_float_curve_closure
        from procedural_human.hand.finger.finger_segment.finger_segment_const import SEGMENT_SAMPLE_COUNT
        from procedural_human.utils import setup_node_group_interface
        
        node_group = context.node_group
        y_offset = context.get_next_y_offset()
        
        seg_name = f"Segment_{index}"
        
        frame = node_group.nodes.new("NodeFrame")
        frame.label = seg_name
        frame.label_size = 30
        
        x_closure = create_float_curve_closure(
            node_group.nodes,
            node_group.links,
            label=f"{seg_name} X Profile",
            location=(-500, y_offset),
        )
        
        y_closure = create_float_curve_closure(
            node_group.nodes,
            node_group.links,
            label=f"{seg_name} Y Profile",
            location=(-500, x_closure.min_y() - 100),
        )
        
        segment_group = self._create_segment_node_group(
            name=f"{context.instance_name}_{seg_name}_Group",
            segment_length=self.length,
            seg_radius=self.radius,
            index=index,
        )
        
        segment_instance = node_group.nodes.new("GeometryNodeGroup")
        segment_instance.node_tree = segment_group
        segment_instance.label = seg_name
        segment_instance.location = (
            x_closure.out_node.location[0] + x_closure.out_node.width + 100,
            y_closure.out_node.location[1],
        )
        
        node_group.links.new(x_closure.output_socket, segment_instance.inputs["X Float Curve"])
        node_group.links.new(y_closure.output_socket, segment_instance.inputs["Y Float Curve"])
        
        segment_instance.inputs["Segment Length"].default_value = self.length
        segment_instance.inputs["Segment Radius"].default_value = self.radius
        segment_instance.inputs["Sample Count"].default_value = SEGMENT_SAMPLE_COUNT
        
        for node in [segment_instance] + x_closure.nodes() + y_closure.nodes():
            node.parent = frame
        
        context.current_y_offset = y_closure.min_y() - 300
        
        result = {
            "index": index,
            "node_group": segment_group,
            "instance": segment_instance,
            "closures": {"X": x_closure, "Y": y_closure},
            "frame": frame,
            "segment": self,
            "abs_x": segment_instance.location[0],
            "abs_y": segment_instance.location[1],
        }
        
        context.segment_results[index] = result
        return result
    
    def _create_segment_node_group(
        self,
        name: str,
        segment_length: float,
        seg_radius: float,
        index: int,
    ) -> Any:
        """Create the internal segment node group structure."""
        import bpy
        from procedural_human.geo_node_groups.dual_radial import create_dual_profile_radial_group
        from procedural_human.hand.finger.finger_segment.finger_segment_const import SEGMENT_SAMPLE_COUNT
        from procedural_human.utils import setup_node_group_interface
        
        segment_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
        setup_node_group_interface(segment_group)
        
        length_socket = segment_group.interface.new_socket(
            name="Segment Length", in_out="INPUT", socket_type="NodeSocketFloat"
        )
        length_socket.default_value = segment_length
        
        radius_socket = segment_group.interface.new_socket(
            name="Segment Radius", in_out="INPUT", socket_type="NodeSocketFloat"
        )
        radius_socket.default_value = seg_radius
        
        segment_group.interface.new_socket(
            name="Segment Radius", in_out="OUTPUT", socket_type="NodeSocketFloat"
        )
        
        sample_count_socket = segment_group.interface.new_socket(
            name="Sample Count", in_out="INPUT", socket_type="NodeSocketInt"
        )
        sample_count_socket.default_value = SEGMENT_SAMPLE_COUNT
        
        segment_group.interface.new_socket(
            name="X Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
        )
        segment_group.interface.new_socket(
            name="Y Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
        )
        
        input_node = segment_group.nodes.new("NodeGroupInput")
        input_node.label = "Inputs"
        input_node.location = (-1400, 0)
        
        bbox_node = segment_group.nodes.new("GeometryNodeBoundBox")
        bbox_node.label = "Find Endpoint"
        bbox_node.location = (-1200, 200)
        segment_group.links.new(input_node.outputs["Geometry"], bbox_node.inputs["Geometry"])
        
        separate_xyz = segment_group.nodes.new("ShaderNodeSeparateXYZ")
        separate_xyz.label = "Extract Z"
        separate_xyz.location = (-1000, 200)
        segment_group.links.new(bbox_node.outputs["Max"], separate_xyz.inputs["Vector"])
        
        grid = segment_group.nodes.new("GeometryNodeMeshGrid")
        grid.label = "Parameter Grid"
        grid.location = (550, -100)
        grid.inputs["Vertices X"].default_value = SEGMENT_SAMPLE_COUNT
        grid.inputs["Size X"].default_value = 1.0
        grid.inputs["Size Y"].default_value = 1.0
        
        radial_group = create_dual_profile_radial_group(suffix=f"Segment_{index}")
        radial_instance = segment_group.nodes.new("GeometryNodeGroup")
        radial_instance.node_tree = radial_group
        radial_instance.label = "Radial Profile (Dual)"
        radial_instance.location = (1400, -200)
        
        segment_group.links.new(input_node.outputs["Segment Radius"], radial_instance.inputs["Radius"])
        segment_group.links.new(separate_xyz.outputs["Z"], radial_instance.inputs["Z Position"])
        segment_group.links.new(input_node.outputs["Segment Length"], radial_instance.inputs["Segment Length"])
        segment_group.links.new(input_node.outputs["X Float Curve"], radial_instance.inputs["X Float Curve"])
        segment_group.links.new(input_node.outputs["Y Float Curve"], radial_instance.inputs["Y Float Curve"])
        segment_group.links.new(input_node.outputs["Sample Count"], grid.inputs["Vertices Y"])
        
        apply_shape = segment_group.nodes.new("GeometryNodeSetPosition")
        apply_shape.label = "Apply Shape"
        apply_shape.location = (2200, 0)
        segment_group.links.new(grid.outputs["Mesh"], apply_shape.inputs["Geometry"])
        segment_group.links.new(radial_instance.outputs["Position"], apply_shape.inputs["Position"])
        
        output_node = segment_group.nodes.new("NodeGroupOutput")
        output_node.label = "Output"
        output_node.location = (2600, 0)
        segment_group.links.new(apply_shape.outputs["Geometry"], output_node.inputs["Geometry"])
        segment_group.links.new(input_node.outputs["Segment Radius"], output_node.inputs["Segment Radius"])
        
        return segment_group


@dsl_primitive
@dataclass
class QuadRadial:
    """
    Quad-axis radial profile for joints.
    
    Uses 4 profile curves at 0°, 90°, 180°, 270° for joint geometry.
    Maps to: procedural_human/geo_node_groups/quad_radial.py
    """
    profile_type: str = "quad"
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names this type uses."""
        return [
            ProfileType.QUAD_0.value,
            ProfileType.QUAD_90.value,
            ProfileType.QUAD_180.value,
            ProfileType.QUAD_270.value,
        ]
    
    def generate(self, context: GenerationContext, index: int, suffix: str = "") -> Any:
        """Generate quad radial profile node group."""
        from procedural_human.geo_node_groups.quad_radial import create_quad_profile_radial_group
        return create_quad_profile_radial_group(suffix=suffix or f"Joint_{index}")


@dsl_primitive
@dataclass
class Joint:
    """
    Joint connector between segments.
    
    Uses QuadRadial for smooth transitions between segments.
    Maps to: procedural_human/hand/finger/finger_segment/joint_segment_nodes.py
    """
    type: type = QuadRadial
    overlap: float = 0.2
    blend_factor: float = 0.5
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    _index: Optional[int] = field(default=None, repr=False)
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names based on joint type."""
        if self.type == QuadRadial or isinstance(self.type, QuadRadial):
            return QuadRadial().get_profile_names()
        return []
    
    def generate(
        self,
        context: GenerationContext,
        index: int,
        prev_segment_result: Dict,
        next_segment_result: Dict,
    ) -> Dict:
        """
        Generate joint geometry nodes between two segments.
        
        Takes geometry from adjacent segments and creates smooth transition.
        Positions joint frame to the right of the segment frames it connects.
        """
        import bpy
        from procedural_human.geo_node_groups.closures import create_flat_float_curve_closure
        from procedural_human.hand.finger.finger_segment.joint_segment_nodes import (
            create_joint_segment_node_group,
        )
        
        node_group = context.node_group
        
        joint_name = f"Joint_{index}"
        
        frame = node_group.nodes.new("NodeFrame")
        frame.label = joint_name
        frame.label_size = 30
        
        prev_frame = prev_segment_result.get("frame")
        next_frame = next_segment_result.get("frame")
        
        max_segment_x = 0
        if prev_frame:
            for node in node_group.nodes:
                if node.parent == prev_frame and node.bl_idname != "NodeFrame":
                    node_right = node.location[0] + node.width
                    if node_right > max_segment_x:
                        max_segment_x = node_right
        if next_frame:
            for node in node_group.nodes:
                if node.parent == next_frame and node.bl_idname != "NodeFrame":
                    node_right = node.location[0] + node.width
                    if node_right > max_segment_x:
                        max_segment_x = node_right
        
        joint_x_start = max_segment_x + 300
        
        prev_y = prev_segment_result.get("abs_y", 0)
        next_y = next_segment_result.get("abs_y", 0)
        y_offset = (prev_y + next_y) / 2
        
        joint_group = create_joint_segment_node_group(
            name=f"{context.instance_name}_{joint_name}_Group",
            prev_start=1.0 - self.overlap,
            next_start=self.overlap,
        )
        
        curve_labels = ["0°", "90°", "180°", "270°"]
        closures = []
        
        first_closure = create_flat_float_curve_closure(
            node_group.nodes,
            node_group.links,
            label=f"{joint_name} {curve_labels[0]}",
            location=(joint_x_start, y_offset),
            value=0.5,
        )
        closures.append(first_closure)
        
        closure_height = first_closure.height()
        vertical_spacing = 300
        
        for i, angle_label in enumerate(curve_labels[1:], start=1):
            closure = create_flat_float_curve_closure(
                node_group.nodes,
                node_group.links,
                label=f"{joint_name} {angle_label}",
                location=(joint_x_start, y_offset - i * vertical_spacing),
                value=0.5,
            )
            closures.append(closure)
        
        joint_instance = node_group.nodes.new("GeometryNodeGroup")
        joint_instance.node_tree = joint_group
        joint_instance.label = joint_name
        
        joint_instance_x = first_closure.out_node.location[0] + first_closure.out_node.width + 100
        joint_instance.location = (joint_instance_x, y_offset)
        
        node_group.links.new(
            prev_segment_result["instance"].outputs["Geometry"],
            joint_instance.inputs["Previous Segment"]
        )
        node_group.links.new(
            next_segment_result["instance"].outputs["Geometry"],
            joint_instance.inputs["Next Segment"]
        )
        
        closure_inputs = ["0° Float Curve", "90° Float Curve", "180° Float Curve", "270° Float Curve"]
        for closure, input_name in zip(closures, closure_inputs):
            node_group.links.new(closure.output_socket, joint_instance.inputs[input_name])
        
        for closure in closures:
            for node in closure.nodes():
                node.parent = frame
        joint_instance.parent = frame
        
        return {
            "index": index,
            "node_group": joint_group,
            "instance": joint_instance,
            "closures": closures,
            "frame": frame,
            "joint": self,
            "abs_x": joint_instance.location[0],
            "abs_y": joint_instance.location[1],
        }


@dsl_primitive
@dataclass
class RadialAttachment:
    """
    Terminal attachment (like fingernail) that attaches to segment end.
    
    Maps to: procedural_human/hand/finger/finger_nail/finger_nail_nodes.py
    """
    type: type = DualRadial
    size_ratio: float = 0.3
    rotation: str = 'Y'
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
        import bpy
        from procedural_human.hand.finger.finger_nail.finger_nail_nodes import (
            create_fingernail_node_group,
        )
        
        node_group = context.node_group
        segment = segment_result["segment"]
        
        attachment_label = f"Attachment_{attr_name}" if attr_name else "Attachment"
        attachment_label = attachment_label.strip("_").replace("_attachment", "").replace("attachment_", "")
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
            attachment_instance.inputs["Geometry"]
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
class SegmentChain:
    """Result of Extend() - a chain of segments along an axis."""
    segments: List[Any]
    axis: str = 'Z'
    norm_lengths: List[float] = field(default_factory=list)
    
    def __iter__(self):
        return iter(self.segments)
    
    def __len__(self):
        return len(self.segments)
    
    def __getitem__(self, index):
        return self.segments[index]
    
    def generate(self, context: GenerationContext) -> Dict:
        """
        Generate chained segment geometry nodes.
        
        Creates each segment and chains geometry: prev_output -> next_input
        Uses normalized lengths if available.
        """
        results = []
        prev_geometry_output = None
        
        if self.norm_lengths and len(self.norm_lengths) == len(self.segments):
            context.normalized_lengths = self.norm_lengths
        
        for idx, segment in enumerate(self.segments):
            if hasattr(segment, 'generate'):
                if self.norm_lengths and idx < len(self.norm_lengths):
                    segment.length = self.norm_lengths[idx]
                
                result = segment.generate(context, idx)
                results.append(result)
                
                if prev_geometry_output is not None:
                    context.node_group.links.new(
                        prev_geometry_output,
                        result["instance"].inputs["Geometry"]
                    )
                
                prev_geometry_output = result["instance"].outputs["Geometry"]
        
        return {
            "segments": results,
            "output": prev_geometry_output,
        }


@dsl_primitive
@dataclass
class JoinedStructure:
    """Result of Join() - segments with joints between them."""
    segments: List[Any]
    joints: List[Joint]
    joint_template: Joint
    
    def get_all_components(self) -> List[Any]:
        """Return interleaved segments and joints."""
        result = []
        for i, seg in enumerate(self.segments):
            result.append(seg)
            if i < len(self.joints):
                result.append(self.joints[i])
        return result
    
    def generate(self, context: GenerationContext, segment_results: List[Dict]) -> Dict:
        """
        Generate joints between segments.
        
        Uses segment geometry from segment_results to create smooth transitions.
        """
        joint_results = []
        
        for idx, joint in enumerate(self.joints):
            if idx < len(segment_results) - 1:
                prev_result = segment_results[idx]
                next_result = segment_results[idx + 1]
                
                if hasattr(joint, 'generate'):
                    result = joint.generate(context, idx, prev_result, next_result)
                    joint_results.append(result)
        
        return {
            "joints": joint_results,
        }


@dsl_primitive
@dataclass 
class AttachedStructure:
    """Result of AttachRaycast() - segment with terminal attachment."""
    segment: Any
    attachment: RadialAttachment
    attr_name: str = ""
    
    def generate(self, context: GenerationContext, segment_result: Dict, attr_name: str = "") -> Dict:
        """Generate attachment on segment end."""
        attachment_name = attr_name or self.attr_name or "attachment"
        if hasattr(self.attachment, 'generate'):
            return self.attachment.generate(context, segment_result, attr_name=attachment_name)
        return {}


@dsl_helper
def normalize(lengths: List[float]) -> List[float]:
    """Normalize a list of lengths to ratios that sum to 1.0."""
    if not lengths:
        return []
    total = sum(lengths)
    if total == 0:
        return [1.0 / len(lengths)] * len(lengths)
    return [length / total for length in lengths]


@dsl_helper
def last(items: List[Any]) -> Any:
    """Get the last item from a list."""
    if not items:
        raise IndexError("Cannot get last item from empty list")
    return items[-1]


@dsl_helper
def Extend(segments: List[Any], axis: str = 'Z', norm_lengths: List[float] = None) -> SegmentChain:
    """Chain segments along an axis, optionally with normalized lengths."""
    return SegmentChain(segments=segments, axis=axis, norm_lengths=norm_lengths or [])


@dsl_helper
def Join(segments: List[Any], joint: Joint) -> JoinedStructure:
    """Insert joints between segments."""
    if isinstance(segments, SegmentChain):
        segment_list = segments.segments
    else:
        segment_list = segments
    
    joints = []
    for i in range(len(segment_list) - 1):
        joint_instance = Joint(
            type=joint.type,
            overlap=joint.overlap,
            blend_factor=joint.blend_factor,
        )
        joint_instance._index = i
        joint_instance._naming_context = joint._naming_context
        joints.append(joint_instance)
    
    return JoinedStructure(
        segments=segment_list,
        joints=joints,
        joint_template=joint,
    )


@dsl_helper
def AttachRaycast(segment: Any, attachment: RadialAttachment) -> AttachedStructure:
    """Attach a terminal to the end of a segment using raycast positioning."""
    return AttachedStructure(segment=segment, attachment=attachment)


Segment = DualRadial
