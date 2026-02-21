---
name: blender-validation
description: Validate Blender addon code using the CLI-based clean validation loop.
---

# Blender CLI Validation Skill

Use this workflow whenever modifying `procedural_human` geometry node groups, operators, or workspace layout logic.

## Primary Validation Flow

Run commands from the repository root (`C:\Code\Blender-Procedural-Human`).  
When running from repo root, you do not need `--project`; use `uv run blender-cli ...`.

1. Ensure Blender server is up:
   - `uv run blender-cli start`
2. Run full validation:
   - `uv run blender-cli validate --group <GroupName>`
3. Inspect JSON output:
   - geometry counts
   - watertight result
   - degenerate check result
   - camera visibility result
4. Review the rendered screenshot path and compare against expected output.

## Command Reference

- `validate` (primary): clean reload + apply group + preflight checks + screenshot
- `preflight`: checks only on existing scene/object state
- `reload`: reload addon (`--keep-scene` optional)
- `shutdown`: stop Blender from CLI (preferred over direct OS taskkill)
- `restart`: kill/restart Blender tracked process
- `exec`: run arbitrary `bpy` Python code inside Blender

## Required Checks

- Mesh has at least 2 vertices and at least 1 face
- Mesh is watertight by default (unless intentionally disabled)
- Mesh is not collapsed to a line or point
- Mesh is visible to active camera

## Failure Handling

- If `validate` fails, fix code and rerun `validate`
- If connection fails, run `uv run blender-cli restart`
- If check output seems wrong, use `exec` for targeted inspection
