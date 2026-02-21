---
title: CLI over MCP for Blender validation
category: architecture
severity: high
modules: [tools, procedural_human/testing]
tags: [cli, mcp, validation, blender-server, hot-reload]
---

## Context

Blender validation was done via MCP server (`mcp_server_standalone.py`). Rebuilding the MCP required restarting Cursor entirely.

## Decision

Replace MCP with a CLI (`tools/blender_cli.py`) that talks to the same Blender HTTP server on port 9876. The Blender-side server stays unchanged.

## Evidence

CLI can be edited and re-invoked instantly via Shell tool. MCP requires full Cursor restart on any change. Both use the same HTTP `/command` endpoint.

## Reuse trigger

Any time a new validation check or Blender command is needed, add a `@cli_command` decorated function in `tools/commands/`. Do not add MCP tools.

## Anti-pattern

The MCP layer (`mcp_server_standalone.py`, `mcp_server.py`, `mcps/`) has been deleted. All validation is CLI-only now.
