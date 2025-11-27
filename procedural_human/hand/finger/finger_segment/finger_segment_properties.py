from enum import Enum
from typing import Iterable, Tuple


class FingerSegmentProperties(Enum):
    SEGMENT_RADIUS = "SegmentRadius"
    SEGMENT_LENGTH = "SegmentLength"
    SAMPLE_COUNT = "Sample Count"
    X_PROFILE_CURVE = "XProfileCurve"
    Y_PROFILE_CURVE = "YProfileCurve"


class JointSegmentProperties(Enum):
    PREV_SEGMENT = "Previous Segment"
    NEXT_SEGMENT = "Next Segment"
    PREV_SEGMENT_START = "Prev Segment Start"
    NEXT_SEGMENT_START = "Next Segment Start"
    CURVE_0 = "0° Float Curve"
    CURVE_90 = "90° Float Curve"
    CURVE_180 = "180° Float Curve"
    CURVE_270 = "270° Float Curve"
    SAMPLE_COUNT = "Sample Count"
