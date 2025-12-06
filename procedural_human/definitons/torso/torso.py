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
        # Use HexRadial for 6-axis sculpting (Front/Back/Sides/Top/Bottom)
        AnatomicalSegment = DualRadialLoft

        self.segments = []
        self.bones = []
        self.height = height

        # Anatomical Segment Ratios (based on vertebral span heights)
        # Total units = 5.3 (approx 100mm per unit relative to 530mm height)
        # Pelvis: 1.0 (Sacrum)
        # Waist: 1.8 (Lumbar L1-L5)
        # Ribcage_Lower: 1.2 (T7-T12)
        # Ribcage_Upper: 1.3 (T1-T6)
        raw_ratios = [1.0, 1.8, 1.2, 1.3] 
        self.norm_lengths = normalize(raw_ratios)
        
        # Base radii for each segment (approximation of skeletal width + muscle thickness)
        # Pelvis: Wide (Iliac Crest)
        # Waist: Narrower (No ribs, Obliques ~9mm thickness)
        # Chest Lower: Widening (Lats start T7)
        # Chest Upper: Widest (Shoulders, Pectoralis ~30mm thickness)
        radii_multipliers = [1.1, 0.9, 1.15, 1.25]

        for i, ratio in enumerate(self.norm_lengths):
            seg_radius = base_radius * radii_multipliers[i]
            
            # Create the anatomical segment
            seg = AnatomicalSegment(
                curve_x=f"Torso_Waist_X_{i}",
                curve_y=f"Torso_Waist_Y_{i}",
                height=ratio * height,
                res_u=4,
                res_v=4,
            )
            
            # Manually assign length for the rig
            seg.length = ratio * height
            
            # Unique naming context for looking up specific muscle curves
            # e.g., "Torso_Waist_X+" controls Rectus Abdominis projection
            segment_names = ["Pelvis", "Waist", "LowerChest", "UpperChest"]
            seg._naming_context = ["Segment", segment_names[i]]

            self.segments.append(seg)

            # Create Bone Metadata
            # Waist (Lumbar) allows more flexion than Chest (Thoracic)
            if i == 1: # Waist/Lumbar
                limits = IKLimits(x=(-30, 45), y=(-20, 20), z=(-15, 15))
            elif i >= 2: # Thoracic (Ribcage is rigid)
                limits = IKLimits(x=(-5, 10), y=(-5, 5), z=(-5, 5))
            else: # Pelvis (Fixed base)
                limits = IKLimits(x=(0, 0), y=(0, 0), z=(0, 0))

            bone = Bone(geometry=seg, ik=limits)
            self.bones.append(bone)

        # Chain segments Z-upwards
    

        self.output = Output([
            self.segments,
        ])


# --- Default Instances ---

# Standard Male Reference (Height ~180cm, Torso ~53cm)
MaleTorso = Torso(height=0.53, base_radius=0.15)

# Standard Female Reference (Height ~165cm, Torso ~48cm)
# Slightly shorter, typically wider pelvis ratio relative to waist
FemaleTorso = Torso(height=0.48, base_radius=0.14)