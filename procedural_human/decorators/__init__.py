"""
Decorators module for automatic registration of Blender classes.

This module provides decorators that automatically set Blender attributes
and handle registration of operators, panels, and other classes.

Usage:
    from procedural_human.decorators.operator_decorator import procedural_operator
    from procedural_human.decorators.panel_decorator import procedural_panel
    
    @procedural_operator
    class MyOperator(Operator):
        ...
    
    @procedural_panel
    class MyPanel(Panel):
        ...

Classes decorated with these decorators are automatically discovered and
registered when the addon loads - no manual imports needed.
"""

from procedural_human.decorators.operator_decorator import (
    procedural_operator,
    register_all_operators,
    unregister_all_operators,
    discover_and_register_all_operators,
    dynamic_enum_operator,
)

from procedural_human.decorators.panel_decorator import (
    procedural_panel,
    register_all_panels,
    unregister_all_panels,
    discover_and_register_all_panels,
)

from procedural_human.decorators.module_discovery import (
    discover_modules,
    import_all_modules,
)

from procedural_human.decorators.dsl_primitive_decorator import (
    dsl_primitive,
    dsl_helper,
    dsl_builtin,
    register_builtin,
    get_dsl_namespace,
    get_dsl_primitive_names,
    get_dsl_helper_names,
    get_all_dsl_names,
    is_dsl_primitive,
    is_dsl_primitive_class,
    get_primitive_class,
)

__all__ = [
    "procedural_operator",
    "register_all_operators",
    "unregister_all_operators",
    "discover_and_register_all_operators",
    "dynamic_enum_operator",
    "procedural_panel",
    "register_all_panels",
    "unregister_all_panels",
    "discover_and_register_all_panels",
    "discover_modules",
    "import_all_modules",
    "dsl_primitive",
    "dsl_helper",
    "dsl_builtin",
    "register_builtin",
    "get_dsl_namespace",
    "get_dsl_primitive_names",
    "get_dsl_helper_names",
    "get_all_dsl_names",
    "is_dsl_primitive",
    "is_dsl_primitive_class",
    "get_primitive_class",
]

