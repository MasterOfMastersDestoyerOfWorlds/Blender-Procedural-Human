---
title: Neck armor decomposition pattern and sub-group inventory
category: architecture
severity: medium
modules: [geo_node_groups/armor/neck]
tags: [armor, neck, decomposition, sub-groups, bi-rail-loft]
---

## Context

The neck piece is the only armor piece decomposed into sub-group files.
Understanding its structure is essential for decomposing other pieces.

## Decision

### main.py composition flow

```
centre_profile + side_profile -> JoinGeometry -> bi_rail_loft.profiles
neck_rails.Rail_A -> bi_rail_loft.Rail_A
neck_rails.Rail_B -> bi_rail_loft.Rail_B
Closure(PingPong 0.25 * 4.0) -> bi_rail_loft.blending
bi_rail_loft.Mesh + bi_rail_loft.UVMap -> neck_trim -> output
```

### Sub-group files used by main.py

| File | Group name | Inputs | Outputs |
|---|---|---|---|
| `centre_profile.py` | `Neck_centre_profile` | none | Geometry |
| `side_profile.py` | `Neck_side_profile` | none | Geometry |
| `neck_rails.py` | `Neck_neck_rails` | none | Rail Curve A, Rail Curve B |
| `neck_trim.py` | `NeckTrim` | Geometry, Vector | Selection, Mesh |

### Bi-rail loft configuration (hardcoded in main.py)

- Smoothing: 0
- Menu: "Resolution"
- X Spacing: 0.01, Y Spacing: 0.03
- X Resolution: 42, Y Resolution: 148
- Profile Blending Curve: PingPong(0.25) * 4.0 closure

### Rail parameters (in neck_rails.py)

Rail A (lower, larger):
- Circle radius=0.13, resolution=73
- Rotate Z=pi/2, then translate=(0,0,0.37), rotate X=0.156, scale=(1.26,1,1)
- Float curve offset: points at (0,0), (0.645,0.058), (1,0)

Rail B (upper, smaller):
- Circle radius=0.08, resolution=73
- Rotate Z=pi/2, then translate=(0,-0.02,0.48), rotate X=0.407

### Unused files in neck/ directory

28 of 32 files are NOT used by main.py. These include alternative frame
designs (frame_005, frame_011, frame_013, frame_017), decoration variants
(broaches, collar_gems, larger_jewels, satalite_gems, pendant), link/chain
elements (necklace_link, loop), and alignment helpers (align). They appear
to be a library of optional components from the original prototype.

### Naming inconsistency

Group names mix conventions: `Neck_centre_profile` (underscore) vs
`NeckTrim` (PascalCase). Function names have a double-neck:
`create_neck_neck_rails_group()`.

## Evidence

- `main.py` lines 72-74: rail and profile wiring to bi_rail_loft
- `main.py` lines 49-70: closure setup with PingPong + Multiply
- `neck_rails.py` lines 34-43: hardcoded rail transforms
- 28 files in neck/ not imported by main.py

## Reuse trigger

Decomposing other monolithic armor pieces (chest, shoulders, waist) into
the same sub-group pattern. Also relevant when extending the DSL to
replace the manual node group approach.

## Anti-pattern

Do NOT assume all files in `neck/` are used. Most are unused variants from
the original prototype. Only 4 sub-groups are wired into `main.py`.
