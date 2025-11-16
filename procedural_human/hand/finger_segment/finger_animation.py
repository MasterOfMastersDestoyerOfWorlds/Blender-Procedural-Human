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
    
    # Ensure animation data exists
    if not armature.animation_data:
        armature.animation_data_create()
    
    # Create or get action
    action_name = f"{armature.name}_FingerCurl"
    if action_name in bpy.data.actions:
        action = bpy.data.actions[action_name]
    else:
        action = bpy.data.actions.new(name=action_name)
    
    armature.animation_data.action = action
    
    # Enter pose mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get all bones
    bones = [armature.pose.bones[f"Finger_Segment_{i + 1}"] for i in range(num_segments)]
    
    # Frame 0: Straight finger (all bones aligned - REST POSITION)
    bpy.context.scene.frame_set(frame_start)
    for bone in bones:
        # Ensure rest position - zero rotation
        bone.rotation_euler = Euler((0, 0, 0), 'XYZ')
        bone.keyframe_insert(data_path="rotation_euler", index=0, frame=frame_start)
        bone.keyframe_insert(data_path="rotation_euler", index=1, frame=frame_start)
        bone.keyframe_insert(data_path="rotation_euler", index=2, frame=frame_start)
    
    # Frame N: Curled finger
    # Calculate rotations so tip touches base and middle is orthogonal
    bpy.context.scene.frame_set(frame_end)
    
    if num_segments == 2:
        # Thumb: Two segments
        # Rotate first segment to curl
        bones[0].rotation_euler = Euler((math.radians(-45), 0, 0), 'XYZ')
        bones[0].keyframe_insert(data_path="rotation_euler", index=0, frame=frame_end)
        bones[0].keyframe_insert(data_path="rotation_euler", index=1, frame=frame_end)
        bones[0].keyframe_insert(data_path="rotation_euler", index=2, frame=frame_end)
        
        # Rotate second segment to complete curl
        bones[1].rotation_euler = Euler((math.radians(-90), 0, 0), 'XYZ')
        bones[1].keyframe_insert(data_path="rotation_euler", index=0, frame=frame_end)
        bones[1].keyframe_insert(data_path="rotation_euler", index=1, frame=frame_end)
        bones[1].keyframe_insert(data_path="rotation_euler", index=2, frame=frame_end)
    
    else:
        # Three segments: Index, Middle, Ring, Little
        # First segment (proximal) curls
        bones[0].rotation_euler = Euler((math.radians(-30), 0, 0), 'XYZ')
        bones[0].keyframe_insert(data_path="rotation_euler", index=0, frame=frame_end)
        bones[0].keyframe_insert(data_path="rotation_euler", index=1, frame=frame_end)
        bones[0].keyframe_insert(data_path="rotation_euler", index=2, frame=frame_end)
        
        # Second segment (middle) orthogonal to both
        bones[1].rotation_euler = Euler((math.radians(-60), 0, 0), 'XYZ')
        bones[1].keyframe_insert(data_path="rotation_euler", index=0, frame=frame_end)
        bones[1].keyframe_insert(data_path="rotation_euler", index=1, frame=frame_end)
        bones[1].keyframe_insert(data_path="rotation_euler", index=2, frame=frame_end)
        
        # Third segment (distal) curls to touch base
        bones[2].rotation_euler = Euler((math.radians(-60), 0, 0), 'XYZ')
        bones[2].keyframe_insert(data_path="rotation_euler", index=0, frame=frame_end)
        bones[2].keyframe_insert(data_path="rotation_euler", index=1, frame=frame_end)
        bones[2].keyframe_insert(data_path="rotation_euler", index=2, frame=frame_end)
    
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
    
    # Update view layer
    bpy.context.view_layer.update()

