from procedural_human.hand.finger.finger_types import FingerType, ensure_finger_type
from procedural_human.hand.finger import finger_proportions as proportions


class FingerData:
    def __init__(self, context):
        finger_object = context.active_object
        self.blend_obj: bpy.types.Object = finger_object
        self.location: tuple[float, float, float] = finger_object.location
        self.modifiers: list[bpy.types.Modifier] = finger_object.modifiers
        self.finger_type: FingerType = finger_object.get("finger_type", "INDEX")
        self.curl_direction: str = finger_object.get("curl_direction", "Y")

        self.scene: bpy.types.Scene = context.scene
        if hasattr(self.scene, "procedural_create_animation_finger"):
            self.create_animation: bool = self.scene.procedural_create_animation_finger
        else:
            self.create_animation: bool = self.create_animation
        self.finger_enum: FingerType = ensure_finger_type(self.finger_type)
        self.finger_proportions: dict = proportions.get_finger_proportions(
            self.finger_enum
        )
        self.num_segments: int = self.finger_proportions["segments"]
        self.total_length: float = 1.0
        self.segment_lengths: list[float] = (
            proportions.get_segment_lengths_blender_units(
                self.finger_enum, self.total_length
            )
        )
