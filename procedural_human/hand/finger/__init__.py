"""
Finger module for Procedural Human Generator
Contains finger generation code with Geometry Nodes
"""

from procedural_human.hand.finger import finger_utils
from procedural_human.hand.finger import finger_nodes
from procedural_human.hand.finger import finger_operator
from procedural_human.hand.finger import finger_proportions
from procedural_human.hand.finger import finger_animation
from procedural_human.hand.finger import finger_types
from procedural_human.hand.finger import finger_segment
from procedural_human.hand.finger import finger_nail
import bpy
from bpy.props import PointerProperty

from procedural_human.hand.fingerfinger import FingerDataProps

classes = (FingerDataProps,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.finger_data = PointerProperty(type=FingerDataProps)


def unregister():
    del bpy.types.Object.finger_data
    for cls in classes:
        bpy.utils.unregister_class(cls)
