from procedural_human.logger import *
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive
from procedural_human.dsl.primitives.primitives import GenerationContext, ProfileType
import bpy
from procedural_human.geo_node_groups.dual_radial import create_dual_profile_radial_group
from procedural_human.geo_node_groups.closures import create_float_curve_closure
from procedural_human.hand.finger.finger_segment.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.utils import setup_node_group_interface

@dsl_primitive
@dataclass
class DualRadial:
    """
    Dual-axis radial profile segment.
    
    Uses X and Y profile curves for organic cross-sections.
    Maps to: procedural_human/geo_node_groups/dual_radial.py
    
    Note: IK limits should be specified via the Bone wrapper, not directly on DualRadial.
    """
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
        
        self._apply_preset_to_closures(context, index, x_closure, y_closure)
        
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
    
    def _apply_preset_to_closures(
        self,
        context: GenerationContext,
        index: int,
        x_closure: Any,
        y_closure: Any,
    ) -> bool:
        """
        Apply preset curve data to the X and Y closures if a preset exists.
        
        Looks up preset by: {instance_name}_Segment_{index}
        Preset data keys: Segment_{index}_X, Segment_{index}_Y
        """
        from procedural_human.decorators.curve_preset_decorator import (
            register_preset_class
        )
        from procedural_human.utils.curve_serialization import apply_data_to_float_curve_node
        
        preset_name = f"{context.instance_name}_Segment_{index}"
        
        all_names = register_preset_class.registry.keys()
        logger.info(f"[Preset Debug] Looking for preset: '{preset_name}'")
        logger.info(f"[Preset Debug] Available presets in registry: {all_names}")
        
        preset_data = register_preset_class.get_preset(preset_name)
        
        if preset_data is None:
            logger.info(f"[Preset Debug] No preset found for '{preset_name}'")
            return False
        
        logger.info(f"[Preset Debug] Found preset '{preset_name}' with keys: {list(preset_data.keys())}")
        
        x_key = f"Segment_{index}_X"
        y_key = f"Segment_{index}_Y"
        
        applied = False
        
        if x_key in preset_data and x_closure.curve_node:
            logger.info(f"[Preset Debug] Applying {x_key} to X closure")
            if apply_data_to_float_curve_node(x_closure.curve_node, preset_data[x_key]):
                applied = True
                logger.info(f"[Preset Debug] Successfully applied {x_key}")
        else:
            logger.info(f"[Preset Debug] Key '{x_key}' not in preset or closure missing")
        
        if y_key in preset_data and y_closure.curve_node:
            logger.info(f"[Preset Debug] Applying {y_key} to Y closure")
            if apply_data_to_float_curve_node(y_closure.curve_node, preset_data[y_key]):
                applied = True
                logger.info(f"[Preset Debug] Successfully applied {y_key}")
        else:
            logger.info(f"[Preset Debug] Key '{y_key}' not in preset or closure missing")
        
        return applied