"""
Naming environment builder for DSL procedural generation.
"""

from typing import Dict, List, Optional, Any

from procedural_human.utils.tree_sitter_utils import (
    extract_class_definitions,
    extract_instance_assignments,
    DSL_PRIMITIVE_TYPES,
)
from procedural_human.logger import *


class NamingEnvironment:
    """Manages hierarchical naming for DSL components."""

    def __init__(self):
        self.definitions: Dict[str, Dict] = {}
        self.instances: Dict[str, Dict] = {}
        self._current_scope: List[str] = []

    def load_from_file(self, file_path: str) -> None:
        """Load naming environment from a DSL file."""
        class_defs = extract_class_definitions(file_path)
        instance_assigns = extract_instance_assignments(file_path)

        for class_def in class_defs:
            self.definitions[class_def["name"]] = {
                "type": "class",
                "components": class_def["components"],
                "init_params": class_def["init_params"],
            }

        for instance in instance_assigns:
            self.instances[instance["name"]] = {
                "definition": instance["definition"],
                "args": instance["args"],
            }

    def push_scope(self, name: str) -> None:
        """Push a name onto the current scope stack."""
        self._current_scope.append(name)

    def pop_scope(self) -> Optional[str]:
        """Pop and return the last name from the scope stack."""
        if self._current_scope:
            return self._current_scope.pop()
        return None

    def get_scope(self) -> List[str]:
        """Get the current scope stack (copy)."""
        return list(self._current_scope)

    def clear_scope(self) -> None:
        """Clear the current scope stack."""
        self._current_scope.clear()

    def build_profile_name(
        self, component: str, index: Optional[int] = None, axis: str = "X"
    ) -> str:
        """Build a full profile name from current scope."""
        parts = list(self._current_scope) + [component]
        if index is not None:
            parts.append(str(index))
        parts.append(axis)
        return "_".join(parts)

    def build_profile_name_chain(
        self, component: str, index: Optional[int] = None, axis: str = "X"
    ) -> List[str]:
        """Build a chain of profile names for fallback resolution."""
        names = []
        scope = list(self._current_scope)

        for i in range(len(scope) + 1):
            prefix_parts = scope[i:]
            full_parts = prefix_parts + [component]
            if index is not None:
                full_parts.append(str(index))
            full_parts.append(axis)
            names.append("_".join(full_parts))

        return names

    def get_component_profiles(
        self, definition_name: str, component_name: str
    ) -> List[str]:
        """Get the profile axes for a component in a definition."""
        if definition_name not in self.definitions:
            return []

        components = self.definitions[definition_name].get("components", {})
        if component_name not in components:
            return []

        component = components[component_name]
        component_type = component.get("type", "")

        if component_type in DSL_PRIMITIVE_TYPES:
            return DSL_PRIMITIVE_TYPES[component_type]["profiles"]

        return component.get("profiles", [])

    def is_component_indexed(self, definition_name: str, component_name: str) -> bool:
        """Check if a component is indexed (created in a loop)."""
        if definition_name not in self.definitions:
            return False

        components = self.definitions[definition_name].get("components", {})
        if component_name not in components:
            return False

        return components[component_name].get("indexed", False)

    def to_dict(self) -> Dict:
        """Export naming environment as a dictionary."""
        return {
            "definitions": self.definitions,
            "instances": self.instances,
        }


def build_naming_environment(file_path: str) -> NamingEnvironment:
    """Build a naming environment from a DSL file."""
    env = NamingEnvironment()
    env.load_from_file(file_path)
    return env


class NamingContext:
    """Context manager for tracking naming scope during DSL execution."""

    def __init__(self, naming_env: NamingEnvironment):
        self.naming_env = naming_env

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.naming_env.clear_scope()
        return False

    def enter_instance(self, instance_name: str) -> "NamingContext":
        """Enter an instance scope."""
        self.naming_env.push_scope(instance_name)
        definition = self.naming_env.instances.get(instance_name, {}).get("definition")
        if definition:
            self.naming_env.push_scope(definition)
        return self

    def get_profile_chain(
        self, component: str, index: Optional[int] = None, axis: str = "X"
    ) -> List[str]:
        """Get profile name chain for current context."""
        return self.naming_env.build_profile_name_chain(component, index, axis)
