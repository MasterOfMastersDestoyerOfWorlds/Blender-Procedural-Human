"""
Operator classes for Procedural Human Generator
"""

import bpy
from procedural_human.decorators.operator_decorator import register_all_operators, unregister_all_operators

from procedural_human.utils import curve_serialization


def register():
    """Register all operators using the decorator system"""
    register_all_operators()


def unregister():
    """Unregister all operators using the decorator system"""
    unregister_all_operators()
