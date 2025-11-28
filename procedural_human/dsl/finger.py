"""
Finger DSL definition.

Defines procedural finger structures using the DSL primitives.
Profile curves are automatically looked up from the registry using
hierarchical naming: Index_Finger_Segment_0_X -> Finger_Segment_0_X -> default
"""

from typing import List
from procedural_human.dsl.primitives import (
    DualRadial,
    QuadRadial,
    IKLimits,
    Bone,
    RadialAttachment,
    Joint,
    normalize,
    last,
    Extend,
    Join,
    AttachRaycast,
)
from procedural_human.decorators.dsl_definition_decorator import dsl_definition


@dsl_definition
class Finger:
    """
    Procedural finger definition.
    
    A finger consists of:
    - N segments (DualRadial wrapped in Bone for armature creation)
    - N-1 joints (QuadRadial with 4 profile curves)
    - 1 nail attachment at the distal end (no bone needed)
    """
    
    def __init__(self, segment_lengths: List[float], radius_taper=0.85, curl_axis='Y'):
        Segment = DualRadial()
        
        self.norm_lengths = norm_lengths = normalize(segment_lengths)
        self.segments = []
        self.bones = []
        self.segment_lengths = segment_lengths
        self.radius_taper = radius_taper
        self.curl_axis = curl_axis
        radius = 0.5
        for i in range(len(segment_lengths)):
            seg = Segment(
                    length=segment_lengths[i],
                    radius=radius,
                    profile_lookup=i,
                )
            self.segments.append(seg)
            bone = Bone(
                geometry=seg,
                ik=IKLimits(x=(-10, 150), y=(-10, 10), z=(-5, 5))
            )
            self.bones.append(bone)
            radius = radius * radius_taper
        
        self.nail = RadialAttachment(
            type=DualRadial,
            size_ratio=0.3,
            rotation=curl_axis,
        )
        
        self.knuckle = Joint(
            type=QuadRadial,
            overlap=0.2,
            blend_factor=0.5,
        )
        
        self.finger_segment_chain = Extend(self.segments, axis='Z', norm_lengths=self.norm_lengths)
        self.finger_joints = Join(self.segments, self.knuckle)
        self.finger_nail_attachment = AttachRaycast(last(self.segments), self.nail)


# Finger instances with anatomical measurements (in mm)
Index = Finger([39.78, 22.38, 15.82])
Thumb = Finger([46.22, 21.67])
Middle = Finger([44.63, 26.33, 17.40])
Ring = Finger([41.37, 25.65, 17.30])
Little = Finger([32.74, 18.11, 15.96])
