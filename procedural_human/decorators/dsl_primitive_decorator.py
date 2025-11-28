"""
DSL Primitive decorator system for automatic registration.

This decorator automatically registers DSL primitive classes and helper functions
into a registry that can be used to build the namespace for DSL file execution.
"""

from typing import Dict, Callable, Any, Set, List, Type


_dsl_primitive_registry: Dict[str, type] = {}
_dsl_helper_registry: Dict[str, Callable] = {}
_dsl_builtin_registry: Dict[str, Any] = {}


def dsl_primitive(cls: type) -> type:
    """
    Decorator for DSL primitive classes.
    
    Registers the class in the primitive registry so it can be automatically
    included in the DSL execution namespace.
    
    Usage:
        @dsl_primitive
        class DualRadial:
            ...
    """
    _dsl_primitive_registry[cls.__name__] = cls
    return cls


def dsl_helper(func: Callable) -> Callable:
    """
    Decorator for DSL helper functions.
    
    Registers the function in the helper registry so it can be automatically
    included in the DSL execution namespace.
    
    Usage:
        @dsl_helper
        def normalize(lengths):
            ...
    """
    _dsl_helper_registry[func.__name__] = func
    return func


def dsl_builtin(name: str = None):
    """
    Decorator for registering Python builtins to expose in DSL.
    
    Usage:
        @dsl_builtin()
        def my_range(*args):
            return range(*args)
        
        # Or with custom name:
        @dsl_builtin("len")
        def dsl_len(obj):
            return len(obj)
    """
    def decorator(func: Callable) -> Callable:
        reg_name = name if name else func.__name__
        _dsl_builtin_registry[reg_name] = func
        return func
    return decorator


def register_builtin(name: str, value: Any) -> None:
    """Register a builtin value directly (for Python builtins like range, len)."""
    _dsl_builtin_registry[name] = value


def get_dsl_namespace(extra: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get the complete DSL namespace for exec().
    
    Combines all registered primitives, helpers, and builtins.
    
    Args:
        extra: Additional items to include in the namespace
        
    Returns:
        Dict ready to use as globals in exec()
    """
    namespace = {}
    namespace.update(_dsl_primitive_registry)
    namespace.update(_dsl_helper_registry)
    namespace.update(_dsl_builtin_registry)
    if extra:
        namespace.update(extra)
    return namespace


def get_dsl_primitive_names() -> Set[str]:
    """Get set of all registered primitive class names."""
    return set(_dsl_primitive_registry.keys())


def get_dsl_helper_names() -> Set[str]:
    """Get set of all registered helper function names."""
    return set(_dsl_helper_registry.keys())


def get_dsl_builtin_names() -> Set[str]:
    """Get set of all registered builtin names."""
    return set(_dsl_builtin_registry.keys())


def get_all_dsl_names() -> Set[str]:
    """Get set of all registered DSL names (primitives + helpers + builtins)."""
    return get_dsl_primitive_names() | get_dsl_helper_names() | get_dsl_builtin_names()


def is_dsl_primitive(obj: Any) -> bool:
    """Check if an object is an instance of a registered DSL primitive."""
    return type(obj).__name__ in _dsl_primitive_registry


def is_dsl_primitive_class(cls: type) -> bool:
    """Check if a class is a registered DSL primitive."""
    return cls.__name__ in _dsl_primitive_registry


def get_primitive_class(name: str) -> type:
    """Get a primitive class by name."""
    return _dsl_primitive_registry.get(name)


def clear_registries() -> None:
    """Clear all registries (useful for testing/reloading)."""
    _dsl_primitive_registry.clear()
    _dsl_helper_registry.clear()
    _dsl_builtin_registry.clear()


def init_default_builtins() -> None:
    """Initialize default Python builtins for DSL execution."""
    register_builtin('range', range)
    register_builtin('len', len)
    register_builtin('sum', sum)
    register_builtin('min', min)
    register_builtin('max', max)
    register_builtin('abs', abs)
    register_builtin('print', print)
    register_builtin('list', list)
    register_builtin('dict', dict)
    register_builtin('tuple', tuple)
    register_builtin('int', int)
    register_builtin('float', float)
    register_builtin('str', str)
    register_builtin('bool', bool)
    register_builtin('enumerate', enumerate)
    register_builtin('zip', zip)


init_default_builtins()

