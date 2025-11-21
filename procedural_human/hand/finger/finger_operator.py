"""
Finger operator for Procedural Human Generator
"""

import bpy
from bpy.types import Operator, Panel
from bpy.props import FloatProperty, EnumProperty, BoolProperty
from procedural_human.hand.finger import finger_utils
from procedural_human.hand.finger.finger import (
    FingerData,
    get_finger_data,
    create_finger,
)
from procedural_human.hand.finger.finger_types import (
    FingerType,
    enum_items as finger_type_items,
)
from procedural_human.hand.finger import finger_animation as finger_animation
from procedural_human.operator_decorator import procedural_operator


@procedural_operator
class CreateFinger(Operator):
    """Create a procedural finger with Geometry Nodes"""

    finger_type = EnumProperty(
        name="Finger Type",
        items=list(finger_type_items()),
        default=FingerType.INDEX.value,
        description="Type of finger to generate",
    )

    curl_direction = EnumProperty(
        name="Curl Direction",
        items=[
            ("X", "X Axis", "Curl along X axis"),
            ("Y", "Y Axis", "Curl along Y axis"),
            ("Z", "Z Axis", "Curl along Z axis"),
        ],
        default="Y",
        description="Axis along which the finger curls",
    )

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
        finger = create_finger(self, context)
        finger = finger_utils.create_finger_geometry(finger)
        bpy.context.view_layer.objects.active = finger.blend_obj
        finger.blend_obj.select_set(True)
        return {"FINISHED"}


@procedural_operator
class RealizeFingerGeometry(Operator):
    """Apply Geometry Nodes modifier to selected finger object"""

    @classmethod
    def poll(cls, context):
        return (
            context.area.type == "VIEW_3D"
            and context.active_object
            and context.active_object.type == "MESH"
            and context.active_object.finger_data.is_finger
            and not context.active_object.finger_data.is_realized
        )

    def execute(self, context):
        finger = get_finger_data(context)
        try:
            finger_utils.realize_finger_geometry(finger)
            self.report({"INFO"}, "Finger geometry realized (modifier applied)")
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"Failed to realize geometry: {str(e)}")
            return {"CANCELLED"}


@procedural_operator
class AddArmatureFinger(Operator):
    """Add armature, bones, weights, IK, and animation to selected finger"""

    @classmethod
    def poll(cls, context):
        return (
            context.area.type == "VIEW_3D"
            and context.active_object
            and context.active_object.type == "MESH"
            and context.active_object.finger_data.is_finger
            and context.active_object.finger_data.is_realized
            and not context.active_object.finger_data.has_armature
            and not context.active_object.finger_data.has_ik
            and not context.active_object.finger_data.has_weights
        )

    def execute(self, context):
        finger = get_finger_data(context)
        try:
            armature = finger_utils.create_finger_armature(finger)
            finger_utils.paint_finger_weights(finger)
            finger_utils.setup_finger_ik(armature, finger)
            bpy.context.view_layer.objects.active = finger.blend_obj
            self.report(
                {"INFO"},
                f"Finger armature added successfully for {finger.finger_type} finger",
            )
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"Failed to add armature: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"CANCELLED"}


@procedural_operator
class CreateAnimationFinger(Operator):
    """Create keyframe animation for selected finger"""

    @classmethod
    def poll(cls, context):
        return (
            context.area.type == "VIEW_3D"
            and context.active_object
            and context.active_object.type == "MESH"
            and context.active_object.finger_data.is_finger
            and context.active_object.finger_data.has_armature
            and context.active_object.finger_data.has_ik
            and context.active_object.finger_data.has_weights
            and not context.active_object.finger_data.has_animation
        )

    def execute(self, context):
        finger = get_finger_data(context)
        try:
            armature = finger.blend_obj.modifiers.get("Armature").object
            finger_animation.create_finger_curl_animation(armature, finger)
            self.report(
                {"INFO"},
                f"Finger animation created successfully for {finger.finger_type} finger",
            )
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"Failed to create finger animation: {str(e)}")
            import traceback

            traceback.print_exc()
            return {"CANCELLED"}
