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
