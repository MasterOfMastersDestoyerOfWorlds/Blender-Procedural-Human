"""
DSL (Domain Specific Language) module for procedural generation.

This module provides a Python-based DSL for defining procedural structures
like fingers, limbs, and other segmented objects using classes with __init__ methods.
"""

from procedural_human.dsl.primitives import (
    DualRadial,
    QuadRadial,
    IKLimits,
    RadialAttachment,
    Joint,
    SegmentChain,
    JoinedStructure,
    AttachedStructure,
    normalize,
    last,
    Extend,
    Join,
    AttachRaycast,
)

__all__ = [
    "DualRadial",
    "QuadRadial",
    "IKLimits",
    "RadialAttachment",
    "Joint",
    "SegmentChain",
    "JoinedStructure",
    "AttachedStructure",
    "normalize",
    "last",
    "Extend",
    "Join",
    "AttachRaycast",
]


def register():
    """Register DSL module with Blender."""
    from procedural_human.dsl import operators
    from procedural_human.dsl import panel
    
    operators.register()
    panel.register()


def unregister():
    """Unregister DSL module from Blender."""
    from procedural_human.dsl import operators
    from procedural_human.dsl import panel
    
    panel.unregister()
    operators.unregister()

