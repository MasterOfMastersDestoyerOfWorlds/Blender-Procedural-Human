"""
Profile curve data for finger segments.

Each profile is a bezier curve normalized to 0-1 along the length,
with radius values as multipliers of the base segment radius.
"""

from enum import Enum
from procedural_human.decorators.curve_preset_decorator import (
    Preset,
    register_preset_class,
)


class ProfileType(Enum):
    """Types of profile curves"""

    X_PROFILE = "x_profile"
    Y_PROFILE = "y_profile"


class SegmentType(Enum):
    """Types of finger segments""" 

    PROXIMAL = "proximal"
    MIDDLE = "middle"
    DISTAL = "distal" 
    JOINT = "joint"


@register_preset_class("Proximal_Segment")
class PresetProximalSegmentCurves(Preset):
    """Preset for Proximal Segment Curves"""

    def get_data(self):
        return {
            "Proximal Segment_X": [
                {"x": 0.0, "y": 0.0, "handle_type": "AUTO"},
                {
                    "x": 0.09545455873012543,
                    "y": 0.2562499940395355,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.5045454502105713,
                    "y": 0.23750023543834686,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.8681817650794983,
                    "y": 0.20000000298023224,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.9545454382896423,
                    "y": 0.062499742954969406,
                    "handle_type": "AUTO",
                },
                {"x": 1.0, "y": 0.0, "handle_type": "AUTO"},
            ],
            "Proximal Segment_Y": [
                {"x": 0.0, "y": 0.0, "handle_type": "AUTO"},
                {
                    "x": 0.13636364042758942,
                    "y": 0.23124997317790985,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.5136364698410034,
                    "y": 0.24374990165233612,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.7590909004211426,
                    "y": 0.23125006258487701,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.9272724986076355,
                    "y": 0.17500001192092896,
                    "handle_type": "AUTO",
                },
                {"x": 1.0, "y": 0.0, "handle_type": "AUTO"},
            ],
        }


@register_preset_class("Middle_Segment")
class PresetMiddleSegmentCurves(Preset):
    """Preset for Middle Segment Curves"""

    def get_data(self):
        return {
            "Middle Segment_X": [
                {"x": 0.0, "y": 0.0, "handle_type": "AUTO"},
                {
                    "x": 0.09545455873012543,
                    "y": 0.2562499940395355,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.4954545497894287,
                    "y": 0.3000001609325409,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.8681817650794983,
                    "y": 0.20000000298023224,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.9545454382896423,
                    "y": 0.062499742954969406,
                    "handle_type": "AUTO",
                },
                {"x": 1.0, "y": 0.0, "handle_type": "AUTO"},
            ],
            "Middle Segment_Y": [
                {"x": 0.0, "y": 0.0, "handle_type": "AUTO"},
                {
                    "x": 0.13636364042758942,
                    "y": 0.23124997317790985,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.5136364698410034,
                    "y": 0.24374990165233612,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.9272724986076355,
                    "y": 0.17500001192092896,
                    "handle_type": "AUTO",
                },
                {"x": 1.0, "y": 0.0, "handle_type": "AUTO"},
            ],
        }


@register_preset_class("Distal_Segment")
class PresetDistalSegmentCurves(Preset):
    """Preset for Distal Segment Curves"""

    def get_data(self):
        return {
            "Distal Segment_X": [
                {"x": 0.0, "y": 0.0, "handle_type": "AUTO"},
                {
                    "x": 0.09545455873012543,
                    "y": 0.2562499940395355,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.4954545497894287,
                    "y": 0.3000001609325409,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.9090908169746399,
                    "y": 0.19999997317790985,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.9954544901847839,
                    "y": 0.07499974220991135,
                    "handle_type": "AUTO",
                },
                {"x": 1.0, "y": 0.0, "handle_type": "AUTO"},
            ],
            "Distal Segment_Y": [
                {"x": 0.0, "y": 0.0, "handle_type": "AUTO"},
                {
                    "x": 0.054545432329177856,
                    "y": 0.20000003278255463,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.4409090280532837,
                    "y": 0.2687501609325409,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.8272725343704224,
                    "y": 0.23124991357326508,
                    "handle_type": "AUTO",
                },
                {
                    "x": 0.9636361002922058,
                    "y": 0.11875002831220627,
                    "handle_type": "AUTO",
                },
                {"x": 1.0, "y": 0.0, "handle_type": "AUTO"},
            ],
        }
