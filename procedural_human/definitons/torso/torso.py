"""
Torso DSL definition using HexRadial primitives.
Incorporates anatomical muscle group dimensions.
"""

from typing import List
from procedural_human.dsl.primitives import *
from procedural_human.decorators.dsl_definition_decorator import dsl_definition


@dsl_definition
class Torso:
    """
    Procedural torso definition based on anatomical muscle groups.

    The torso is constructed as a chain of 5 distinct anatomical segments:
    1. Pelvis (Sacral): Hips and Gluteus origins.
    2. Waist (Lumbar L1-L5): Abdominals, Obliques, lower Erector Spinae.
    3. Lower Chest (Thoracic T7-T12): Bottom of Pectoralis, Latissimus Dorsi origin.
    4. Upper Chest (Thoracic T1-T6): Pectoralis Major, Scapula, Trapezius.
    5. Neck Base (Cervical C7): Connection to head/neck.

    Dimensions derived from average morphometric data:
    - Total Height: ~530mm
    - Lumbar Span: ~200mm
    - Thoracic Span: ~300mm
    """

    def __init__(self, height: float = 0.53, base_radius: float = 0.14):
        AnatomicalSegment = DualRadialLoft

        self.segments = []
        self.bones = []
        self.height = height
        raw_ratios = [1.0, 1.8, 1.2, 1.3]
        self.norm_lengths = normalize(raw_ratios)
        radii_multipliers = [1.1, 0.9, 1.15, 1.25]

        for i, ratio in enumerate(self.norm_lengths):
            seg_radius = base_radius * radii_multipliers[i]
            seg = AnatomicalSegment(
                curve_x=f"Torso_Waist_X_{i}",
                curve_y=f"Torso_Waist_Y_{i}",
                height=ratio * height,
                res_u=4,
                res_v=4,
            )
            seg.length = ratio * height
            segment_names = ["Pelvis", "Waist", "LowerChest", "UpperChest"]
            seg._naming_context = ["Segment", segment_names[i]]

            self.segments.append(seg)
            if i == 1:  # Waist/Lumbar
                limits = IKLimits(x=(-30, 45), y=(-20, 20), z=(-15, 15))
            elif i >= 2:  # Thoracic (Ribcage is rigid)
                limits = IKLimits(x=(-5, 10), y=(-5, 5), z=(-5, 5))
            else:  # Pelvis (Fixed base)
                limits = IKLimits(x=(0, 0), y=(0, 0), z=(0, 0))

            bone = Bone(geometry=seg, ik=limits)
            self.bones.append(bone)

        self.output = Output(
            [
                self.segments,
            ]
        )
MaleTorso = Torso(height=0.53, base_radius=0.15)
FemaleTorso = Torso(height=0.48, base_radius=0.14)
