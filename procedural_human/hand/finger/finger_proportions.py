"""
Finger proportions data from anatomical measurements.
"""

from procedural_human.hand.finger.finger_types import (
    FingerType,
    ensure_finger_type,
)

# Finger proportions in mm (from Proportions.md)
FINGER_PROPORTIONS = {
    FingerType.THUMB: {
        "segments": 2,
        "lengths_mm": [46.22, 21.67],  # Proximal, Distal
        "names": ["Proximal", "Distal"],
    },
    FingerType.INDEX: {
        "segments": 3,
        "lengths_mm": [39.78, 22.38, 15.82],  # Proximal, Middle, Distal
        "names": ["Proximal", "Middle", "Distal"],
    },
    FingerType.MIDDLE: {
        "segments": 3,
        "lengths_mm": [44.63, 26.33, 17.40],  # Proximal, Middle, Distal
        "names": ["Proximal", "Middle", "Distal"],
    },
    FingerType.RING: {
        "segments": 3,
        "lengths_mm": [41.37, 25.65, 17.30],  # Proximal, Middle, Distal
        "names": ["Proximal", "Middle", "Distal"],
    },
    FingerType.LITTLE: {
        "segments": 3,
        "lengths_mm": [32.74, 18.11, 15.96],  # Proximal, Middle, Distal
        "names": ["Proximal", "Middle", "Distal"],
    },
}


def get_finger_proportions(finger_type):
    """
    Get finger proportions for a given finger type.
    """
    enum_value = ensure_finger_type(finger_type)
    data = FINGER_PROPORTIONS[enum_value]

    lengths = list(data["lengths_mm"])
    total_mm = sum(lengths)

    return {
        "finger_type": enum_value,
        "segments": data["segments"],
        "lengths_mm": lengths,
        "names": list(data["names"]),
        "total_mm": total_mm,
        "ratios": [length / total_mm for length in lengths],
    }


def get_segment_lengths_blender_units(finger_type, total_length=1.0):
    """
    Get segment lengths in blender units, normalized to total_length.
    """
    proportions = get_finger_proportions(finger_type)
    return [ratio * total_length for ratio in proportions["ratios"]]


__all__ = [
    "FINGER_PROPORTIONS",
    "get_finger_proportions",
    "get_segment_lengths_blender_units",
]