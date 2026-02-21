---
title: Blender executable discovery fallback chain
category: configuration
severity: medium
modules: [tools/commands/lifecycle]
tags: [blender-path, config, vscode-settings, discovery]
---

## Context

Agents and users kept having to pass `--blender C:\path\to\blender.exe` on every CLI call.

## Decision

Five-tier fallback chain in `_resolve_blender_executable()`:
1. `--blender` CLI arg
2. `BLENDER_EXE` env var
3. `tools/blender_config.json` (`blender_executable` key)
4. `.vscode/settings.json` (`blender.executables`, prefers `isDefault: true`)
5. `shutil.which("blender")` (PATH lookup)

## Evidence

With `BLENDER_EXE` set or `blender_config.json` populated, `uv run blender-cli start` works with zero arguments from repo root.

## Reuse trigger

If Blender start fails with "No Blender executable configured", check these five sources in order.

## Anti-pattern

Do not hardcode Blender paths in CLI source code or command files.
