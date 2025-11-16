"""
Finger operator for Procedural Human Generator
"""

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty, BoolProperty
from . import utils as finger_utils


class PROCEDURAL_OT_create_finger(Operator):
    bl_idname = "mesh.procedural_finger"
    bl_label = "Create Procedural Finger"
    bl_description = "Create a procedural finger with Geometry Nodes"
    bl_options = {"REGISTER", "UNDO"}

    # Finger type
    finger_type = EnumProperty(
        name="Finger Type",
        items=[
            ("THUMB", "Thumb", "Thumb finger (2 segments)"),
            ("INDEX", "Index", "Index finger (3 segments)"),
            ("MIDDLE", "Middle", "Middle finger (3 segments)"),
            ("RING", "Ring", "Ring finger (3 segments)"),
            ("LITTLE", "Little", "Little finger (3 segments)"),
        ],
        default="INDEX",
        description="Type of finger to generate",
    )

    # Curl direction
    curl_direction = EnumProperty(
        name="Curl Direction",
        items=[
            ("X", "X Axis", "Curl along X axis"),
            ("Y", "Y Axis", "Curl along Y axis (default)"),
            ("Z", "Z Axis", "Curl along Z axis"),
        ],
        default="Y",
        description="Axis along which the finger curls",
    )

    # Finger parameters
    radius = FloatProperty(
        name="Radius",
        default=0.007,
        min=0.004,
        max=0.012,
        description="Base finger radius",
    )

    nail_size = FloatProperty(
        name="Nail Size",
        default=0.003,
        min=0.001,
        max=0.006,
        description="Fingernail size",
    )

    taper_factor = FloatProperty(
        name="Taper Factor",
        default=0.15,
        min=0.0,
        max=0.5,
        description="How much radius decreases per segment (0.15 = 15% reduction)",
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        # Handle all property access robustly (works for both EnumProperty and FloatProperty)
        def get_property_value(prop_name, default):
            """Get actual value from Blender property"""
            try:
                val = getattr(self, prop_name, default)
                # Check if it's a deferred property
                if hasattr(val, '_default'):
                    return val._default
                elif hasattr(val, 'default'):
                    return val.default
                elif str(type(val)) == "<class 'bpy.props._PropertyDeferred'>":
                    return default
                else:
                    # Try to convert to appropriate type
                    if isinstance(default, (int, float)):
                        return float(val)
                    else:
                        return str(val)
            except Exception:
                return default
        
        finger_type_val = get_property_value("finger_type", "INDEX")
        curl_direction_val = get_property_value("curl_direction", "Y")
        nail_size_val = get_property_value("nail_size", 0.003)
        taper_val = get_property_value("taper_factor", 0.15)

        # Radius is now calculated from segment length (~1/2 of length)
        # Pass a default value but it will be overridden by calculation
        finger = finger_utils.create_finger_geometry(
            finger_type=finger_type_val,
            radius=0.007,  # Not used - calculated from segment length
            nail_size=nail_size_val,
            taper_factor=taper_val,
            curl_direction=curl_direction_val,
            total_length=1.0,
        )
        
        # Store finger type as custom property on the object
        finger["finger_type"] = finger_type_val
        finger["curl_direction"] = curl_direction_val
        
        bpy.context.view_layer.objects.active = finger
        finger.select_set(True)
        
        return {"FINISHED"}


class PROCEDURAL_OT_realize_finger_geometry(Operator):
    bl_idname = "mesh.procedural_realize_finger"
    bl_label = "Realize Finger Geometry"
    bl_description = "Apply Geometry Nodes modifier to selected finger object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.area.type == "VIEW_3D"
            and context.active_object
            and context.active_object.type == "MESH"
        )

    def execute(self, context):
        finger = context.active_object
        
        try:
            finger_utils.realize_finger_geometry(finger)
            self.report({"INFO"}, "Finger geometry realized (modifier applied)")
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"Failed to realize geometry: {str(e)}")
            return {"CANCELLED"}


class PROCEDURAL_OT_add_finger_armature(Operator):
    bl_idname = "mesh.procedural_add_finger_armature"
    bl_label = "Add Finger Armature"
    bl_description = "Add armature, bones, weights, IK, and animation to selected finger (reads finger type from object)"
    bl_options = {"REGISTER", "UNDO"}

    # Animation options
    create_animation = BoolProperty(
        name="Create Animation",
        default=True,
        description="Create keyframe animation for finger curl",
    )

    @classmethod
    def poll(cls, context):
        return (
            context.area.type == "VIEW_3D"
            and context.active_object
            and context.active_object.type == "MESH"
        )

    def execute(self, context):
        finger = context.active_object
        
        # Read finger type and curl direction from object custom properties
        finger_type_val = finger.get("finger_type", "INDEX")
        curl_direction_val = finger.get("curl_direction", "Y")
        
        # Get create_animation (bool property)
        create_anim = self.create_animation

        try:
            armature = finger_utils.add_finger_armature_to_object(
                finger,
                finger_type=finger_type_val,
                curl_direction=curl_direction_val,
                create_animation=create_anim,
            )
            self.report({"INFO"}, f"Finger armature added successfully for {finger_type_val} finger")
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"Failed to add armature: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"CANCELLED"}


# Registration
def register():
    bpy.utils.register_class(PROCEDURAL_OT_create_finger)
    bpy.utils.register_class(PROCEDURAL_OT_realize_finger_geometry)
    bpy.utils.register_class(PROCEDURAL_OT_add_finger_armature)


def unregister():
    bpy.utils.unregister_class(PROCEDURAL_OT_create_finger)
    bpy.utils.unregister_class(PROCEDURAL_OT_realize_finger_geometry)
    bpy.utils.unregister_class(PROCEDURAL_OT_add_finger_armature)

