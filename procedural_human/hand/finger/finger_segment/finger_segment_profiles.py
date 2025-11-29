"""
Profile curve data for finger segments.

Each profile is a bezier curve normalized to 0-1 along the length,
with radius values as multipliers of the base segment radius.
"""

from enum import Enum


class ProfileType(Enum):
    """Types of profile curves"""

    X_PROFILE = "x_profile"
    Y_PROFILE = "y_profile"


class SegmentType(Enum):
    """Types of finger segments""" 

    PROXIMAL = "proximal"
    MIDDLE = "middle"
    DISTAL = "distal" 
    JOINT = "joint"