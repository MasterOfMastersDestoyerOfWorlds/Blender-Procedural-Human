from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive
from procedural_human.dsl.primitives.ik.ik import IKLimits


@dsl_primitive
@dataclass
class Bone:
    """
    Metadata container for armature bone creation.

    References a geometry-generating primitive (DualRadial, QuadRadial, etc.)
    and specifies IK limits. Does NOT generate geometry nodes - that's done
    by the segments list. This is purely metadata for armature creation.

    Usage:
        seg = DualRadial(length=10, radius=1.0, profile_lookup=0)
        segments.append(seg)  # This generates geometry
        bones.append(Bone(geometry=seg, ik=IKLimits(...)))  # This is metadata
    """

    geometry: Any = None
    ik: Optional[IKLimits] = None
    _index: Optional[int] = field(default=None, repr=False)

    def get_bone_info(self, index: int) -> Dict:
        """
        Get bone metadata for armature creation.
        Does NOT generate any geometry nodes.
        """
        return {
            "index": index,
            "ik_limits": self.ik,
            "length": getattr(self.geometry, "length", 1.0) if self.geometry else 1.0,
            "radius": getattr(self.geometry, "radius", 1.0) if self.geometry else 1.0,
            "parent_index": index - 1 if index > 0 else None,
            "axis": "Z",
        }
