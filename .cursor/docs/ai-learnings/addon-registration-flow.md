---
title: Addon registration flow and auto-discovery system
category: architecture
severity: medium
modules: [decorators, __init__]
tags: [registration, decorators, discovery, geo-node-group, auto-discovery]
---

## Context

The addon uses a decorator-based auto-discovery system so that adding a
new file with a decorated function/class requires zero manual registration.

## Decision

### Registration sequence (in __init__.py register())

1. `import_all_modules()` -- recursively scans `procedural_human/` for
   `.py` files, imports each one. Importing triggers decorators.
2. Each `@geo_node_group` function registers in `geo_node_group.registry`
   dict at import time (key = function name, value = function).
3. `discover_and_register_all_decorators()` called for each decorator type
   (panels, operators, node groups, shader groups, etc.)
4. `create_registered_node_groups()` scheduled via `bpy.app.timers.register`
   at 0.1s delay. Iterates `geo_node_group.registry` and calls each function.

### Decorator types

| Decorator | Target | Registration |
|---|---|---|
| `@geo_node_group` | Functions creating node groups | `geo_node_group.registry` dict |
| `@shader_node_group` | Functions creating shader groups | Similar registry |
| `@procedural_operator` | Blender operator classes | `bpy.utils.register_class()` |
| `@procedural_panel` | Blender panel classes | `bpy.utils.register_class()` |
| `@dsl_primitive` | DSL primitive dataclasses | DSL namespace |
| `@dsl_definition` | DSL definition classes | DSL browser |
| `@dsl_helper` | DSL helper functions | DSL namespace |

### geo_node_group decorator internals

```python
class geo_node_group:
    registry: Dict[str, Callable] = {}
    def __new__(cls, func):
        cls.registry[func.__name__] = func
        return func  # returns function unchanged
```

Uses `__new__` to intercept decoration. The function is stored in the
class-level registry dict and returned unchanged.

### Adding a new node group

Just create a file anywhere under `procedural_human/` with:
```python
@geo_node_group
def create_my_thing_group():
    ...
```
The system auto-discovers it. No imports needed in `__init__.py`.

To USE it from another node group, import the function normally.

### Module discovery exclusions

`discover_modules()` skips: `__init__.py`, `__pycache__/`, `tmp/`, `.venv/`.

## Evidence

- `__init__.py` line 274: `import_all_modules()` call
- `__init__.py` line 358: `bpy.app.timers.register(create_registered_node_groups, first_interval=0.1)`
- `geo_node_decorator.py`: `__new__` pattern for registry

## Reuse trigger

Adding new node groups, operators, panels, or DSL primitives. Understanding
why a new file is or isn't being picked up by the addon.

## Anti-pattern

Do NOT manually register node groups in `__init__.py`. The decorator system
handles it. Do NOT put files in `tmp/` or `__pycache__/` expecting them to
be discovered -- these directories are excluded.
