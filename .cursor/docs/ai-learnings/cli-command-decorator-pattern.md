---
title: "@cli_command decorator auto-registers and enforces docs"
category: architecture
severity: medium
modules: [tools/cli_registry]
tags: [decorator, cli, argparse, self-registration, documentation]
---

## Context

New CLI commands required manual wiring into `argparse` subparsers and had no enforced documentation standards.

## Decision

Created `@cli_command` decorator (modeled after `@procedural_operator`) that:
1. Parses function signature for arguments and type hints
2. Parses docstring for summary and `:param:` help text
3. Raises `ValueError` if docstring or any param docs are missing
4. Auto-registers into `_REGISTRY` keyed by `function_name.replace("_", "-")`
5. `blender_cli.py` dynamically imports all `tools/commands/*.py` modules and builds `argparse` from the registry

## Evidence

Adding a new command is: write one function with `@cli_command`, add a docstring with `:param:` entries. No other files need editing.

## Reuse trigger

To add a CLI command: create a function in any `tools/commands/*.py` file, decorate with `@cli_command`, write docstring with summary and `:param:` lines. That's it.

## Anti-pattern

Do not manually add subparsers in `blender_cli.py`. Do not create commands without docstrings (the decorator will raise).
