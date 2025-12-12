from dataclasses import dataclass
from typing import Dict, Optional, Any
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive
from procedural_human.dsl.primitives.primitives import GenerationContext
from procedural_human.dsl.primitives.dual_radial_loft.dual_radial_loft_nodes import create_dual_radial_loft_group
import bpy

@dsl_primitive
@dataclass
class DualRadialLoft:
    """
    Synthesizes a 3D Spheroid from two profile curves.
    
    Universal Lofting Primitive:
    - Curve X: Always the Primary/Front profile (XZ Plane).
    - Curve Y: Can be either a Side profile (YZ Plane) OR a Top profile (XY Plane).
    
    The system automatically detects if 'Curve Y' is vertical or flat and switches 
    mathematical modes accordingly to produce a manifold spheroid.
    """
    curve_x: str  # Name of object defining X silhouette
    curve_y: str  # Name of object defining Y silhouette (Side or Top)
    height: float = 1.0 # Optional scaling factor
    res_u: int = 32
    res_v: int = 64
    
    def generate(self, context: GenerationContext, index: int) -> Dict:
        node_group = context.node_group
        
        # Create Frame
        name = f"Loft_{index}"
        frame = node_group.nodes.new("NodeFrame")
        frame.label = name
        
        # Create the Lofting Node Group
        loft_group = create_dual_radial_loft_group(name=f"{context.instance_name}_{name}_Group")
        loft_instance = node_group.nodes.new("GeometryNodeGroup")
        loft_instance.node_tree = loft_group
        loft_instance.label = "Dual Radial Loft"
        loft_instance.parent = frame
        
        # Fetch Curve Objects
        obj_info_x = node_group.nodes.new("GeometryNodeObjectInfo")
        obj_info_x.transform_space = 'RELATIVE'
        if self.curve_x in bpy.data.objects:
            obj_info_x.inputs["Object"].default_value = bpy.data.objects[self.curve_x]
        
        obj_info_y = node_group.nodes.new("GeometryNodeObjectInfo")
        obj_info_y.transform_space = 'RELATIVE'
        if self.curve_y in bpy.data.objects:
            obj_info_y.inputs["Object"].default_value = bpy.data.objects[self.curve_y]
            
        obj_info_x.parent = frame
        obj_info_y.parent = frame
        
        # Layout
        x_pos = context.get_next_y_offset()
        y_pos = 0
        loft_instance.location = (x_pos, y_pos)
        obj_info_x.location = (x_pos - 200, y_pos + 100)
        obj_info_y.location = (x_pos - 200, y_pos - 100)
         
        # Links
        node_group.links.new(obj_info_x.outputs["Geometry"], loft_instance.inputs["Curve X (Front)"])
        node_group.links.new(obj_info_y.outputs["Geometry"], loft_instance.inputs["Curve Y (Side)"])
        
        loft_instance.inputs["Resolution U"].default_value = self.res_u
        loft_instance.inputs["Resolution V"].default_value = self.res_v
        
        return {
            "instance": loft_instance,
            "frame": frame
        }