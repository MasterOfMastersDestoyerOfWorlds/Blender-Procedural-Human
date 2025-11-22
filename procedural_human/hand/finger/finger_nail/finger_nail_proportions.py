"""
Fingernail proportion helpers.
"""

from procedural_human.hand.finger.finger_types import FingerType, ensure_finger_type


# Ratios are relative to the distal segment radius (width) or to that width.
# Defaults ensure the nail width stays near one third of the distal radius and
# that its height extends slightly longer than it is wide.
DEFAULT_NAIL_PROPORTIONS = {
    "width_ratio": 0.33,
    "height_ratio": 1.25,
}

FINGER_NAIL_PROPORTIONS = {
    FingerType.THUMB: {"width_ratio": 0.35, "height_ratio": 1.20},
    FingerType.INDEX: {"width_ratio": 0.33, "height_ratio": 1.30},
    FingerType.MIDDLE: {"width_ratio": 0.34, "height_ratio": 1.30},
    FingerType.RING: {"width_ratio": 0.33, "height_ratio": 1.25},
    FingerType.LITTLE: {"width_ratio": 0.32, "height_ratio": 1.10},
}


def get_fingernail_proportions(finger_type):
    """
    Return width/height ratios for the requested finger type.
    """
    enum_value = ensure_finger_type(finger_type)
    data = FINGER_NAIL_PROPORTIONS.get(enum_value, DEFAULT_NAIL_PROPORTIONS)

    width_ratio = data.get("width_ratio", DEFAULT_NAIL_PROPORTIONS["width_ratio"])
    height_ratio = data.get("height_ratio", DEFAULT_NAIL_PROPORTIONS["height_ratio"])

    return {
        "finger_type": enum_value,
        "width_ratio": width_ratio,
        "height_ratio": height_ratio,
    }

