---
title: JoinGeometry link order, float curve points, and closure pairing are not preserved by auto-export
category: blender-api
severity: high
modules: [geo_node_groups, armor, utilities]
tags: [blender5, join-geometry, float-curve, closure, auto-export, order-dependent]
---

## Context

When decomposing an auto-exported node group (`temp_5.py`) into separate
sub-group modules for the Neck armor piece, three categories of data were
lost or mishandled, each producing different geometry from the original.

## Decision

### 1. JoinGeometry multi-input link order matters for join_splines

The `Join Splines` utility converts curves to points, merges endpoints by
distance, then converts back to a single curve. The order that curves are
linked into the upstream `JoinGeometry` determines which endpoints get
stitched and the resulting curve direction. Wrong order = geometry explosion.

When linking to a JoinGeometry multi-input, match the link creation order
from the reference. The first `links.new()` call places the geometry at the
bottom of the stack; subsequent calls stack on top.

### 2. ShaderNodeFloatCurve points are not captured by auto-export

The auto-exporter creates the node and sets the Factor input but does NOT
emit the curve control points. A freshly created `ShaderNodeFloatCurve`
defaults to a straight line `(0,0)→(1,1)`, which silently produces wrong
offsets.

Always initialize the curve mapping explicitly:

```python
float_curve = nodes.new("ShaderNodeFloatCurve")
float_curve.inputs[0].default_value = 1.0
curve_map = float_curve.mapping.curves[0]
curve_map.points[0].location = (0.0, 0.0)
curve_map.points[1].location = (1.0, 0.0)
curve_map.points.new(0.645, 0.058)
float_curve.mapping.update()
```

### 3. Closure nodes need explicit item setup and pairing

Auto-exported code omits `input_items.new()`, `output_items.new()`, and
`pair_with_output()`. Without these, the closure has no typed sockets and
the ClosureInput isn't associated with its ClosureOutput.

```python
closure_output = nodes.new("NodeClosureOutput")
closure_output.input_items.new("FLOAT", "Value")
closure_output.output_items.new("FLOAT", "Value")
closure_output.define_signature = False

closure_input = nodes.new("NodeClosureInput")
closure_input.pair_with_output(closure_output)
```

### 4. MenuSwitch enum_items order must match interface socket index

Enum item 0 maps to `menu_switch.inputs[1]`, enum item 1 maps to
`inputs[2]`, etc. If the interface declares sockets as Spacing (index 1)
then Resolution (index 2), the enum items must be created in that same
order: `"Spacing"` first, `"Resolution"` second.

## Evidence

- Neck armour `centre_profile.py` / `side_profile.py`: swapping JoinGeometry
  link order fixed a geometry explosion caused by join_splines stitching
  curve endpoints in the wrong direction.
- `neck_rails.py`: float curve defaulted to a straight line `(0,0)→(1,1)`
  instead of the intended bump `(0,0)→(0.645,0.058)→(1,0)`.
- `main.py` closure for bi-rail loft profile blending was missing entirely
  in the auto-exported reference; had to be added manually.
- `space_switch.py`: enum items `["Resolution","Spacing"]` were backwards
  relative to the interface sockets `[Spacing, Resolution]`, causing the
  menu to apply the wrong resolution mode.

## Reuse trigger

- Porting any auto-exported node group — audit for float curves, closures,
  and multi-input link order.
- Any node group that uses `Join Splines` — verify input curve order.
- Any node group with `ShaderNodeFloatCurve` — check that points are set.
- Any node group with `NodeClosureOutput` — check items and pairing.

## Anti-pattern

Do NOT trust that auto-exported `.py` files capture all node state. Float
curve mappings, closure definitions, and enum item ordering are silently
dropped. Always cross-reference against the live Blender node tree.
