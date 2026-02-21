---
title: Every server-side check must be its own CLI command
category: architecture
severity: high
modules: [tools/commands]
tags: [cli, composability, preflight, validation]
---

## Context

`preflight` and `validate` originally called `client.command()` inline for watertight, camera visibility, and degenerate checks. Those checks were unreachable as standalone CLI commands.

## Decision

Every server-side check exposed through `blender_server.py` must also be a standalone `@cli_command`. Higher-level commands (`preflight`, `validate`) import and call these command functions instead of making raw `client.command()` calls.

Atomic commands: `validate-geometry`, `check-watertight`, `check-degenerate`, `check-camera-visibility`, `screenshot`, `mesh-metrics`, `apply-node-group`, `reload`, `exec`.

Composite commands: `preflight` (chains the atomic checks), `validate` (reload + apply + preflight).

## Evidence

After refactoring, agents can run `uv run blender-cli check-watertight` independently, or let `validate` compose it automatically. Maximum user freedom with zero duplication.

## Reuse trigger

When adding a new Blender-side handler, always create a matching standalone `@cli_command` first, then optionally wire it into `preflight` or `validate`.

## Anti-pattern

Do not inline `client.command("some_check", ...)` inside a composite command if `some_check` should be independently useful. Extract it as its own `@cli_command` first.
