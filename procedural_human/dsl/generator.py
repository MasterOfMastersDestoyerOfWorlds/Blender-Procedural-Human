"""
DSL-to-Geometry-Nodes generator.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    bpy = None

from procedural_human.dsl.primitives import DualRadial, Joint, SegmentChain, JoinedStructure
from procedural_human.dsl.naming import NamingEnvironment
from procedural_human.dsl.executor import DSLExecutionResult
from procedural_human.decorators.curve_preset_decorator import resolve_profile_chain


@dataclass
class GeneratedObject:
    """Result of generating a Blender object from DSL."""
    name: str
    blend_obj: Any
    node_group: Any
    dsl_source: str
    dsl_instance: str
    segments: List[Any] = field(default_factory=list)
    joints: List[Any] = field(default_factory=list)


class DSLGenerator:
    """Generates Blender geometry nodes from DSL definitions."""
    
    def __init__(self, context: Any = None):
        self.context = context
        self._generated_objects: Dict[str, GeneratedObject] = {}
    
    def generate_from_result(
        self,
        result: DSLExecutionResult,
        instance_filter: Optional[List[str]] = None
    ) -> List[GeneratedObject]:
        """Generate Blender objects from DSL execution result."""
        if not BLENDER_AVAILABLE:
            raise RuntimeError("Blender is not available")
        
        generated = []
        
        for instance_name, instance in result.instances.items():
            if instance_filter and instance_name not in instance_filter:
                continue
            
            definition_name = instance.__class__.__name__
            
            result.naming_env.clear_scope()
            result.naming_env.push_scope(instance_name)
            result.naming_env.push_scope(definition_name)
            
            gen_obj = self._generate_instance(
                instance_name=instance_name,
                instance=instance,
                definition_name=definition_name,
                naming_env=result.naming_env,
                source_file=result.file_path,
            )
            
            if gen_obj:
                generated.append(gen_obj)
                self._generated_objects[instance_name] = gen_obj
        
        return generated
    
    def _generate_instance(
        self,
        instance_name: str,
        instance: Any,
        definition_name: str,
        naming_env: NamingEnvironment,
        source_file: str,
    ) -> Optional[GeneratedObject]:
        """Generate a single Blender object from a DSL instance."""
        if not BLENDER_AVAILABLE:
            return None
        
        mesh = bpy.data.meshes.new(f"{instance_name}Mesh")
        mesh.from_pydata([(0, 0, 0)], [], [])
        obj = bpy.data.objects.new(instance_name, mesh)
        
        if self.context:
            self.context.collection.objects.link(obj)
        else:
            bpy.context.collection.objects.link(obj)
        
        obj["dsl_source_file"] = source_file
        obj["dsl_instance_name"] = instance_name
        obj["dsl_definition_name"] = definition_name
        
        modifier = obj.modifiers.new(name=f"{instance_name}Shape", type='NODES')
        node_group = bpy.data.node_groups.new(f"{instance_name}_Nodes", 'GeometryNodeTree')
        modifier.node_group = node_group
        
        self._setup_node_group_interface(node_group)
        segments, joints = self._build_geometry_nodes(node_group, instance, naming_env)
        
        return GeneratedObject(
            name=instance_name,
            blend_obj=obj,
            node_group=node_group,
            dsl_source=source_file,
            dsl_instance=instance_name,
            segments=segments,
            joints=joints,
        )
    
    def _setup_node_group_interface(self, node_group: Any) -> None:
        """Set up basic geometry node group interface."""
        node_group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
        node_group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    
    def _build_geometry_nodes(
        self,
        node_group: Any,
        instance: Any,
        naming_env: NamingEnvironment,
    ) -> Tuple[List[Any], List[Any]]:
        """Build geometry nodes from DSL instance."""
        input_node = node_group.nodes.new("NodeGroupInput")
        input_node.label = "Input"
        input_node.location = (-1000, 0)
        
        output_node = node_group.nodes.new("NodeGroupOutput")
        output_node.label = "Output"
        output_node.location = (1200, 0)
        
        segments = []
        joints = []
        
        if hasattr(instance, 'segments'):
            instance_segments = getattr(instance, 'segments')
            if isinstance(instance_segments, (list, SegmentChain)):
                for idx, seg in enumerate(instance_segments):
                    segment_nodes = self._create_segment_nodes(node_group, seg, idx, naming_env)
                    segments.append(segment_nodes)
        
        if hasattr(instance, '_joined_structure'):
            joined = getattr(instance, '_joined_structure')
            if isinstance(joined, JoinedStructure):
                for idx, joint in enumerate(joined.joints):
                    joint_nodes = self._create_joint_nodes(node_group, joint, idx, naming_env)
                    joints.append(joint_nodes)
        
        join_geo = node_group.nodes.new("GeometryNodeJoinGeometry")
        join_geo.label = "Join All"
        join_geo.location = (1000, 0)
        
        node_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
        node_group.links.new(join_geo.outputs["Geometry"], output_node.inputs["Geometry"])
        
        return segments, joints
    
    def _create_segment_nodes(
        self,
        node_group: Any,
        segment: Any,
        index: int,
        naming_env: NamingEnvironment,
    ) -> Dict:
        """Create nodes for a single segment with profile lookups."""
        profiles = {}
        
        if isinstance(segment, DualRadial):
            for axis in ["X", "Y"]:
                name_chain = naming_env.build_profile_name_chain("Segment", index, axis)
                profile_data, resolved_name = resolve_profile_chain(name_chain, axis)
                profiles[axis] = {"data": profile_data, "resolved_name": resolved_name}
        
        frame = node_group.nodes.new("NodeFrame")
        frame.label = f"Segment_{index}"
        frame.location = (-500, -index * 300)
        
        return {"index": index, "frame": frame, "profiles": profiles, "segment": segment}
    
    def _create_joint_nodes(
        self,
        node_group: Any,
        joint: Joint,
        index: int,
        naming_env: NamingEnvironment,
    ) -> Dict:
        """Create nodes for a single joint with profile lookups."""
        profiles = {}
        
        for axis in ["0", "90", "180", "270"]:
            name_chain = naming_env.build_profile_name_chain("Knuckle", index, axis)
            profile_data, resolved_name = resolve_profile_chain(name_chain, axis)
            profiles[axis] = {"data": profile_data, "resolved_name": resolved_name}
        
        frame = node_group.nodes.new("NodeFrame")
        frame.label = f"Joint_{index}"
        frame.location = (0, -index * 300)
        
        return {"index": index, "frame": frame, "profiles": profiles, "joint": joint}


def generate_from_dsl_file(
    file_path: str,
    context: Any = None,
    instance_filter: Optional[List[str]] = None
) -> List[GeneratedObject]:
    """Generate Blender objects from a DSL file."""
    from procedural_human.dsl.executor import execute_dsl_file
    
    result = execute_dsl_file(file_path)
    if not result.success:
        print(f"DSL execution errors: {result.errors}")
    
    generator = DSLGenerator(context)
    return generator.generate_from_result(result, instance_filter)


def regenerate_dsl_object(obj: Any) -> Optional[GeneratedObject]:
    """Regenerate a Blender object from its DSL source."""
    if not BLENDER_AVAILABLE:
        return None
    
    source_file = obj.get("dsl_source_file", "")
    instance_name = obj.get("dsl_instance_name", "")
    
    if not source_file or not instance_name:
        return None
    
    from procedural_human.dsl.executor import execute_dsl_file
    
    result = execute_dsl_file(source_file)
    if instance_name not in result.instances:
        return None
    
    generator = DSLGenerator()
    generator._generated_objects[instance_name] = GeneratedObject(
        name=instance_name,
        blend_obj=obj,
        node_group=obj.modifiers[0].node_group if obj.modifiers else None,
        dsl_source=source_file,
        dsl_instance=instance_name,
    )
    
    return generator._generated_objects.get(instance_name)

