---
title: Map Blender addon paths to workspace paths in error logs
category: tooling
severity: medium
modules: [logger]
tags: [logging, debugging, blender-addon]
---

## Context

Blender loads addons from `AppData\Roaming\Blender Foundation\...`, so
Python tracebacks point there instead of the workspace source. Clicking
such paths in Cursor opens the wrong copy of the file.

## Decision

Use a custom `logging.Formatter` that rewrites exception frame paths
to the workspace root by finding the `\procedural_human\` marker in the
path and prepending the workspace root. Only rewrite on ERROR+ with
`exc_info`, and emit the *exception origin* frame (last in traceback),
not the `logger.error()` call site.

## Evidence

Implemented in `procedural_human/logger.py` as `CursorErrorFormatter`.
Error logs now emit clickable `C:\Code\...\procedural_human\file.py:42`
paths that open directly in Cursor.

## Reuse trigger

Any Blender addon that runs from a symlinked/copied location and wants
IDE-clickable error paths.

## Anti-pattern

Do NOT log the call site of `logger.error()` — that's usually a generic
error handler. Log the last frame of `exc_info[2]` to point at the
actual failure.
