

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive
from procedural_human.dsl.primitives.primitives import GenerationContext, ProfileType


@dsl_primitive
@dataclass
class QuadRadial:
    """
    Quad-axis radial profile for joints.
    
    Uses 4 profile curves at 0°, 90°, 180°, 270° for joint geometry.
    Maps to: procedural_human/geo_node_groups/quad_radial.py
    """
    profile_type: str = "quad"
    _naming_context: Optional[List[str]] = field(default=None, repr=False)
    
    def get_profile_names(self) -> List[str]:
        """Return the profile curve names this type uses."""
        return [
            ProfileType.QUAD_0.value,
            ProfileType.QUAD_90.value,
            ProfileType.QUAD_180.value,
            ProfileType.QUAD_270.value,
        ]
    
    def generate(self, context: GenerationContext, index: int, suffix: str = "") -> Any:
        """Generate quad radial profile node group."""
        from procedural_human.dsl.primitives.quad_radial.quad_radial_nodes import create_quad_profile_radial_group
        return create_quad_profile_radial_group(suffix=suffix or f"Joint_{index}")