"""
Finger animation functions for Procedural Human Generator
"""

import bpy
from mathutils import Vector, Euler
import math


def create_finger_curl_animation(armature, num_segments):
    """
    Create keyframe animation for finger curl
    
    Args:
        armature: Armature object
        num_segments: Number of segments (2 or 3)
    """
    # Set frame range
    frame_start = 0
    frame_end = 30
    
    # Enter pose mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get all bones
    bones = [armature.pose.bones[f"Finger_Segment_{i + 1}"] for i in range(num_segments)]
    
    # Frame 0: Straight finger (all bones aligned)
    bpy.context.scene.frame_set(frame_start)
    for bone in bones:
        bone.rotation_euler = Euler((0, 0, 0), 'XYZ')
        bone.keyframe_insert(data_path="rotation_euler", index=0)
        bone.keyframe_insert(data_path="rotation_euler", index=1)
        bone.keyframe_insert(data_path="rotation_euler", index=2)
    
    # Frame N: Curled finger
    # Calculate rotations so tip touches base and middle is orthogonal
    bpy.context.scene.frame_set(frame_end)
    
    if num_segments == 2:
        # Thumb: Two segments
        # Rotate first segment to curl
        bones[0].rotation_euler = Euler((math.radians(-45), 0, 0), 'XYZ')
        bones[0].keyframe_insert(data_path="rotation_euler", index=0)
        bones[0].keyframe_insert(data_path="rotation_euler", index=1)
        bones[0].keyframe_insert(data_path="rotation_euler", index=2)
        
        # Rotate second segment to complete curl
        bones[1].rotation_euler = Euler((math.radians(-90), 0, 0), 'XYZ')
        bones[1].keyframe_insert(data_path="rotation_euler", index=0)
        bones[1].keyframe_insert(data_path="rotation_euler", index=1)
        bones[1].keyframe_insert(data_path="rotation_euler", index=2)
    
    else:
        # Three segments: Index, Middle, Ring, Little
        # First segment (proximal) curls
        bones[0].rotation_euler = Euler((math.radians(-30), 0, 0), 'XYZ')
        bones[0].keyframe_insert(data_path="rotation_euler", index=0)
        bones[0].keyframe_insert(data_path="rotation_euler", index=1)
        bones[0].keyframe_insert(data_path="rotation_euler", index=2)
        
        # Second segment (middle) orthogonal to both
        bones[1].rotation_euler = Euler((math.radians(-60), 0, 0), 'XYZ')
        bones[1].keyframe_insert(data_path="rotation_euler", index=0)
        bones[1].keyframe_insert(data_path="rotation_euler", index=1)
        bones[1].keyframe_insert(data_path="rotation_euler", index=2)
        
        # Third segment (distal) curls to touch base
        bones[2].rotation_euler = Euler((math.radians(-60), 0, 0), 'XYZ')
        bones[2].keyframe_insert(data_path="rotation_euler", index=0)
        bones[2].keyframe_insert(data_path="rotation_euler", index=1)
        bones[2].keyframe_insert(data_path="rotation_euler", index=2)
    
    # Set interpolation to bezier for smooth animation
    if armature.animation_data and armature.animation_data.action:
        for fcurve in armature.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'BEZIER'
                keyframe.handle_left_type = 'AUTO'
                keyframe.handle_right_type = 'AUTO'
    
    # Exit pose mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Set playback range
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

