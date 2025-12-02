"""
Output primitive for DSL generation control.

Declares what structures should be generated and automatically resolves
dependencies between them using topological sort.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set
from procedural_human.decorators.dsl_primitive_decorator import dsl_primitive


def get_all_object_refs(obj: Any, visited: Set[int] = None) -> List[Any]:
    """
    Recursively collect all object references from an object's attributes.
    
    This inspects dataclass fields, __dict__, and common container types
    to find all objects that this item depends on.
    """
    if visited is None:
        visited = set()
    
    obj_id = id(obj)
    if obj_id in visited:
        return []
    visited.add(obj_id)
    
    refs = []
    
    # Skip primitive types
    if isinstance(obj, (str, int, float, bool, bytes, type(None))):
        return refs
    
    # Handle lists and tuples
    if isinstance(obj, (list, tuple)):
        for item in obj:
            refs.append(item)
            refs.extend(get_all_object_refs(item, visited))
        return refs
    
    # Handle dicts
    if isinstance(obj, dict):
        for value in obj.values():
            refs.append(value)
            refs.extend(get_all_object_refs(value, visited))
        return refs
    
    # Get attributes from __dict__ or dataclass fields
    attrs_to_check = []
    
    if hasattr(obj, '__dataclass_fields__'):
        # Dataclass - check all fields
        attrs_to_check = list(obj.__dataclass_fields__.keys())
    elif hasattr(obj, '__dict__'):
        # Regular object with __dict__
        attrs_to_check = list(obj.__dict__.keys())
    
    for attr_name in attrs_to_check:
        if attr_name.startswith('_'):
            continue
        try:
            attr_value = getattr(obj, attr_name, None)
            if attr_value is not None and not isinstance(attr_value, (str, int, float, bool, bytes)):
                refs.append(attr_value)
                refs.extend(get_all_object_refs(attr_value, visited))
        except Exception:
            pass
    
    return refs


def toposort(items: List[Any], deps: Dict[int, Set[int]]) -> List[Any]:
    """
    Topological sort of items based on dependency graph.
    
    Args:
        items: List of items to sort
        deps: Dict mapping id(item) -> set of id(dependency) for items it depends on
        
    Returns:
        Items sorted so dependencies come before dependents
    """
    # Build id -> item mapping
    id_to_item = {id(item): item for item in items}
    
    # Kahn's algorithm
    # Count incoming edges for each node
    in_degree = {id(item): 0 for item in items}
    for item_id, dep_ids in deps.items():
        in_degree[item_id] = len(dep_ids)
    
    # Start with nodes that have no dependencies
    queue = [id_to_item[item_id] for item_id, degree in in_degree.items() if degree == 0]
    result = []
    
    # Build reverse graph (item -> items that depend on it)
    reverse_deps = {id(item): set() for item in items}
    for item_id, dep_ids in deps.items():
        for dep_id in dep_ids:
            if dep_id in reverse_deps:
                reverse_deps[dep_id].add(item_id)
    
    while queue:
        item = queue.pop(0)
        result.append(item)
        
        # For each item that depends on this one, decrement its in-degree
        for dependent_id in reverse_deps.get(id(item), set()):
            in_degree[dependent_id] -= 1
            if in_degree[dependent_id] == 0:
                queue.append(id_to_item[dependent_id])
    
    # Check for cycles
    if len(result) != len(items):
        # Cycle detected - fall back to original order
        print("[Output] Warning: Cycle detected in dependencies, using original order")
        return items
    
    return result


@dsl_primitive
@dataclass
class Output:
    """
    Declares what structures should be generated and in what order.
    
    The Output primitive:
    - Takes an explicit list of structures to generate
    - Automatically resolves dependencies by inspecting object references
    - Returns items in dependency order (dependencies first)
    
    Usage:
        self.output = Output([
            self.segment_chain,
            self.joints,
            self.attachments,
        ])
    """
    items: List[Any] = field(default_factory=list)
    
    def get_ordered_items(self) -> List[Any]:
        """
        Return items sorted by dependency graph.
        
        Inspects each item's attributes to find references to other items
        in the Output list, then topologically sorts to ensure dependencies
        are generated first.
        
        Also handles containment: if item A references an object that is
        contained within item B (e.g., a segment that's part of a SegmentChain),
        then A depends on B.
        """
        if not self.items:
            return []
        
        if len(self.items) == 1:
            return self.items
        
        # Build set of item ids for quick lookup
        item_ids = {id(item) for item in self.items}
        
        # Build containment map: id(contained_obj) -> id(container_item)
        # This allows detecting when an item references something inside another item
        containment_map: Dict[int, int] = {}
        for item in self.items:
            contained = get_all_object_refs(item)
            for obj in contained:
                obj_id = id(obj)
                # Don't map items to themselves
                if obj_id not in item_ids:
                    containment_map[obj_id] = id(item)
        
        # For each item, find which other Output items it references
        deps: Dict[int, Set[int]] = {id(item): set() for item in self.items}
        
        for item in self.items:
            # Get all object references from this item
            refs = get_all_object_refs(item)
            
            for ref in refs:
                ref_id = id(ref)
                # Direct dependency: this reference is another item in Output
                if ref_id in item_ids and ref_id != id(item):
                    deps[id(item)].add(ref_id)
                # Indirect dependency: this reference is contained within another Output item
                elif ref_id in containment_map:
                    container_id = containment_map[ref_id]
                    if container_id != id(item):
                        deps[id(item)].add(container_id)
        
        # Topological sort
        ordered = toposort(self.items, deps)
        
        return ordered
    
    def __iter__(self):
        """Allow iterating over ordered items."""
        return iter(self.get_ordered_items())
    
    def __len__(self):
        return len(self.items)

