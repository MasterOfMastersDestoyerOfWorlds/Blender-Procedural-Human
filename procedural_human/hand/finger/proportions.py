"""
Finger proportions data from anatomical measurements
"""

# Finger proportions in mm (from Proportions.md)
FINGER_PROPORTIONS = {
    "THUMB": {
        "segments": 2,
        "lengths_mm": [21.67, 46.22],  # Distal, Proximal
        "names": ["Distal", "Proximal"],
    },
    "INDEX": {
        "segments": 3,
        "lengths_mm": [15.82, 22.38, 39.78],  # Distal, Middle, Proximal
        "names": ["Distal", "Middle", "Proximal"],
    },
    "MIDDLE": {
        "segments": 3,
        "lengths_mm": [17.40, 26.33, 44.63],  # Distal, Middle, Proximal
        "names": ["Distal", "Middle", "Proximal"],
    },
    "RING": {
        "segments": 3,
        "lengths_mm": [17.30, 25.65, 41.37],  # Distal, Middle, Proximal
        "names": ["Distal", "Middle", "Proximal"],
    },
    "LITTLE": {
        "segments": 3,
        "lengths_mm": [15.96, 18.11, 32.74],  # Distal, Middle, Proximal
        "names": ["Distal", "Middle", "Proximal"],
    },
}


def get_finger_proportions(finger_type):
    """
    Get finger proportions for a given finger type
    
    Args:
        finger_type: One of "THUMB", "INDEX", "MIDDLE", "RING", "LITTLE"
    
    Returns:
        dict with 'segments', 'lengths_mm', 'names', 'total_mm', 'ratios'
    """
    if finger_type not in FINGER_PROPORTIONS:
        finger_type = "INDEX"  # Default fallback
    
    data = FINGER_PROPORTIONS[finger_type].copy()
    total_mm = sum(data["lengths_mm"])
    data["total_mm"] = total_mm
    data["ratios"] = [length / total_mm for length in data["lengths_mm"]]
    
    return data


def get_segment_lengths_blender_units(finger_type, total_length=1.0):
    """
    Get segment lengths in blender units, normalized to total_length
    
    Args:
        finger_type: One of "THUMB", "INDEX", "MIDDLE", "RING", "LITTLE"
        total_length: Total finger length in blender units (default 1.0)
    
    Returns:
        list of segment lengths in blender units
    """
    proportions = get_finger_proportions(finger_type)
    ratios = proportions["ratios"]
    return [ratio * total_length for ratio in ratios]

