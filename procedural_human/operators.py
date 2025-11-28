"""
Operator classes for Procedural Human Generator

Operators are automatically discovered from the entire procedural_human directory.
Simply decorate your operator class with @procedural_operator and it will be registered.
"""

from procedural_human.decorators.operator_decorator import (
    discover_and_register_all_operators,
    unregister_all_operators,
)


def register():
    """Discover and register all operators using the decorator system"""
    discover_and_register_all_operators()


def unregister():
    """Unregister all operators using the decorator system"""
    unregister_all_operators()
