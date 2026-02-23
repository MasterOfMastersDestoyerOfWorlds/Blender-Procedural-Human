---
title: DSL system architecture for procedural body generation
category: architecture
severity: medium
modules: [dsl, dsl/primitives, definitons]
tags: [dsl, primitives, generator, executor, definitions, torso, finger]
---

## Context

The DSL system lets users define procedural body parts in Python that
compile to Blender geometry nodes with interactive float-curve editing.

## Decision

### Core execution flow

1. **Definition** (`@dsl_definition` class) composes primitives
2. **Executor** (`dsl/executor.py`) runs the file in a sandboxed namespace
3. **Generator** (`dsl/generator.py`) recursively walks the definition,
   calling `generate(context, index)` on each primitive
4. Each primitive's `generate()` creates Blender geometry nodes
5. **File watcher** (`dsl/watcher.py`) monitors for changes, auto-regenerates

### Primitive contract

Every primitive is a `@dsl_primitive` decorated `@dataclass` with a
`generate(self, context: GenerationContext, index: int) -> Dict` method.

The returned dict typically contains:
- `instance`: the node group instance in the parent tree
- `frame`: NodeFrame containing the nodes
- `closures`: dict of float curve closures for interactive editing

### Available primitives

| Primitive | Purpose | Node group |
|---|---|---|
| `DualRadial` | X/Y profile curves -> cylindrical segment | `create_dual_profile_radial_group()` |
| `QuadRadial` | 4-axis profiles -> joint geometry | `create_quad_profile_radial_group()` |
| `HexRadial` | 6-axis spheroid | `create_hex_profile_spheroid_group()` |
| `DualRadialLoft` | Loft from two curve objects | Loft-based node group |

### Structural operators

| Operator | DSL helper | Dataclass | Purpose |
|---|---|---|---|
| `Extend()` | `@dsl_helper` | `SegmentChain` | Chain segments along axis, link prev.Geometry -> next.Geometry |
| `Join()` | `@dsl_helper` | `JoinedStructure` | Insert joints between segments |
| `AttachRaycast()` | `@dsl_helper` | `AttachedStructure` | Terminal attachments (e.g., nails) |

### GenerationContext

Shared state passed between `generate()` calls:
- `node_group`: the Blender node group being built
- `naming_env`: hierarchical name resolution for curve presets
- `instance_name`, `definition_name`: scope identifiers
- `current_y_offset`: auto-incrementing Y position for node layout
- `normalized_lengths`: segment length ratios

### Output primitive

`Output(items)` declares what to generate and handles dependency ordering
via topological sort on object references.

### Definition examples

**Finger:** `DualRadial` segments -> `Extend()` chain -> `Join()` knuckles
-> `AttachRaycast()` nail. Creates bones with IK limits.

**Torso:** `DualRadialLoft` segments with anatomical proportions (Pelvis,
Waist, LowerChest, UpperChest). Parameterized by height and base_radius.
`MaleTorso = Torso(height=0.53, base_radius=0.15)`.

### Float curve closures and presets

Primitives create `ShaderNodeFloatCurve` wrapped in closure pairs for
interactive profile editing. Curve data is saved to `*_float_curve_presets.py`
files via `@register_preset_class`. The naming environment resolves curve
names hierarchically: instance -> definition -> component.

### Registration and discovery

- `@dsl_primitive` registers in primitive namespace (available in DSL files)
- `@dsl_helper` registers helper functions (available in DSL files)
- `@dsl_definition` registers definitions for the DSL browser panel
- All discovered via `get_dsl_namespace()` which builds the sandboxed
  execution environment

### Adding new primitives

1. Create `@dsl_primitive` `@dataclass` in `dsl/primitives/`
2. Implement `generate(context, index)` that creates Blender nodes
3. Create corresponding node group helper if needed
4. Register in `dsl/primitives/__init__.py`

### Key files

- `dsl/generator.py` -- recursive generation engine
- `dsl/executor.py` -- sandboxed Python execution
- `dsl/primitives/primitives.py` -- GenerationContext, helpers
- `dsl/primitives/__init__.py` -- primitive registry
- `dsl/operators.py` -- Blender operators (Create, Realize & Animate)
- `dsl/panel.py` -- DSL Browser UI panel
- `dsl/watcher.py` -- file change watcher

## Evidence

- `torso.py` line 41: `AnatomicalSegment = DualRadialLoft` used in loop
- `extend.py` lines 51-57: chains geometry via `prev_output -> next.inputs["Geometry"]`
- `generator.py` line 82: `_generate_instance` called per DSL instance
- `dual_radial.py` line 76: creates float curve closures for profile editing

## Reuse trigger

Any task involving DSL primitives, adding new body parts, extending the
DSL for armor, or understanding how definitions compile to geometry nodes.

## Anti-pattern

Do NOT confuse DSL definitions with `@geo_node_group` functions. DSL
definitions create Blender objects with geometry node modifiers via the
generator. `@geo_node_group` functions directly create node groups in
`bpy.data.node_groups`. The two systems are currently independent.
