---
title: Armor system architecture and how pieces are composed
category: architecture
severity: medium
modules: [geo_node_groups/armor, utilities]
tags: [armor, bi-rail-loft, composition, positioning, mirror]
---

## Context

The armor system creates ornate medieval armor pieces procedurally using
geometry nodes. Each piece is a standalone node group with hardcoded
absolute world coordinates.

## Decision

### Piece inventory and file sizes

| Piece | File | Lines | Decomposed? |
|---|---|---|---|
| Neck | `armor/neck/` (32 files) | ~85 (main.py) | Yes -- sub-groups |
| Chest | `armor/chest.py` | ~987 | No -- monolithic |
| Shoulders | `armor/shoulders.py` | ~1512 | No -- monolithic |
| Waist | `armor/waist.py` | ~912 | No -- monolithic |
| Sleeves | `armor/sleeves.py` | ~313 | No -- monolithic |
| Blocker | `armor/blocker.py` | ~828 | No -- monolithic |
| Suit | `armor/armor_suit.py` | ~139 | Composition only |

### The bi-rail loft pattern

Every armor piece uses the same core algorithm:

1. Two **rail curves** (circles with transforms) define the surface path
2. **Profile curves** (quadratic beziers) define cross-sections
3. **Bi-Rail Loft** utility interpolates profiles along rails to create a mesh
4. Optional **closure** provides a blending curve for profile interpolation
5. **Trim** step adds pipes, rivets, and clips to X >= 0 half-space

Rail parameters: circle resolution, radius, translation, rotation, scale,
optional float curve for Z-offset along the rail.

### Positioning: hardcoded absolute coordinates

Pieces do NOT reference body geometry, armatures, or landmarks. Every
position is a hardcoded `Vector` constant. The `armor_suit.py` Geometry
input socket exists but is **never wired to anything**.

Coordinate conventions:
- Y negative = forward, Z positive = up, X negative = left
- Only the left half (X < 0) is modeled
- `mirror.py` scales by `(-1, 1, 1)` around world origin for the right half

### armor_suit.py composition

Flat join of all pieces -> RealizeInstances -> Mirror X -> material chain.
Materials assigned by named boolean attributes: `gold`, `ruby`, `saphire`,
`fabric`, `blocker`, `rope`, `skip` (mirror skip).

### Blocker role

`blocker.py` creates icospheres at hardcoded positions, converts to SDF
grids for boolean collision geometry. Tagged with `"blocker"` attribute.
NOT a body proxy -- purely self-intersection prevention.

### Shared utilities used across pieces

Multi-piece: bi_rail_loft, pipes, rivet, gem_in_holder, gold_on_band,
join_splines, swap_attr.
Neck-only: space_switch, gold_wavies, gold_decorations, rotate_on_centre,
mirror, is_edge_boundary.

## Evidence

- `armor_suit.py` lines 46-49: neck instantiated with no body input
- `neck_rails.py` lines 34-36: rail translation/rotation are literal Vectors
- `armor_suit.py` line 23: Geometry INPUT socket defined but never linked
- `mirror.py` line 33: scale `(-1, 1, 1)` confirms X-axis mirror at origin

## Reuse trigger

Any task involving armor pieces, adding new armor, or understanding how
pieces are positioned. Also relevant when connecting armor to body geometry.

## Anti-pattern

Do NOT assume armor pieces reference body geometry or use raycast/proximity.
They are entirely freestanding with hardcoded coordinates. A design doc
(`procedural_armor_plan.md`) describes body-conforming but it was never
implemented.
