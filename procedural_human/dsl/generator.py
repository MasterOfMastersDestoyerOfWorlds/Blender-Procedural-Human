"""
DSL-to-Geometry-Nodes generator.

Recursively walks DSL instances and calls generate() on each primitive to create
actual Blender geometry nodes.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

import bpy

from procedural_human.dsl.primitives import GenerationContext
from procedural_human.dsl.naming import NamingEnvironment
from procedural_human.dsl.executor import DSLExecutionResult
from procedural_human.decorators.dsl_primitive_decorator import is_dsl_primitive


@dataclass
class GenerationResult:
    """Result from recursive generation."""
    segments: List[Dict] = field(default_factory=list)
    joints: List[Dict] = field(default_factory=list)
    attachments: List[Dict] = field(default_factory=list)
    geometry_outputs: List[Any] = field(default_factory=list)
    
    def merge(self, other: 'GenerationResult') -> None:
        """Merge another result into this one."""
        self.segments.extend(other.segments)
        self.joints.extend(other.joints)
        self.attachments.extend(other.attachments)
        self.geometry_outputs.extend(other.geometry_outputs)


@dataclass
class GeneratedObject:
    """Result of generating a Blender object from DSL."""
    name: str
    blend_obj: Any
    node_group: Any
    dsl_source: str
    dsl_instance: str
    generation_result: GenerationResult = field(default_factory=GenerationResult)


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
        
        gen_context = GenerationContext(
            node_group=node_group,
            naming_env=naming_env,
            instance_name=instance_name,
            definition_name=definition_name,
        )
        
        gen_result = self._build_geometry_nodes(node_group, instance, gen_context)
        
        return GeneratedObject(
            name=instance_name,
            blend_obj=obj,
            node_group=node_group,
            dsl_source=source_file,
            dsl_instance=instance_name,
            generation_result=gen_result,
        )
    
    def _setup_node_group_interface(self, node_group: Any) -> None:
        """Set up basic geometry node group interface."""
        node_group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
        node_group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    
    def _build_geometry_nodes(
        self,
        node_group: Any,
        instance: Any,
        context: GenerationContext,
    ) -> GenerationResult:
        """Build geometry nodes by recursively walking instance."""
        input_node = node_group.nodes.new("NodeGroupInput")
        input_node.label = "Input"
        input_node.location = (-1000, 0)
        
        output_node = node_group.nodes.new("NodeGroupOutput")
        output_node.label = "Output"
        output_node.location = (1200, 0)
        
        starting_point = node_group.nodes.new("GeometryNodeCurvePrimitiveLine")
        starting_point.label = "Starting Axis"
        starting_point.location = (-700, 400)
        starting_point.inputs["Start"].default_value = (0.0, 0.0, 0.0)
        starting_point.inputs["End"].default_value = (0.0, 0.0, 0.0)
        
        gen_result = self._generate_recursive(instance, context, starting_point.outputs["Curve"])
        
        join_geo = node_group.nodes.new("GeometryNodeJoinGeometry")
        join_geo.label = "Join All"
        join_geo.location = (1000, 0)
        
        node_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
        
        for geo_output in gen_result.geometry_outputs:
            if geo_output is not None:
                node_group.links.new(geo_output, join_geo.inputs["Geometry"])
        
        node_group.links.new(join_geo.outputs["Geometry"], output_node.inputs["Geometry"])
        
        return gen_result
    
    def _generate_recursive(
        self,
        obj: Any,
        context: GenerationContext,
        prev_geometry: Any = None,
        depth: int = 0,
        index: int = 0,
    ) -> GenerationResult:
        """
        Recursively generate nodes for any object with generate() or generatable attributes.
        
        This enables nested DSL structures like Hand containing Fingers,
        each Finger containing segments, joints, attachments, etc.
        """
        result = GenerationResult()
        
        if obj is None:
            return result
        
        if hasattr(obj, 'generate'):
            gen_result = self._call_generate(obj, context, prev_geometry, index)
            if gen_result:
                self._categorize_result(gen_result, result)
                if "instance" in gen_result and hasattr(gen_result["instance"], "outputs"):
                    if "Geometry" in gen_result["instance"].outputs:
                        result.geometry_outputs.append(gen_result["instance"].outputs["Geometry"])
            return result
        
        if isinstance(obj, (list, tuple)):
            prev_output = prev_geometry
            for idx, item in enumerate(obj):
                sub_result = self._generate_recursive(item, context, prev_output, depth + 1, idx)
                result.merge(sub_result)
                if sub_result.geometry_outputs:
                    prev_output = sub_result.geometry_outputs[-1]
            return result
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                sub_result = self._generate_recursive(value, context, prev_geometry, depth + 1)
                result.merge(sub_result)
            return result
        
        if self._is_dsl_instance(obj):
            for attr_name in self._get_generatable_attrs(obj):
                attr_value = getattr(obj, attr_name, None)
                if attr_value is not None:
                    sub_result = self._generate_recursive(attr_value, context, prev_geometry, depth + 1)
                    result.merge(sub_result)
                    if sub_result.geometry_outputs:
                        prev_geometry = sub_result.geometry_outputs[-1]
        
        return result
    
    def _call_generate(
        self,
        obj: Any,
        context: GenerationContext,
        prev_geometry: Any,
        index: int,
    ) -> Optional[Dict]:
        """Call generate() on an object with appropriate arguments."""
        import inspect
        
        generate_method = getattr(obj, 'generate', None)
        if not generate_method:
            return None
        
        sig = inspect.signature(generate_method)
        params = list(sig.parameters.keys())
        
        kwargs = {}
        if 'context' in params:
            kwargs['context'] = context
        if 'index' in params:
            kwargs['index'] = index
        if 'segment_results' in params:
            kwargs['segment_results'] = list(context.segment_results.values())
        if 'segment_result' in params and context.segment_results:
            last_idx = max(context.segment_results.keys())
            kwargs['segment_result'] = context.segment_results[last_idx]
        if 'prev_segment_result' in params and context.segment_results:
            if index in context.segment_results:
                kwargs['prev_segment_result'] = context.segment_results[index]
            elif context.segment_results:
                first_idx = min(context.segment_results.keys())
                kwargs['prev_segment_result'] = context.segment_results[first_idx]
        if 'next_segment_result' in params and context.segment_results:
            next_idx = index + 1
            if next_idx in context.segment_results:
                kwargs['next_segment_result'] = context.segment_results[next_idx]
            elif context.segment_results:
                last_idx = max(context.segment_results.keys())
                kwargs['next_segment_result'] = context.segment_results[last_idx]
        
        try:
            result = generate_method(**kwargs)
            return result
        except TypeError as e:
            print(f"[Generator] Error calling generate on {type(obj).__name__}: {e}")
            try:
                result = generate_method(context, index)
                return result
            except Exception:
                return None
    
    def _categorize_result(self, gen_result: Dict, result: GenerationResult) -> None:
        """Categorize a generation result into segments, joints, or attachments."""
        if gen_result is None:
            return
        
        if "segment" in gen_result or "segments" in gen_result:
            if "segments" in gen_result:
                result.segments.extend(gen_result["segments"])
            else:
                result.segments.append(gen_result)
        elif "joint" in gen_result or "joints" in gen_result:
            if "joints" in gen_result:
                result.joints.extend(gen_result["joints"])
            else:
                result.joints.append(gen_result)
        elif "attachment" in gen_result:
            result.attachments.append(gen_result)
        elif "instance" in gen_result:
            result.segments.append(gen_result)
    
    def _is_dsl_instance(self, obj: Any) -> bool:
        """Check if an object is a DSL instance (user-defined class from DSL file)."""
        if obj is None:
            return False
        if isinstance(obj, (str, int, float, bool, bytes)):
            return False
        if is_dsl_primitive(obj):
            return False
        if hasattr(obj, '__class__') and hasattr(obj.__class__, '__module__'):
            return True
        return False
    
    def _get_generatable_attrs(self, obj: Any) -> List[str]:
        """Get list of attribute names that might be generatable.
        
        Returns attrs sorted so public attrs (no underscore) come first,
        then single-underscore attrs. This ensures primary data like 'segments'
        is processed before derived data like '_nail_attachment'.
        """
        public_attrs = []
        private_attrs = []
        
        for attr_name in dir(obj):
            if attr_name.startswith('__'):
                continue
            if attr_name.startswith('get_') or attr_name.startswith('to_'):
                continue
            if callable(getattr(obj, attr_name, None)) and not attr_name.startswith('_'):
                continue
            
            attr_value = getattr(obj, attr_name, None)
            if attr_value is None:
                continue
            if isinstance(attr_value, (str, int, float, bool, bytes)):
                continue
            
            is_generatable = False
            if hasattr(attr_value, 'generate'):
                is_generatable = True
            elif isinstance(attr_value, (list, tuple)):
                if attr_value and hasattr(attr_value[0], 'generate'):
                    is_generatable = True
            elif self._is_dsl_instance(attr_value):
                is_generatable = True
            
            if is_generatable:
                if attr_name.startswith('_'):
                    private_attrs.append(attr_name)
                else:
                    public_attrs.append(attr_name)
        
        return public_attrs + private_attrs


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
    source_file = obj.get("dsl_source_file", "")
    instance_name = obj.get("dsl_instance_name", "")
    
    if not source_file or not instance_name:
        return None
    
    from procedural_human.dsl.executor import execute_dsl_file
    
    result = execute_dsl_file(source_file)
    if instance_name not in result.instances:
        return None
    
    if obj.modifiers:
        old_node_group = obj.modifiers[0].node_group
        if old_node_group:
            bpy.data.node_groups.remove(old_node_group)
    
    generator = DSLGenerator()
    new_results = generator.generate_from_result(result, instance_filter=[instance_name])
    
    if new_results:
        new_result = new_results[0]
        if obj.modifiers:
            obj.modifiers[0].node_group = new_result.node_group
        return new_result
    
    return None
