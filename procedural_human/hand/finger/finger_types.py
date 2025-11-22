"""
Finger type enumeration and helpers.
"""

from enum import Enum
from typing import Iterable, Tuple

class FingerType(Enum):
    THUMB = "THUMB"
    INDEX = "INDEX"
    MIDDLE = "MIDDLE"
    RING = "RING"
    LITTLE = "LITTLE"

    @property
    def label(self) -> str:
        return {
            FingerType.THUMB: "Thumb",
            FingerType.INDEX: "Index",
            FingerType.MIDDLE: "Middle",
            FingerType.RING: "Ring",
            FingerType.LITTLE: "Little",
        }[self]

    @property
    def segment_count(self) -> int:
        return 2 if self is FingerType.THUMB else 3


def ensure_finger_type(value, default: FingerType = FingerType.INDEX) -> FingerType:
    """
    Convert an arbitrary value to a FingerType enum.
    """
    if isinstance(value, FingerType):
        return value
    if isinstance(value, str):
        key = value.strip().upper()
        if key in FingerType.__members__:
            return FingerType[key]
    return default


def enum_items() -> Iterable[Tuple[str, str, str]]:
    """
    Return Blender EnumProperty-friendly tuples.
    """
    for finger in FingerType:
        description = f"{finger.label} finger ({finger.segment_count} segments)"
        yield (finger.value, finger.label, description)

