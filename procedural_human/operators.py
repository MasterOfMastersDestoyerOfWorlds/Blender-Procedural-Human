"""
Operator classes for Procedural Human Generator
"""

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty
from . import utils


class PROCEDURAL_OT_create_human(Operator):
    bl_idname = "mesh.procedural_human"
    bl_label = "Procedural Human"
    bl_options = {"REGISTER", "UNDO"}

    # Body parameters
    height = FloatProperty(
        name="Height",
        default=1.7,
        min=1.0,
        max=2.5,
        description="Character height in meters",
    )

    build = FloatProperty(
        name="Build",
        default=0.5,
        min=0.0,
        max=1.0,
        description="Body build from thin to muscular",
    )

    # Head parameters
    head_scale = FloatProperty(name="Head Scale", default=1.0, min=0.5, max=1.5)

    # Limb parameters
    arm_length = FloatProperty(name="Arm Length", default=0.7, min=0.5, max=1.0)

    leg_length = FloatProperty(name="Leg Length", default=0.8, min=0.6, max=1.2)

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        # Handle Blender property access robustly
        def get_prop_value(prop_name, default):
            """Get actual numeric value from Blender property"""
            try:
                val = getattr(self, prop_name, default)
                # Handle _PropertyDeferred objects
                if hasattr(val, '_default'):
                    return val._default
                elif hasattr(val, 'default'):
                    return val.default
                elif str(type(val)) == "<class 'bpy.props._PropertyDeferred'>":
                    return default
                else:
                    return float(val)
            except:
                return default
        
        # Get property values with proper handling
        height_val = get_prop_value("height", 1.7)
        build_val = get_prop_value("build", 0.5)
        head_scale_val = get_prop_value("head_scale", 1.0)
        arm_length_val = get_prop_value("arm_length", 0.7)
        leg_length_val = get_prop_value("leg_length", 0.8)

        # Create main body components with parameters
        torso = utils.create_torso_geometry(height=height_val, build=build_val)

        # Create spine scaffold
        spine = utils.create_spine_curve()
        spine.hide_viewport = True
        spine.hide_render = True

        # Create head with parameters
        head = utils.create_head_geometry(head_scale=head_scale_val, height=height_val)

        # Calculate positions based on height
        shoulder_height = height_val * 0.75
        arm_end_height = shoulder_height * 0.6
        hip_height = height_val * 0.45
        knee_height = hip_height * 0.5

        # Create limbs with parameters
        # Arms - properly mirrored
        left_arm = utils.create_limb_geometry(
            "LeftArm",
            (0.3, 0, shoulder_height),
            (0.6, 0, arm_end_height),
            (0.45, 0, shoulder_height * 0.8),
            radius=0.06,
            length_scale=arm_length_val,
            build=build_val,
        )

        right_arm = utils.create_limb_geometry(
            "RightArm",
            (-0.3, 0, shoulder_height),
            (-0.6, 0, arm_end_height),
            (-0.45, 0, shoulder_height * 0.8),
            radius=0.06,
            length_scale=arm_length_val,
            build=build_val,
        )

        # Legs - properly mirrored and positioned
        left_leg = utils.create_limb_geometry(
            "LeftLeg",
            (0.12, 0, hip_height),
            (0.12, 0, 0.1),
            (0.12, 0, knee_height),
            radius=0.08,
            length_scale=leg_length_val,
            build=build_val,
        )

        right_leg = utils.create_limb_geometry(
            "RightLeg",
            (-0.12, 0, hip_height),
            (-0.12, 0, 0.1),
            (-0.12, 0, knee_height),
            radius=0.08,
            length_scale=leg_length_val,
            build=build_val,
        )

        # Create hands with proper positioning
        left_hand = utils.create_hand_geometry()
        left_hand.location = (0.6 * arm_length_val, 0, arm_end_height)

        right_hand = utils.create_hand_geometry()
        right_hand.location = (-0.6 * arm_length_val, 0, arm_end_height)

        # Parent all objects to torso
        for obj in [
            head,
            left_arm,
            right_arm,
            left_leg,
            right_leg,
            left_hand,
            right_hand,
        ]:
            obj.parent = torso

        # Select the torso as active
        bpy.context.view_layer.objects.active = torso
        torso.select_set(True)

        return {"FINISHED"}


class PROCEDURAL_OT_create_torso(Operator):
    bl_idname = "mesh.procedural_torso"
    bl_label = "Procedural Torso"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        torso = utils.create_torso_geometry()
        bpy.context.view_layer.objects.active = torso
        torso.select_set(True)
        return {"FINISHED"}


class PROCEDURAL_OT_create_head(Operator):
    bl_idname = "mesh.procedural_head"
    bl_label = "Procedural Head"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        head = utils.create_head_geometry()
        bpy.context.view_layer.objects.active = head
        head.select_set(True)
        return {"FINISHED"}


# Registration
def register():
    bpy.utils.register_class(PROCEDURAL_OT_create_human)
    bpy.utils.register_class(PROCEDURAL_OT_create_torso)
    bpy.utils.register_class(PROCEDURAL_OT_create_head)


def unregister():
    bpy.utils.unregister_class(PROCEDURAL_OT_create_head)
    bpy.utils.unregister_class(PROCEDURAL_OT_create_torso)
    bpy.utils.unregister_class(PROCEDURAL_OT_create_human)
