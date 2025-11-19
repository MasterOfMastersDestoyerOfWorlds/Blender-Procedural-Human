"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes
"""

import bpy
from . import operators
from . import panels
from . import menus
from .hand.finger.finger_types import (
    FingerType,
    enum_items as finger_type_items,
)

bl_info = {
    "name": "Procedural Human Generator",
    "author": "Procedural Human Team",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh",
    "description": "Generates complete procedural humans using Geometry Nodes",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


# Scene properties for finger operations
def register_scene_properties():
    """Register scene properties for finger operations"""
    bpy.types.Scene.procedural_finger_type = bpy.props.EnumProperty(
        name="Finger Type",
        items=list(finger_type_items()),
        default=FingerType.INDEX.value,
        description="Type of finger to generate",
    )
    
    bpy.types.Scene.procedural_finger_curl_direction = bpy.props.EnumProperty(
        name="Curl Direction",
        items=[
            ("X", "X Axis", "Curl along X axis"),
            ("Y", "Y Axis", "Curl along Y axis (default)"),
            ("Z", "Z Axis", "Curl along Z axis"),
        ],
        default="Y",
        description="Axis along which the finger curls",
    )
    
    bpy.types.Scene.procedural_create_animation_finger = bpy.props.BoolProperty(
        name="Create Animation",
        default=True,
        description="Create keyframe animation for finger curl",
    )


def unregister_scene_properties():
    """Unregister scene properties"""
    del bpy.types.Scene.procedural_finger_type
    del bpy.types.Scene.procedural_finger_curl_direction
    del bpy.types.Scene.procedural_create_animation_finger


# Registration
def register():
    register_scene_properties()
    operators.register()
    panels.register()
    menus.register()


def unregister():
    menus.unregister()
    panels.unregister()
    operators.unregister()
    unregister_scene_properties()


if __name__ == "__main__":
    register()
