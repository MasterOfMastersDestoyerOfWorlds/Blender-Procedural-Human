"""
DSL primitive classes for procedural generation.

These classes map to geometry node groups in the codebase:
- DualRadial -> dual_radial.py (X, Y profile curves)
- QuadRadial -> quad_radial.py (0°, 90°, 180°, 270° curves)
- Joint -> joint_segment_nodes.py (uses QuadRadial)
- RadialAttachment -> finger_nail_nodes.py (terminal attachments)
- IKLimits -> finger_utils.py IK constraint setup

Each primitive has a generate() method that creates its own geometry nodes.
All primitives are registered via @dsl_primitive decorator for automatic namespace building.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Any, Dict
from enum import Enum

from procedural_human.decorators.dsl_primitive_decorator import (
    dsl_primitive,
    dsl_helper,
)


class ProfileType(Enum):
    """Types of profile curves based on radial type."""

    DUAL_X = "X"
    DUAL_Y = "Y"
    QUAD_0 = "0"
    QUAD_90 = "90"
    QUAD_180 = "180"
    QUAD_270 = "270"


@dataclass
class GenerationContext:
    """Context passed between generate() calls to share state."""

    node_group: Any
    naming_env: Any
    instance_name: str
    definition_name: str
    segment_results: Dict[int, Dict] = field(default_factory=dict)
    current_y_offset: float = 0
    node_spacing: float = 300
    current_attr_name: str = ""
    normalized_lengths: List[float] = field(default_factory=list)

    def get_next_y_offset(self) -> float:
        """Get next Y position and decrement for next call."""
        y = self.current_y_offset
        self.current_y_offset -= self.node_spacing
        return y

@dsl_helper
def normalize(lengths: List[float]) -> List[float]:
    """Normalize a list of lengths to ratios that sum to 1.0."""
    if not lengths:
        return []
    total = sum(lengths)
    if total == 0:
        return [1.0 / len(lengths)] * len(lengths)
    return [length / total for length in lengths]


@dsl_helper
def last(items: List[Any]) -> Any:
    """Get the last item from a list."""
    if not items:
        raise IndexError("Cannot get last item from empty list")
    return items[-1]
