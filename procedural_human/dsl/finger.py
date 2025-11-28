"""
Finger DSL definition.

Defines procedural finger structures using the DSL primitives.
Profile curves are automatically looked up from the registry using
hierarchical naming: Index_Finger_Segment_0_X -> Finger_Segment_0_X -> default
"""

from procedural_human.dsl.primitives import (
    DualRadial,
    QuadRadial,
    IKLimits,
    RadialAttachment,
    Joint,
    normalize,
    last,
    Extend,
    Join,
    AttachRaycast,
)


class Finger:
    """
    Procedural finger definition.
    
    A finger consists of:
    - N segments (DualRadial with X/Y profile curves)
    - N-1 joints (QuadRadial with 4 profile curves)
    - 1 nail attachment at the distal end
    """
    
    def __init__(self, segment_lengths=None, radius_taper=0.85, curl_axis='Y'):
        if segment_lengths is None:
            segment_lengths = [1.0, 0.6, 0.4]
        
        Segment = DualRadial(
            ik=IKLimits(x=(-10, 150), y=(-10, 10), z=(-5, 5))
        )
        
        norm_lengths = normalize(segment_lengths)
        
        segments = []
        radius = 1.0
        
        for i in range(len(segment_lengths)):
            seg = Segment(
                length=segment_lengths[i],
                radius=radius,
                profile_lookup=i,
            )
            segments.append(seg)
            radius = radius * radius_taper
        
        self.segments = segments
        self.segment_lengths = segment_lengths
        self.norm_lengths = norm_lengths
        self.radius_taper = radius_taper
        self.curl_axis = curl_axis
        
        Nail = RadialAttachment(
            type=DualRadial,
            size_ratio=0.3,
            rotation=curl_axis,
        )
        self.nail = Nail
        
        Knuckle = Joint(
            type=QuadRadial,
            overlap=0.2,
            blend_factor=0.5,
        )
        self.knuckle_template = Knuckle
        
        self._segment_chain = Extend(segments, axis='Z', norm_lengths=norm_lengths)
        self._joined_structure = Join(segments, Knuckle)
        self.joints = self._joined_structure.joints
        self._nail_attachment = AttachRaycast(last(segments), Nail)
    
    def get_total_length(self):
        """Get total finger length."""
        return sum(self.segment_lengths)
    
    def get_segment_count(self):
        """Get number of segments."""
        return len(self.segments)
    
    def get_joint_count(self):
        """Get number of joints."""
        return len(self.joints)


# Finger instances with anatomical measurements (in mm)
Index = Finger([39.78, 22.38, 15.82])
Thumb = Finger([46.22, 21.67])
Middle = Finger([44.63, 26.33, 17.40])
Ring = Finger([41.37, 25.65, 17.30])
Little = Finger([32.74, 18.11, 15.96])

