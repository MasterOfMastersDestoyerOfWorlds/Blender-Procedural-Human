from enum import Enum
from typing import Iterable, Tuple


class FingerSegmentProperties(Enum):
    SEGMENT_RADIUS = "SegmentRadius"
    SEGMENT_LENGTH = "SegmentLength"
    SAMPLE_COUNT = "Sample Count"
    X_PROFILE_CURVE = "XProfileCurve"
    Y_PROFILE_CURVE = "YProfileCurve"


class JointSegmentProperties(Enum):
    """Properties for joint segments that connect regular segments"""
    
    START_RADIUS = "StartRadius"
    END_RADIUS = "EndRadius"
    OVERLAP_AMOUNT = "OverlapAmount"
    BLEND_FACTOR = "BlendFactor"
    THICKNESS_RATIO = "ThicknessRatio"
    SAMPLE_COUNT = "Sample Count"
