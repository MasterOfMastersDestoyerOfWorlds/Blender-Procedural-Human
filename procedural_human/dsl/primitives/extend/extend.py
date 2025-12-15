from dataclasses import dataclass, field
from typing import Any, Dict, List
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive
from procedural_human.dsl.primitives.primitives import GenerationContext
from procedural_human.decorators.dsl_primitive_decorator import dsl_helper


@dsl_primitive
@dataclass
class SegmentChain:
    """Result of Extend() - a chain of segments along an axis."""

    segments: List[Any]
    axis: str = "Z"
    norm_lengths: List[float] = field(default_factory=list)

    def __iter__(self):
        return iter(self.segments)

    def __len__(self):
        return len(self.segments)

    def __getitem__(self, index):
        return self.segments[index]

    def generate(self, context: GenerationContext) -> Dict:
        """
        Generate chained segment geometry nodes.

        Creates each segment and chains geometry: prev_output -> next_input
        Uses normalized lengths if available.

        Note: Bone metadata is stored separately in the bones list,
        not processed here. This only handles geometry generation.
        """
        results = []
        prev_geometry_output = None

        if self.norm_lengths and len(self.norm_lengths) == len(self.segments):
            context.normalized_lengths = self.norm_lengths

        for idx, segment in enumerate(self.segments):
            if self.norm_lengths and idx < len(self.norm_lengths):
                if hasattr(segment, "length"):
                    segment.length = self.norm_lengths[idx]

            if hasattr(segment, "generate"):
                result = segment.generate(context, idx)
                results.append(result)

                if prev_geometry_output is not None and "instance" in result:
                    context.node_group.links.new(
                        prev_geometry_output, result["instance"].inputs["Geometry"]
                    )

                if "instance" in result:
                    prev_geometry_output = result["instance"].outputs["Geometry"]

        return {
            "segments": results,
            "output": prev_geometry_output,
        }


@dsl_helper
def Extend(
    segments: List[Any], axis: str = "Z", norm_lengths: List[float] = None
) -> SegmentChain:
    """Chain segments along an axis, optionally with normalized lengths."""
    return SegmentChain(segments=segments, axis=axis, norm_lengths=norm_lengths or [])
