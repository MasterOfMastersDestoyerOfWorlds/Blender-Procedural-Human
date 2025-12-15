from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive
from procedural_human.dsl.primitives.primitives import GenerationContext
from procedural_human.dsl.primitives.hex_radial.hex_radial_nodes import (
    create_hex_profile_spheroid_group,
)
from procedural_human.geo_node_groups.closures import create_float_curve_closure
import bpy


@dsl_primitive
@dataclass
class HexRadial:
    """
    6-Axis Radial Spheroid.

    Defines a spheroid shape using 6 profile curves (X+, X-, Y+, Y-, Z+, Z-).
    Input to curves is the distance from that axis (0 at pole, 1 at equator).
    """

    radius: float = 1.0
    subdivisions: int = 4
    _naming_context: Optional[List[str]] = field(default=None, repr=False)

    def get_profile_names(self) -> List[str]:
        return ["X+", "X-", "Y+", "Y-", "Z+", "Z-"]

    def generate(self, context: GenerationContext, index: int) -> Dict:
        node_group = context.node_group

        # Create Frame
        name = f"HexSpheroid_{index}"
        frame = node_group.nodes.new("NodeFrame")
        frame.label = name

        # Create 6 Closures
        closures = {}
        y_cursor = context.get_next_y_offset()

        labels = self.get_profile_names()

        for label in labels:
            closure = create_float_curve_closure(
                node_group.nodes,
                node_group.links,
                label=f"{name} {label}",
                location=(-500, y_cursor),
            )
            # Default curve to 1.0 (Unit sphere shape)
            for p in closure.curve_node.mapping.curves[0].points:
                p.location.y = 1.0

            closures[label] = closure
            # Group nodes into frame
            for n in closure.nodes():
                n.parent = frame

            y_cursor -= 150

        # Create Geometry (UV Sphere)
        sphere = node_group.nodes.new("GeometryNodeMeshUVSphere")
        sphere.inputs["Radius"].default_value = 1.0  # Base unit sphere
        sphere.inputs["Segments"].default_value = 32 * self.subdivisions
        sphere.inputs["Rings"].default_value = 16 * self.subdivisions
        sphere.parent = frame
        sphere.location = (-800, y_cursor)

        # Create Hex Group
        hex_group = create_hex_profile_spheroid_group(
            suffix=f"{context.instance_name}_{index}"
        )
        hex_instance = node_group.nodes.new("GeometryNodeGroup")
        hex_instance.node_tree = hex_group
        hex_instance.label = "Hex Radial Deform"
        hex_instance.parent = frame
        hex_instance.location = (-200, y_cursor)

        # Links
        node_group.links.new(sphere.outputs["Mesh"], hex_instance.inputs["Geometry"])
        hex_instance.inputs["Radius"].default_value = self.radius

        for label in labels:
            node_group.links.new(
                closures[label].output_socket,
                hex_instance.inputs[f"{label} Float Curve"],
            )

        # Apply Preset if available (using logic from dual_radial)
        self._apply_presets(context, index, closures)

        context.current_y_offset = y_cursor - 300

        return {"instance": hex_instance, "frame": frame, "closures": closures}

    def _apply_presets(self, context, index, closures):
        # reuse existing preset application logic found in dual_radial.py
        # adapted for the 6 keys
        pass
