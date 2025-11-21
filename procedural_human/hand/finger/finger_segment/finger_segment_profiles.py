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


DEFAULT_X_PROFILE_PROXIMAL = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (-0.05, 0.0, 0.0),
            "handle_right": (0.05, 0.0, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
        {
            "co": (0.0, 0.0, 0.5),
            "handle_left": (0.0, 0.0, -0.2),
            "handle_right": (0.0, 0.0, 0.2),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
            "radius": 1.05,
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (-0.05, 0.0, 0.0),
            "handle_right": (0.05, 0.0, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
    ]
}

DEFAULT_Y_PROFILE_PROXIMAL = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
        {
            "co": (0.0, 0.0, 0.5),
            "handle_left": (0.0, 0.0, -0.2),
            "handle_right": (0.0, 0.0, 0.2),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
            "radius": 1.05,
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
    ]
}

DEFAULT_X_PROFILE_MIDDLE = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (-0.05, 0.0, 0.0),
            "handle_right": (0.05, 0.0, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
        {
            "co": (0.0, 0.0, 0.5),
            "handle_left": (0.0, 0.0, -0.2),
            "handle_right": (0.0, 0.0, 0.2),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (-0.05, 0.0, 0.0),
            "handle_right": (0.05, 0.0, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
    ]
}

DEFAULT_Y_PROFILE_MIDDLE = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
        {
            "co": (0.0, 0.0, 0.5),
            "handle_left": (0.0, 0.0, -0.2),
            "handle_right": (0.0, 0.0, 0.2),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
    ]
}

DEFAULT_X_PROFILE_DISTAL = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
        {
            "co": (0.0, 0.0, 0.5),
            "handle_left": (0.0, 0.0, -0.15),
            "handle_right": (0.0, 0.0, 0.15),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
            "radius": 0.92,
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
    ]
}

DEFAULT_Y_PROFILE_DISTAL = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
        {
            "co": (0.0, 0.0, 0.5),
            "handle_left": (0.0, 0.0, -0.15),
            "handle_right": (0.0, 0.0, 0.15),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
            "radius": 0.92,
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (0.0, -0.05, 0.0),
            "handle_right": (0.0, 0.05, 0.0),
            "handle_left_type": "AUTO",
            "handle_right_type": "AUTO",
        },
    ]
}


PROFILE_DATA = {
    SegmentType.PROXIMAL: {
        ProfileType.X_PROFILE: DEFAULT_X_PROFILE_PROXIMAL,
        ProfileType.Y_PROFILE: DEFAULT_Y_PROFILE_PROXIMAL,
    },
    SegmentType.MIDDLE: {
        ProfileType.X_PROFILE: DEFAULT_X_PROFILE_MIDDLE,
        ProfileType.Y_PROFILE: DEFAULT_Y_PROFILE_MIDDLE,
    },
    SegmentType.DISTAL: {
        ProfileType.X_PROFILE: DEFAULT_X_PROFILE_DISTAL,
        ProfileType.Y_PROFILE: DEFAULT_Y_PROFILE_DISTAL,
    },
}


def get_profile_data(segment_type: SegmentType, profile_type: ProfileType):
    """
    Get profile data for a given segment and profile type.

    Args:
        segment_type: SegmentType enum
        profile_type: ProfileType enum

    Returns:
        Profile data dictionary
    """

    return PROFILE_DATA[segment_type][profile_type]


__all__ = [
    "ProfileType",
    "SegmentType",
    "PROFILE_DATA",
    "get_profile_data",
    "DEFAULT_X_PROFILE_PROXIMAL",
    "DEFAULT_Y_PROFILE_PROXIMAL",
    "DEFAULT_X_PROFILE_MIDDLE",
    "DEFAULT_Y_PROFILE_MIDDLE",
    "DEFAULT_X_PROFILE_DISTAL",
    "DEFAULT_Y_PROFILE_DISTAL",
]
