import bpy
from procedural_human.dsl.primitives.extend import SegmentChain
from procedural_human.geo_node_groups.closures import create_flat_float_curve_closure
from procedural_human.hand.finger.finger_segment.joint_segment_nodes import (
    create_joint_segment_node_group,
)
from procedural_human.dsl.primitives.primitives import GenerationContext, ProfileType
from procedural_human.decorators.dsl_primitive_decorator import dsl_helper, dsl_primitive
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from procedural_human.dsl.primitives.quad_radial import QuadRadial

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
        assert len(joint_results) == len(self.joints), "Number of joint results does not match number of joints"
        return {
            "joints": joint_results,
        }

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