"""
DSL primitive classes for procedural generation.

These classes map to geometry node groups in the codebase:
- DualRadial -> dual_radial.py (X, Y profile curves)
- QuadRadial -> quad_radial.py (0°, 90°, 180°, 270° curves)
- Joint -> joint_segment_nodes.py (uses QuadRadial)
- RadialAttachment -> finger_nail_nodes.py (terminal attachments)
- IKLimits -> finger_utils.py IK constraint setup
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Any, Dict
from enum import Enum


class ProfileType(Enum):
    """Types of profile curves based on radial type."""
    DUAL_X = "X"
    DUAL_Y = "Y"
    QUAD_0 = "0"
    QUAD_90 = "90"
    QUAD_180 = "180"
    QUAD_270 = "270"


@dataclass
class IKLimits:
    """
    Inverse Kinematics limits for bone constraints.
    
    Each axis tuple is (min_degrees, max_degrees).
    """
    x: Tuple[float, float] = (-10, 150)
    y: Tuple[float, float] = (-10, 10)
    z: Tuple[float, float] = (-5, 5)
    
    def to_radians(self) -> Dict[str, Tuple[float, float]]:
        """Convert limits to radians for Blender."""
        import math
        return {
            'x': (math.radians(self.x[0]), math.radians(self.x[1])),
            'y': (math.radians(self.y[0]), math.radians(self.y[1])),
            'z': (math.radians(self.z[0]), math.radians(self.z[1])),
        }


@dataclass
class DualRadial:
    """
    Dual-axis radial profile segment.
    
    Uses X and Y profile curves for organic cross-sections.
    Maps to: procedural_human/geo_node_groups/dual_radial.py
    """
    ik: Optional[IKLimits] = None
    profile_type: str = "dual"
    length: float = 1.0
    radius: float = 1.0
    profile_lookup: Optional[int] = None
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    _index: Optional[int] = field(default=None, repr=False)
    
    def __call__(self, length: float = 1.0, radius: float = 1.0, 
                 profile_lookup: Optional[int] = None) -> 'DualRadial':
        """Create a segment instance with specific parameters."""
        instance = DualRadial(
            ik=self.ik,
            profile_type=self.profile_type,
            length=length,
            radius=radius,
            profile_lookup=profile_lookup,
        )
        instance._naming_context = self._naming_context
        instance._index = profile_lookup
        return instance
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names this type uses."""
        return [ProfileType.DUAL_X.value, ProfileType.DUAL_Y.value]


@dataclass
class QuadRadial:
    """
    Quad-axis radial profile for joints.
    
    Uses 4 profile curves at 0°, 90°, 180°, 270° for joint geometry.
    Maps to: procedural_human/geo_node_groups/quad_radial.py
    """
    profile_type: str = "quad"
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names this type uses."""
        return [
            ProfileType.QUAD_0.value,
            ProfileType.QUAD_90.value,
            ProfileType.QUAD_180.value,
            ProfileType.QUAD_270.value,
        ]


@dataclass
class Joint:
    """
    Joint connector between segments.
    
    Uses QuadRadial for smooth transitions between segments.
    Maps to: procedural_human/hand/finger/finger_segment/joint_segment_nodes.py
    """
    type: type = QuadRadial
    overlap: float = 0.2
    blend_factor: float = 0.5
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    _index: Optional[int] = field(default=None, repr=False)
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names based on joint type."""
        if self.type == QuadRadial or isinstance(self.type, QuadRadial):
            return QuadRadial().get_profile_names()
        return []


@dataclass
class RadialAttachment:
    """
    Terminal attachment (like fingernail) that attaches to segment end.
    
    Maps to: procedural_human/hand/finger/finger_nail/finger_nail_nodes.py
    """
    type: type = DualRadial
    size_ratio: float = 0.3
    rotation: str = 'Y'
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names based on attachment type."""
        if self.type == DualRadial or isinstance(self.type, DualRadial):
            return DualRadial().get_profile_names()
        return []


@dataclass
class SegmentChain:
    """Result of Extend() - a chain of segments along an axis."""
    segments: List[Any]
    axis: str = 'Z'
    
    def __iter__(self):
        return iter(self.segments)
    
    def __len__(self):
        return len(self.segments)
    
    def __getitem__(self, index):
        return self.segments[index]


@dataclass
class JoinedStructure:
    """Result of Join() - segments with joints between them."""
    segments: List[Any]
    joints: List[Joint]
    joint_template: Joint
    
    def get_all_components(self) -> List[Any]:
        """Return interleaved segments and joints."""
        result = []
        for i, seg in enumerate(self.segments):
            result.append(seg)
            if i < len(self.joints):
                result.append(self.joints[i])
        return result


@dataclass 
class AttachedStructure:
    """Result of AttachRaycast() - segment with terminal attachment."""
    segment: Any
    attachment: RadialAttachment


def normalize(lengths: List[float]) -> List[float]:
    """Normalize a list of lengths to ratios that sum to 1.0."""
    if not lengths:
        return []
    total = sum(lengths)
    if total == 0:
        return [1.0 / len(lengths)] * len(lengths)
    return [length / total for length in lengths]


def last(items: List[Any]) -> Any:
    """Get the last item from a list."""
    if not items:
        raise IndexError("Cannot get last item from empty list")
    return items[-1]


def Extend(segments: List[Any], axis: str = 'Z') -> SegmentChain:
    """Chain segments along an axis."""
    return SegmentChain(segments=segments, axis=axis)


def Join(segments: List[Any], joint: Joint) -> JoinedStructure:
    """Insert joints between segments."""
    if isinstance(segments, SegmentChain):
        segment_list = segments.segments
    else:
        segment_list = segments
    
    joints = []
    for i in range(len(segment_list) - 1):
        joint_instance = Joint(
            type=joint.type,
            overlap=joint.overlap,
            blend_factor=joint.blend_factor,
        )
        joint_instance._index = i
        joint_instance._naming_context = joint._naming_context
        joints.append(joint_instance)
    
    return JoinedStructure(
        segments=segment_list,
        joints=joints,
        joint_template=joint,
    )


def AttachRaycast(segment: Any, attachment: RadialAttachment) -> AttachedStructure:
    """Attach a terminal to the end of a segment using raycast positioning."""
    return AttachedStructure(segment=segment, attachment=attachment)


Segment = DualRadial

