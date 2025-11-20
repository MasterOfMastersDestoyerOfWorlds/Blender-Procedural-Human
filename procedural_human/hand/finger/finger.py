from procedural_human.hand.finger.finger_types import FingerType, ensure_finger_type
from procedural_human.hand.finger import finger_proportions as proportions
from procedural_human.utils import get_numeric_value, get_property_value
import bpy

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
)

from procedural_human.hand.finger.finger_types import FingerType, ensure_finger_type


class FingerDataProps(PropertyGroup):

    finger_type: EnumProperty(
        name="Finger Type",
        items=[(ft.name, ft.name, "") for ft in FingerType],
        default="INDEX",
    )

    curl_direction: EnumProperty(
        name="Curl Direction",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
        ],
        default="Y",
    )

    nail_size: FloatProperty(name="Nail Size", default=0.003, min=0.0, max=1.0)

    taper_factor: FloatProperty(name="Taper", default=0.15, min=0.0, max=1.0)

    radius: FloatProperty(name="Radius", default=0.007, min=0.0, max=1.0)

    total_length: FloatProperty(name="Total Length", default=1.0, min=0.0, max=10.0)

    num_segments: IntProperty(name="Segments", default=3, min=1, max=10)

    is_finger: BoolProperty(name="Is Finger", default=False)
    has_armature: BoolProperty(name="Has Armature", default=False)
    has_animation: BoolProperty(name="Has Animation", default=False)
    has_ik: BoolProperty(name="Has IK", default=False)
    has_weights: BoolProperty(name="Has Weights", default=False)
    is_realized: BoolProperty(name="Is Realized", default=False)


class FingerData:
    """Runtime generator that uses FingerDataProps values."""

    def __init__(self, obj, context):
        self.blend_obj = obj
        self.props = obj.finger_data

        self.mesh = obj.data

        self.finger_type = ensure_finger_type(self.props.finger_type)
        self.curl_direction = self.props.curl_direction
        self.nail_size = self.props.nail_size
        self.radius = self.props.radius
        self.taper_factor = self.props.taper_factor
        self.total_length = self.props.total_length

        self.finger_proportions = proportions.get_finger_proportions(self.finger_type)
        self.num_segments = self.finger_proportions["segments"]
        self.segment_lengths = proportions.get_segment_lengths_blender_units(
            self.finger_type, self.total_length
        )

        self.scene = context.scene


def create_finger(operator, context) -> FingerData:
    mesh = bpy.data.meshes.new("FingerMesh")
    mesh.from_pydata([(0, 0, 0)], [], [])
    obj = bpy.data.objects.new("Finger", mesh)
    context.collection.objects.link(obj)

    props = obj.finger_data
    props.radius = get_numeric_value(operator.radius, 0.007)
    props.taper_factor = get_numeric_value(operator.taper_factor, 0.15)
    props.nail_size = get_numeric_value(operator.nail_size, 0.003)
    props.finger_type = ensure_finger_type(operator.finger_type).value
    props.is_finger = True
    return FingerData(obj, context)


def get_finger_data(context) -> FingerData:
    obj = context.active_object

    return FingerData(obj, context)
