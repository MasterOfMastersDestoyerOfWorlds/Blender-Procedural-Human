---
title: setuptools flat-layout discovers too many top-level packages
category: counter-intuitive
severity: medium
modules: [pyproject.toml]
tags: [uv, setuptools, packaging, pyproject]
---

## Context

Running `uv run blender-cli` failed with `Multiple top-level packages discovered in a flat-layout: ['mcps', 'procedural_human']`. The repo has several top-level directories with `__init__.py` or importable structure.

## Decision

Add explicit package discovery in `pyproject.toml`:

```toml
[tool.setuptools.packages.find]
include = ["tools*"]
```

This tells setuptools to only package the `tools` directory. Other top-level directories (`procedural_human`, `mcps`) are Blender addon / MCP infrastructure and are not part of the CLI distribution.

## Evidence

After adding the include filter, `uv run blender-cli --help` works from repo root without `--project`.

## Reuse trigger

If adding new top-level directories causes `uv run` to break, check the `include` list in `pyproject.toml`.

## Anti-pattern

Do not remove `__init__.py` from other packages to work around this. Fix the `setuptools` discovery scope instead.
