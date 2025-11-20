from bpy.types import UILayout, Context


def create_geometry_nodes_modifier(box: UILayout, context: Context, name: str) -> None:
    snake_name = name.replace(" ", "_").lower()
    box.label(text=f"{name} Operations:")
    box.operator(f"mesh.procedural_{snake_name}", text=f"Create {name}")
    box.operator(f"mesh.procedural_realize_{snake_name}", text=f"Realize Geometry")
    box.separator()
    box.operator(f"mesh.procedural_add_armature_{snake_name}", text=f"Add Armature")
    box.operator(
        f"mesh.procedural_create_animation_{snake_name}",
        text="Create Animation",
    )