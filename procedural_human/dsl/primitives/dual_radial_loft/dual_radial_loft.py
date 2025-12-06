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
    Synthesizes a 3D surface from two 2D profile curves (Lofting).
    
    Takes the names of two Curve Objects in the scene:
    - curve_x: Defines the width profile (XZ plane).
    - curve_y: Defines the depth profile (YZ plane).
    
    The system uses raycasting to measuring the curves and 'Dual Radial' elliptical
    math to interpolate the surface between them.
    """
    curve_x: str  # Name of the object defining X silhouette
    curve_y: str  # Name of the object defining Y silhouette
    height: float = 1.0
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
        
        # Create Object Info nodes to fetch the curves
        # Note: We use 'Relative' transform so the user can place curves in the scene
        # and the rig will respect their local space relative to the generated object.
        
        obj_info_x = node_group.nodes.new("GeometryNodeObjectInfo")
        obj_info_x.transform_space = 'RELATIVE'
        # We need to assign the object. 
        # Since this runs during generation, we assume the objects exist.
        if self.curve_x in bpy.data.objects:
            obj_info_x.inputs["Object"].default_value = bpy.data.objects[self.curve_x]
        else:
            print(f"[DualRadialLoft] Warning: Curve object '{self.curve_x}' not found.")
            
        obj_info_y = node_group.nodes.new("GeometryNodeObjectInfo")
        obj_info_y.transform_space = 'RELATIVE'
        if self.curve_y in bpy.data.objects:
            obj_info_y.inputs["Object"].default_value = bpy.data.objects[self.curve_y]
        else:
            print(f"[DualRadialLoft] Warning: Curve object '{self.curve_y}' not found.")
            
        obj_info_x.parent = frame
        obj_info_y.parent = frame
        
        # Positioning
        x_pos, y_pos = context.get_next_y_offset(), 0 # Simple placement
        loft_instance.location = (x_pos, y_pos)
        obj_info_x.location = (x_pos - 200, y_pos + 100)
        obj_info_y.location = (x_pos - 200, y_pos - 100)
        
        # Linking
        node_group.links.new(obj_info_x.outputs["Geometry"], loft_instance.inputs["Curve X (Front)"])
        node_group.links.new(obj_info_y.outputs["Geometry"], loft_instance.inputs["Curve Y (Side)"])
        
        # Set Parameters
        loft_instance.inputs["Resolution U"].default_value = self.res_u
        loft_instance.inputs["Resolution V"].default_value = self.res_v
        loft_instance.inputs["Height"].default_value = self.height
        
        return {
            "instance": loft_instance,
            "frame": frame
        }
