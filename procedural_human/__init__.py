"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes
"""

import bpy
from . import operators
from . import panels
from . import menus
from procedural_human.hand.finger.finger_types import (
    FingerType,
    
    enum_items as finger_type_items,
)
import procedural_human.hand.finger as finger


def update_profile_curves(self, context):
    """
    Update callback for profile curve changes.
    Finds all finger objects and updates their geometry node trees.
    """
    # Find all finger objects with geometry nodes
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and hasattr(obj, 'finger_data'):
            if obj.finger_data.is_finger:
                # Find geometry nodes modifier
                for modifier in obj.modifiers:
                    if modifier.type == 'NODES' and modifier.node_group:
                        # Update will happen automatically when nodes reference scene properties
                        # Force a viewport update
                        pass
    
    # Force viewport update
    if context.view_layer:
        context.view_layer.update()
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
    
    # Collapsible section properties
    bpy.types.Scene.procedural_finger_expanded = bpy.props.BoolProperty(
        name="Finger Expanded",
        default=True,
        description="Show/hide finger panel content",
    )
    
    bpy.types.Scene.procedural_finger_nail_expanded = bpy.props.BoolProperty(
        name="Finger Nail Expanded",
        default=False,
        description="Show/hide finger nail panel content",
    )
    
    bpy.types.Scene.procedural_finger_segment_expanded = bpy.props.BoolProperty(
        name="Finger Segment Expanded",
        default=False,
        description="Show/hide finger segment panel content",
    )
    
    # Profile curve pointer properties for each segment type
    # Proximal segment
    bpy.types.Scene.procedural_segment_proximal_x_profile = bpy.props.PointerProperty(
        name="Proximal X Profile",
        type=bpy.types.Object,
        description="X-axis profile curve for proximal finger segment",
        poll=lambda self, obj: obj.type == 'CURVE',
        update=update_profile_curves,
    )
    
    bpy.types.Scene.procedural_segment_proximal_y_profile = bpy.props.PointerProperty(
        name="Proximal Y Profile",
        type=bpy.types.Object,
        description="Y-axis profile curve for proximal finger segment",
        poll=lambda self, obj: obj.type == 'CURVE',
        update=update_profile_curves,
    )
    
    # Middle segment
    bpy.types.Scene.procedural_segment_middle_x_profile = bpy.props.PointerProperty(
        name="Middle X Profile",
        type=bpy.types.Object,
        description="X-axis profile curve for middle finger segment",
        poll=lambda self, obj: obj.type == 'CURVE',
        update=update_profile_curves,
    )
    
    bpy.types.Scene.procedural_segment_middle_y_profile = bpy.props.PointerProperty(
        name="Middle Y Profile",
        type=bpy.types.Object,
        description="Y-axis profile curve for middle finger segment",
        poll=lambda self, obj: obj.type == 'CURVE',
        update=update_profile_curves,
    )
    
    # Distal segment
    bpy.types.Scene.procedural_segment_distal_x_profile = bpy.props.PointerProperty(
        name="Distal X Profile",
        type=bpy.types.Object,
        description="X-axis profile curve for distal finger segment",
        poll=lambda self, obj: obj.type == 'CURVE',
        update=update_profile_curves,
    )
    
    bpy.types.Scene.procedural_segment_distal_y_profile = bpy.props.PointerProperty(
        name="Distal Y Profile",
        type=bpy.types.Object,
        description="Y-axis profile curve for distal finger segment",
        poll=lambda self, obj: obj.type == 'CURVE',
        update=update_profile_curves,
    )


def unregister_scene_properties():
    """Unregister scene properties"""
    del bpy.types.Scene.procedural_finger_type
    del bpy.types.Scene.procedural_finger_curl_direction
    del bpy.types.Scene.procedural_create_animation_finger
    
    # Collapsible section properties
    del bpy.types.Scene.procedural_finger_expanded
    del bpy.types.Scene.procedural_finger_nail_expanded
    del bpy.types.Scene.procedural_finger_segment_expanded
    
    # Profile curve pointer properties
    del bpy.types.Scene.procedural_segment_proximal_x_profile
    del bpy.types.Scene.procedural_segment_proximal_y_profile
    del bpy.types.Scene.procedural_segment_middle_x_profile
    del bpy.types.Scene.procedural_segment_middle_y_profile
    del bpy.types.Scene.procedural_segment_distal_x_profile
    del bpy.types.Scene.procedural_segment_distal_y_profile


def register():
    register_scene_properties()
    operators.register()
    panels.register()
    menus.register()
    finger.register()


def unregister():
    menus.unregister()
    panels.unregister()
    operators.unregister()
    unregister_scene_properties()
    finger.unregister()


if __name__ == "__main__":
    register()
