"""
Operator classes for Procedural Human Generator
"""

import bpy
from .operator_decorator import register_all_operators, unregister_all_operators

# Import operator modules to trigger decorator registration
from .hand.finger.finger_operator import (
    CreateFinger,
    RealizeFingerGeometry,
    AddArmatureFinger,
    CreateAnimationFinger,
)


def register():
    """Register all operators using the decorator system"""
    register_all_operators()


def unregister():
    """Unregister all operators using the decorator system"""
    unregister_all_operators()
