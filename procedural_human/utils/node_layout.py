"""
Automatic node layout using topological sort.

Positions nodes in a geometry node group based on their dependencies,
with input nodes on the left and output nodes on the right.
"""

from typing import Dict, List, Set, Any, Tuple
from collections import defaultdict


def auto_layout_nodes(
    node_group: Any,
    x_spacing: int = 250,
    y_spacing: int = 150,
    start_x: int = -1400,
    start_y: int = 0,
) -> None:
    """
    Automatically position nodes using topological sort.

    Nodes are arranged left-to-right based on dependency depth:
    - Input nodes at the leftmost position
    - Output nodes at the rightmost position
    - Intermediate nodes positioned by their depth in the dependency graph

    Args:
        node_group: Blender node group to layout
        x_spacing: Horizontal spacing between depth levels
        y_spacing: Vertical spacing between nodes at same depth
        start_x: Starting X position for leftmost nodes
        start_y: Center Y position
    """
    nodes = list(node_group.nodes)
    links = list(node_group.links)

    if not nodes:
        return
    depends_on: Dict[str, Set[str]] = defaultdict(set)
    feeds_into: Dict[str, Set[str]] = defaultdict(set)

    for link in links:
        from_node = link.from_node.name
        to_node = link.to_node.name
        depends_on[to_node].add(from_node)
        feeds_into[from_node].add(to_node)
    node_depth: Dict[str, int] = {}
    sources = [n.name for n in nodes if not depends_on[n.name]]
    if not sources:
        sources = [n.name for n in nodes if n.bl_idname == "NodeGroupInput"]
    queue = [(name, 0) for name in sources]
    visited = set()

    while queue:
        node_name, depth = queue.pop(0)

        if node_name in visited:
            node_depth[node_name] = max(node_depth.get(node_name, 0), depth)
            continue

        visited.add(node_name)
        node_depth[node_name] = depth
        for next_node in feeds_into[node_name]:
            queue.append((next_node, depth + 1))
    for node in nodes:
        if node.name not in node_depth:
            node_depth[node.name] = 0
    max_depth = max(node_depth.values()) if node_depth else 0
    for node in nodes:
        if node.bl_idname == "NodeGroupOutput":
            node_depth[node.name] = max_depth + 1
    max_depth = max(node_depth.values()) if node_depth else 0
    nodes_at_depth: Dict[int, List[Any]] = defaultdict(list)
    for node in nodes:
        depth = node_depth[node.name]
        nodes_at_depth[depth].append(node)
    for depth, depth_nodes in nodes_at_depth.items():

        def get_avg_connected_y(node):
            y_positions = []
            for dep_name in depends_on[node.name]:
                dep_node = node_group.nodes.get(dep_name)
                if dep_node and dep_node.name in node_depth:
                    y_positions.append(dep_node.location[1])
            return sum(y_positions) / len(y_positions) if y_positions else 0

        depth_nodes.sort(key=get_avg_connected_y, reverse=True)
    for depth in range(max_depth + 1):
        depth_nodes = nodes_at_depth[depth]
        num_nodes = len(depth_nodes)

        x = start_x + (depth * x_spacing)
        total_height = (num_nodes - 1) * y_spacing
        top_y = start_y + (total_height / 2)

        for i, node in enumerate(depth_nodes):
            y = top_y - (i * y_spacing)
            node.location = (x, y)


def get_node_depth_info(node_group: Any) -> Dict[str, int]:
    """
    Get depth information for all nodes in a group.

    Useful for debugging layout issues.

    Args:
        node_group: Blender node group to analyze

    Returns:
        Dictionary mapping node names to their depth values
    """
    nodes = list(node_group.nodes)
    links = list(node_group.links)

    depends_on: Dict[str, Set[str]] = defaultdict(set)
    feeds_into: Dict[str, Set[str]] = defaultdict(set)

    for link in links:
        from_node = link.from_node.name
        to_node = link.to_node.name
        depends_on[to_node].add(from_node)
        feeds_into[from_node].add(to_node)

    node_depth: Dict[str, int] = {}
    sources = [n.name for n in nodes if not depends_on[n.name]]

    if not sources:
        sources = [n.name for n in nodes if n.bl_idname == "NodeGroupInput"]

    queue = [(name, 0) for name in sources]
    visited = set()

    while queue:
        node_name, depth = queue.pop(0)
        if node_name in visited:
            node_depth[node_name] = max(node_depth.get(node_name, 0), depth)
            continue
        visited.add(node_name)
        node_depth[node_name] = depth
        for next_node in feeds_into[node_name]:
            queue.append((next_node, depth + 1))

    for node in nodes:
        if node.name not in node_depth:
            node_depth[node.name] = 0

    return node_depth
