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

    if ik_target:
        # Animate IK target translation to drive curl
        initial_location = ik_target.location.copy()
        bpy.context.scene.frame_set(frame_start)
        ik_target.location = initial_location
        ik_target.keyframe_insert(data_path="location", frame=frame_start)

        bpy.context.scene.frame_set(frame_end)
        curl_location = initial_location.copy()
        curl_location.z -= total_length * 0.6
        ik_target.location = curl_location
        ik_target.keyframe_insert(data_path="location", frame=frame_end)

        # Smooth interpolation
        if ik_target.animation_data and ik_target.animation_data.action:
            for fcurve in ik_target.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'BEZIER'
                    keyframe.handle_left_type = 'AUTO'
                    keyframe.handle_right_type = 'AUTO'
    else:
        # Fallback to direct bone keyframes if IK target not available
        if not armature.animation_data:
            armature.animation_data_create()
        action_name = f"{armature.name}_FingerCurl"
        if action_name in bpy.data.actions:
            action = bpy.data.actions[action_name]
        else:
            action = bpy.data.actions.new(name=action_name)
        armature.animation_data.action = action

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        bones = [armature.pose.bones[f"Finger_Segment_{i + 1}"] for i in range(finger.num_segments)]
        bpy.context.scene.frame_set(frame_start)
        for bone in bones:
            bone.rotation_euler = Euler((0, 0, 0), 'XYZ')
            bone.keyframe_insert(data_path="rotation_euler", frame=frame_start)

        bpy.context.scene.frame_set(frame_end)
        rotations = [math.radians(-30), math.radians(-60), math.radians(-60)]
        if finger.num_segments == 2:
            rotations = [math.radians(-45), math.radians(-90)]
        for idx, bone in enumerate(bones):
            rot = rotations[idx if idx < len(rotations) else -1]
            bone.rotation_euler = Euler((rot, 0, 0), 'XYZ')
            bone.keyframe_insert(data_path="rotation_euler", frame=frame_end)

        if armature.animation_data and armature.animation_data.action:
            for fcurve in armature.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'BEZIER'
                    keyframe.handle_left_type = 'AUTO'
                    keyframe.handle_right_type = 'AUTO'

        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    bpy.context.view_layer.update()

