---
title: validate is the uber command, preflight is checks-only
category: workflow
severity: high
modules: [tools/commands/validation]
tags: [validate, preflight, reload, clean-scene]
---

## Context

Validation requires a clean scene (no stale objects or default cube), a fresh addon reload, node group application, geometry checks, and a screenshot. Agents were forgetting intermediate steps.

## Decision

`validate` is the single uber command that does reload + apply + preflight + screenshot. `preflight` exists separately for when the agent already has a scene set up and only wants checks.

## Evidence

Baking reload into `validate` eliminates state carryover bugs. The default cube was being mistaken for target geometry in early runs.

## Reuse trigger

After editing any geo node code, agents should run `uv run blender-cli validate --group <Name>`. Use `preflight` only when iterating on an existing scene without code changes.

## Anti-pattern

Do not run `reload` then `apply-node-group` then `preflight` as three separate calls. Use `validate` instead. The separate commands exist for debugging, not for the standard loop.
