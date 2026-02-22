---
title: NodeSocketMenu enum items must be defined on the interface socket
category: blender-api
severity: high
modules: [geo_node_groups, utilities]
tags: [blender5, menu-switch, enum, sockets]
---

## Context

When a geometry node group exposes a `NodeSocketMenu` input on its public
interface, the menu appears as "Menu Undefined" in the Blender UI unless
the enum items are explicitly copied to the interface socket.

## Decision

After creating a `GeometryNodeMenuSwitch` and defining its enum items
internally, copy the enum definition to the public interface socket:

```python
menu_socket = group.interface.items_tree["My Menu Input"]
menu_switch = group.nodes.new("GeometryNodeMenuSwitch")
# ... add enum_items on menu_switch ...
menu_socket.from_socket(menu_switch, menu_switch.inputs[0])
menu_socket.default_value = "DesiredDefault"
```

Setting `active_index` on the internal `GeometryNodeMenuSwitch` does NOT
propagate to the group's external interface.

## Evidence

- `space_switch.py`: Setting `menu_switch.active_index = 1` made the
  internal node correct but left the interface socket showing
  "Menu Undefined". Fixed by `menu_socket.from_socket(...)`.
- `bi_rail_loft.py`: Same pattern, same fix.

## Reuse trigger

Any geometry node group that exposes a `NodeSocketMenu` to users needs
`from_socket()` on the interface socket after defining the internal
`GeometryNodeMenuSwitch` items.

## Anti-pattern

Do NOT set `menu_switch.active_item = "SomeName"` with a string —
it expects a `NodeEnumItem`. Do NOT assume defining items on the
internal node automatically populates the group-level interface socket.
