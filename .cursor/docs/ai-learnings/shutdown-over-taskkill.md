---
title: Use blender-cli shutdown, not taskkill
category: workflow
severity: high
modules: [tools/commands/lifecycle, .cursor/hooks/pre_tool_guard]
tags: [shutdown, taskkill, process-management, banned-commands]
---

## Context

Agents were using raw `taskkill /PID ... /T /F` to stop Blender, bypassing PID tracking and cleanup.

## Decision

Added `shutdown` CLI command that kills tracked PID and clears the PID file. Added `taskkill` to the banned patterns in `pre_tool_guard.py` so agents are forced through the CLI path.

## Evidence

`uv run blender-cli shutdown` successfully terminates and cleans up. Direct `taskkill` is now blocked by the preToolUse hook.

## Reuse trigger

To stop Blender, always use `uv run blender-cli shutdown`. If no PID is tracked, `shutdown` falls back to sending `bpy.ops.wm.quit_blender()` through the server.

## Anti-pattern

Never use `taskkill`, `kill`, or `Stop-Process` directly. The pre-tool guard will block it.
