"""
DSL-to-Geometry-Nodes generator.

Recursively walks DSL instances and calls generate() on each primitive to create
actual Blender geometry nodes.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import inspect
import bpy

from procedural_human.dsl.debug import export_debug_info
from procedural_human.dsl.primitives import GenerationContext
from procedural_human.dsl.naming import NamingEnvironment
from procedural_human.dsl.executor import DSLExecutionResult
from procedural_human.decorators.dsl_primitive_decorator import is_dsl_primitive
from procedural_human.logger import *
from procedural_human.dsl.primitives import (
    SegmentChain,
    JoinedStructure,
    AttachedStructure,
    Bone,
)

@dataclass
class GenerationResult:
    """Result from recursive generation."""

    segments: List[Dict] = field(default_factory=list) 
    joints: List[Dict] = field(default_factory=list)
    attachments: List[Dict] = field(default_factory=list)
    geometry_outputs: List[Any] = field(default_factory=list)
    bones: List[Dict] = field(default_factory=list)

    def merge(self, other: "GenerationResult") -> None:
        """Merge another result into this one."""
        self.segments.extend(other.segments)
        self.joints.extend(other.joints)
        self.attachments.extend(other.attachments)
        self.geometry_outputs.extend(other.geometry_outputs)
        self.bones.extend(other.bones)


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
        self, result: DSLExecutionResult, instance_filter: Optional[List[str]] = None
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

        modifier = obj.modifiers.new(name=f"{instance_name}Shape", type="NODES")
        node_group = bpy.data.node_groups.new(
            f"{instance_name}_Nodes", "GeometryNodeTree"
        )
        modifier.node_group = node_group

        node_group.interface.new_socket(
            name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        node_group.interface.new_socket(
            name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

        gen_context = GenerationContext(
            node_group=node_group,
            naming_env=naming_env,
            instance_name=instance_name,
            definition_name=definition_name,
        )

        input_node = node_group.nodes.new("NodeGroupInput")
        input_node.label = "Input"
        input_node.location = (-1000, 0)

        starting_point = node_group.nodes.new("GeometryNodeCurvePrimitiveLine")
        starting_point.label = "Starting Axis"
        starting_point.location = (-700, 400)
        starting_point.inputs["Start"].default_value = (0.0, 0.0, 0.0)
        starting_point.inputs["End"].default_value = (0.0, 0.0, 0.0)

        gen_result = self._generate_recursive(
            instance, gen_context, starting_point.outputs["Curve"]
        )

        max_x = 0
        for node in node_group.nodes:
            if node.bl_idname != "NodeFrame":
                node_right = node.location[0] + node.width
                if node_right > max_x:
                    max_x = node_right

        join_geo = node_group.nodes.new("GeometryNodeJoinGeometry")
        join_geo.label = "Join All"
        join_geo.location = (max_x + 200, 0)

        output_node = node_group.nodes.new("NodeGroupOutput")
        output_node.label = "Output"
        output_node.location = (join_geo.location[0] + 200, 0)

        node_group.links.new(
            input_node.outputs["Geometry"], join_geo.inputs["Geometry"]
        )

        all_geometry_outputs = []

        for seg in gen_result.segments:
            if seg and "instance" in seg and hasattr(seg["instance"], "outputs"):
                if "Geometry" in seg["instance"].outputs:
                    all_geometry_outputs.append(seg["instance"].outputs["Geometry"])

        for joint in gen_result.joints:
            if joint and "instance" in joint and hasattr(joint["instance"], "outputs"):
                if "Geometry" in joint["instance"].outputs:
                    all_geometry_outputs.append(joint["instance"].outputs["Geometry"])

        for attach in gen_result.attachments:
            if (
                attach
                and "instance" in attach
                and hasattr(attach["instance"], "outputs")
            ):
                if "Geometry" in attach["instance"].outputs:
                    all_geometry_outputs.append(attach["instance"].outputs["Geometry"])

        for geo_output in gen_result.geometry_outputs:
            if geo_output is not None and geo_output not in all_geometry_outputs:
                all_geometry_outputs.append(geo_output)

        for geo_output in all_geometry_outputs:
            if geo_output is not None:
                node_group.links.new(geo_output, join_geo.inputs["Geometry"])

        node_group.links.new(
            join_geo.outputs["Geometry"], output_node.inputs["Geometry"]
        )

        export_debug_info(node_group, instance_name, source_file)

        return GeneratedObject(
            name=instance_name,
            blend_obj=obj,
            node_group=node_group,
            dsl_source=source_file,
            dsl_instance=instance_name,
            generation_result=gen_result,
        )


    def _generate_recursive(
        self,
        obj: Any,
        context: GenerationContext,
        prev_geometry: Any = None,
        depth: int = 0,
        index: int = 0,
        attr_name: str = "",
    ) -> GenerationResult:
        """
        Recursively generate nodes for any object with generate() or generatable attributes.

        This enables nested DSL structures like Hand containing Fingers,
        each Finger containing segments, joints, attachments, etc.
        """
        result = GenerationResult()

        if obj is None:
            return result
        if hasattr(obj, "generate"):

            if obj._type == "JoinedStructure":
                logger.info(f"Generating JoinedStructure: {obj._type}")
            gen_result = None
            generate_method = getattr(obj, "generate", None)
            sig = inspect.signature(generate_method)
            params = list(sig.parameters.keys())

            kwargs = {}
            if "context" in params:
                kwargs["context"] = context
            if "index" in params:
                kwargs["index"] = index
            if "attr_name" in params:
                kwargs["attr_name"] = attr_name
            if "segment_results" in params:
                kwargs["segment_results"] = list(context.segment_results.values())
            if "segment_result" in params and context.segment_results:
                last_idx = max(context.segment_results.keys())
                kwargs["segment_result"] = context.segment_results[last_idx]
            if "prev_segment_result" in params and context.segment_results:
                if index in context.segment_results:
                    kwargs["prev_segment_result"] = context.segment_results[index]
                elif context.segment_results:
                    first_idx = min(context.segment_results.keys())
                    kwargs["prev_segment_result"] = context.segment_results[
                        first_idx
                    ]
            if "next_segment_result" in params and context.segment_results:
                next_idx = index + 1
                if next_idx in context.segment_results:
                    kwargs["next_segment_result"] = context.segment_results[
                        next_idx
                    ]
                elif context.segment_results:
                    last_idx = max(context.segment_results.keys())
                    kwargs["next_segment_result"] = context.segment_results[
                        last_idx
                    ]
            try:
                gen_result = generate_method(**kwargs)
            except TypeError as e:
                logger.info(
                    f"[Generator] Error calling generate on {type(obj).__name__}: {e}"
                )
                try:
                    gen_result = generate_method(context, index)
                except Exception:
                    gen_result = None
            if gen_result:
                if gen_result is None:
                    return
                if "segments" in gen_result:
                    result.segments.extend(gen_result["segments"])
                elif "segment" in gen_result:
                    result.segments.append(gen_result)
                elif "instance" in gen_result:
                    result.segments.append(gen_result)

                if "joints" in gen_result:
                    result.joints.extend(gen_result["joints"])
                elif "joint" in gen_result:
                    result.joints.append(gen_result)

                if "attachment" in gen_result:
                    result.attachments.append(gen_result)

                if "bones" in gen_result:
                    result.bones.extend(gen_result["bones"])
                elif gen_result.get("bone"):
                    result.bones.append(gen_result)

                if "instance" in gen_result and hasattr(
                    gen_result["instance"], "outputs"
                ):
                    if "Geometry" in gen_result["instance"].outputs:
                        result.geometry_outputs.append(
                            gen_result["instance"].outputs["Geometry"]
                        )
            return result

        if isinstance(obj, (list, tuple)):
            prev_output = prev_geometry
            for idx, item in enumerate(obj):
                sub_result = self._generate_recursive(
                    item, context, prev_output, depth + 1, idx, attr_name
                )
                result.merge(sub_result)

                if sub_result.segments:
                    last_seg = sub_result.segments[-1]
                    if last_seg and "instance" in last_seg:
                        instance = last_seg["instance"]
                        if (
                            hasattr(instance, "outputs")
                            and "Geometry" in instance.outputs
                        ):
                            prev_output = instance.outputs["Geometry"]
                elif sub_result.geometry_outputs:
                    prev_output = sub_result.geometry_outputs[-1]
            return result

        if isinstance(obj, dict):
            for key, value in obj.items():
                sub_result = self._generate_recursive(
                    value, context, prev_geometry, depth + 1, attr_name=key
                )
                result.merge(sub_result)
            return result

        if self._is_dsl_instance(obj):
            for attribute in self._get_generatable_attrs(obj):
                attr_value = getattr(obj, attribute, None) 
                if attr_value is not None:
                    sub_result = self._generate_recursive(
                        attr_value, context, prev_geometry, depth + 1, attr_name=attribute
                    )
                    result.merge(sub_result)

                    if sub_result.segments:
                        last_seg = sub_result.segments[-1]
                        if last_seg and "instance" in last_seg:
                            instance = last_seg["instance"]
                            if (
                                hasattr(instance, "outputs")
                                and "Geometry" in instance.outputs
                            ):
                                prev_geometry = instance.outputs["Geometry"]
                    elif sub_result.geometry_outputs:
                        prev_geometry = sub_result.geometry_outputs[-1]

        return result 

    def _is_dsl_instance(self, obj: Any) -> bool:
        """Check if an object is a DSL instance (user-defined class from DSL file)."""
        if obj is None:
            return False
        if isinstance(obj, (str, int, float, bool, bytes)):
            return False
        if is_dsl_primitive(obj):
            return False
        if hasattr(obj, "__class__") and hasattr(obj.__class__, "__module__"):
            return True
        return False

    def _get_generatable_attrs(self, obj: Any) -> List[str]:
        """Get list of attribute names that might be generatable.

        Uses type-based checking (isinstance) instead of name-based checking.
        This allows DSL definitions to use any attribute names while still
        being processed correctly.

        Processing order:
        1. SegmentChain instances (skip raw 'segments' lists if present)
        2. JoinedStructure instances (skip raw 'joints' lists if present)
        3. AttachedStructure instances
        4. Other generatable attributes

        Note: 'bones' lists are skipped - they're metadata for armature creation,
        not geometry generation.
        """


        segment_chain_attr = None
        joined_structure_attr = None
        attached_structure_attrs = []
        other_generatable = []
        raw_lists_to_skip = set(["bones"])

        for attr_name in dir(obj):
            if attr_name.startswith("__"):
                continue
            if attr_name.startswith("get_") or attr_name.startswith("to_"):
                continue
            if callable(getattr(obj, attr_name, None)) and not attr_name.startswith(
                "_"
            ):
                continue

            attr_value = getattr(obj, attr_name, None)
            if attr_value is None:
                continue
            if isinstance(attr_value, (str, int, float, bool, bytes)):
                continue

            if isinstance(attr_value, SegmentChain):
                segment_chain_attr = attr_name
                raw_lists_to_skip.add("segments")
            elif isinstance(attr_value, JoinedStructure):
                joined_structure_attr = attr_name
                raw_lists_to_skip.add("joints")
            elif isinstance(attr_value, AttachedStructure):
                attached_structure_attrs.append(attr_name)
            elif isinstance(attr_value, Bone):
                continue
            elif hasattr(attr_value, "generate"):
                other_generatable.append(attr_name)
            elif isinstance(attr_value, (list, tuple)):
                if attr_value and isinstance(attr_value[0], Bone):
                    continue
                if attr_value and hasattr(attr_value[0], "generate"):
                    other_generatable.append(attr_name)
            elif self._is_dsl_instance(attr_value):
                other_generatable.append(attr_name)

        ordered_attrs = []

        if segment_chain_attr:
            ordered_attrs.append(segment_chain_attr)
        if joined_structure_attr:
            ordered_attrs.append(joined_structure_attr)

        ordered_attrs.extend(attached_structure_attrs)

        for attr_name in other_generatable:
            if attr_name not in raw_lists_to_skip:
                ordered_attrs.append(attr_name)

        return ordered_attrs


def generate_from_dsl_file(
    file_path: str, context: Any = None, instance_filter: Optional[List[str]] = None
) -> List[GeneratedObject]:
    """Generate Blender objects from a DSL file."""
    from procedural_human.dsl.executor import execute_dsl_file

    result = execute_dsl_file(file_path)
    if not result.success:
        logger.info(f"DSL execution errors: {result.errors}")

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
    new_results = generator.generate_from_result(
        result, instance_filter=[instance_name]
    )

    if new_results:
        new_result = new_results[0]
        if obj.modifiers:
            obj.modifiers[0].node_group = new_result.node_group
        return new_result

    return None
