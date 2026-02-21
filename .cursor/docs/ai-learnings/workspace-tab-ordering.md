---
title: Workspace duplicate displaces Layout tab
category: bug-fix
severity: medium
modules: [procedural_human/decorators/workspace_decorator]
tags: [workspace, blender-ui, tab-order, layout]
---

## Context

`bpy.ops.workspace.duplicate()` inserts the new workspace tab adjacent to the base. When Layout is the base (or first fallback), the custom workspace displaces Layout from position 0.

## Decision

After creating and naming the new workspace, call `_move_workspace_to_back()` which switches to the new workspace, runs `bpy.ops.workspace.reorder_to_back()`, then switches back to the original.

## Evidence

Before fix: Curve Segmentation at tab 0, Layout.001 at tab 1. After fix: Layout stays at tab 0.

## Reuse trigger

Any new `@procedural_workspace` class will automatically get reordered to the back. No manual intervention needed.

## Anti-pattern

Do not assume `workspace.duplicate()` preserves tab ordering. Always reorder after creation.
