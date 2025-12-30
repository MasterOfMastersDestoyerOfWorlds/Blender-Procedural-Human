"""
Decorators module for automatic registration of Blender classes.

This module provides decorators that automatically set Blender attributes
and handle registration of operators, panels, workspaces, and other classes.

Usage:
    from procedural_human.decorators.operator_decorator import procedural_operator
    from procedural_human.decorators.panel_decorator import procedural_panel
    from procedural_human.decorators.workspace_decorator import procedural_workspace

    @procedural_operator
    class MyOperator(Operator):
        ...

    @procedural_panel
    class MyPanel(Panel):
        ...

    @procedural_workspace
    class MyWorkspace:
        name = "My Custom Workspace"
        
        @staticmethod
        def create_layout(context):
            # Layout creation logic
            pass

Classes decorated with these decorators are automatically discovered and
registered when the addon loads - no manual imports needed.
"""
