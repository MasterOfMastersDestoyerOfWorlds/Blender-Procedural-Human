"""
Finger module for Procedural Human Generator
Contains finger generation code with Geometry Nodes
"""

from . import finger_utils
from . import finger_nodes
from . import finger_operator
from . import finger_proportions
from . import finger_animation
from . import finger_types
from . import finger_segment
from . import finger_nail
import bpy
from bpy.props import PointerProperty

__all__ = [
    "finger_utils",
    "finger_nodes",
    "finger_operator",
    "finger_proportions",
    "finger_animation",
    "finger_types",
    "finger_segment",
    "finger_nail",
]
from .finger import FingerDataProps

classes = (FingerDataProps,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.finger_data = PointerProperty(type=FingerDataProps)


def unregister():
    del bpy.types.Object.finger_data
    for cls in classes:
        bpy.utils.unregister_class(cls)
