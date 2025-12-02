from dataclasses import dataclass
from typing import Tuple, Dict
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive
import math


@dsl_primitive
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
        return {
            "x": (math.radians(self.x[0]), math.radians(self.x[1])),
            "y": (math.radians(self.y[0]), math.radians(self.y[1])),
            "z": (math.radians(self.z[0]), math.radians(self.z[1])),
        }