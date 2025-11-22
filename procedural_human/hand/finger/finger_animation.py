"""
Finger animation functions for Procedural Human Generator
"""

import bpy
from mathutils import Vector, Euler
import math

from procedural_human.hand.finger.finger import FingerData


def create_finger_curl_animation(armature: bpy.types.Object, finger: FingerData):
    """
    Create keyframe animation for finger curl
    
    Args:
        armature: Armature object
        finger: Finger data
    """
    frame_start = 0
    frame_end = 30
    segment_lengths = armature.get("finger_segment_lengths", [1.0 / finger.num_segments] * finger.num_segments)
    total_length = sum(segment_lengths)
    ik_target_name = armature.get("finger_ik_target")
    ik_target = bpy.data.objects.get(ik_target_name) if ik_target_name else None
    
    initial_location = ik_target.location.copy()
    bpy.context.scene.frame_set(frame_start)
    ik_target.location = initial_location
    ik_target.keyframe_insert(data_path="location", frame=frame_start)

    bpy.context.scene.frame_set(frame_end)
    curl_location = initial_location.copy()
    curl_location.z -= total_length * 0.6
    ik_target.location = curl_location
    ik_target.keyframe_insert(data_path="location", frame=frame_end)
    if ik_target.animation_data and ik_target.animation_data.action:
        for fcurve in ik_target.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'BEZIER'
                keyframe.handle_left_type = 'AUTO'
                keyframe.handle_right_type = 'AUTO'
   
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    bpy.context.view_layer.update()

