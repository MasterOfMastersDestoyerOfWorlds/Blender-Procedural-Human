"""
Finger operator for Procedural Human Generator
"""

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty, BoolProperty
from . import utils as finger_utils


class PROCEDURAL_OT_create_finger(Operator):
    bl_idname = "mesh.procedural_finger"
    bl_label = "Procedural Finger"
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

    # Animation options
    create_animation = BoolProperty(
        name="Create Animation",
        default=True,
        description="Create keyframe animation for finger curl",
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        # Handle Blender property access robustly
        def get_prop_value(prop_name, default):
            """Get actual numeric value from Blender property"""
            try:
                val = getattr(self, prop_name, default)
                if hasattr(val, '_default'):
                    return val._default
                elif hasattr(val, 'default'):
                    return val.default
                elif str(type(val)) == "<class 'bpy.props._PropertyDeferred'>":
                    return default
                else:
                    return val
            except Exception:
                return default

        finger_type_val = get_prop_value("finger_type", "INDEX")
        curl_direction_val = get_prop_value("curl_direction", "Y")
        radius_val = get_prop_value("radius", 0.007)
        nail_size_val = get_prop_value("nail_size", 0.003)
        taper_val = get_prop_value("taper_factor", 0.15)
        create_anim = get_prop_value("create_animation", True)

        finger, armature = finger_utils.create_finger_geometry(
            finger_type=finger_type_val,
            radius=radius_val,
            nail_size=nail_size_val,
            taper_factor=taper_val,
            curl_direction=curl_direction_val,
            total_length=1.0,
            create_armature=True,
            create_animation=create_anim,
        )
        
        bpy.context.view_layer.objects.active = finger
        finger.select_set(True)
        
        # Select armature too if it exists
        if armature:
            armature.select_set(True)
        
        return {"FINISHED"}


# Registration
def register():
    bpy.utils.register_class(PROCEDURAL_OT_create_finger)


def unregister():
    bpy.utils.unregister_class(PROCEDURAL_OT_create_finger)

