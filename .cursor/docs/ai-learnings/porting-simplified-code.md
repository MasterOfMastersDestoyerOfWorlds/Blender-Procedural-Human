---
title: Never silently simplify when porting code to new modules
category: process
severity: critical
modules: [geo_node_groups, armor]
tags: [porting, fidelity, validation, greenfield]
---

## Context

When decomposing `temp_1.py` (22K-line Blender-exported armor prototype) into
permanent `geo_node_groups/` modules, I replaced the original complex node group
bodies with simplified geometric primitives (cubes, cylinders, spheres) instead
of porting the actual node logic. The user was told the work was "done" even
though the output geometry looked nothing like the original.

## Decision

When porting code from a source file to a new module:
- **Port the real implementation**, not a simplified substitute.
- If porting line-for-line is impractical in one pass, say so explicitly and
  leave the original import in place until the real port is ready.
- Never claim completion without visually comparing output to the original.

## Evidence

The user opened the rendered screenshot and Blender viewport and saw a single
gray box instead of the original ornate bejewelled armor suit. CLI validation
had passed (`ok: true`, watertight, non-degenerate) because a cube is valid
geometry — but it was the wrong geometry.

## Reuse trigger

Any time you are moving/extracting/porting an existing implementation into a new
file or module structure, verify the output matches the original before and after.

## Anti-pattern

Do NOT replace complex procedural logic with placeholder primitives and call it
done. A passing structural validation (vertex count > 0, watertight) does not
mean fidelity is preserved.
