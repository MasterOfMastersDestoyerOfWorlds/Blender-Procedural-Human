"""
Operator classes for Procedural Human Generator
"""

import bpy
from .hand.finger import finger_operator



def register():
    finger_operator.register()


def unregister():
    finger_operator.unregister()
