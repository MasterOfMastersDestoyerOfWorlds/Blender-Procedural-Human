        
def create_geometry_nodes_modifier(box, context, name: str):
    snake_name = name.replace(" ", "_").lower()
    box.label(text="Finger Operations:")
    box.operator(f"mesh.procedural_{snake_name}", text=f"Create {name}")

    box.operator(f"mesh.procedural_realize_{snake_name}", text=f"Realize Geometry")

    box.separator()
    if hasattr(context.scene, f"procedural_create_animation_{snake_name}"):
        box.prop(
            context.scene,
            f"procedural_create_animation_{snake_name}",
            text="Create Animation",
        )

    box.operator(f"mesh.procedural_add_armature_{snake_name}", text=f"Add Armature")