import bpy


def run_create_finger():
    """Reset Blender scene and run the Procedural Finger operator."""
    
    bpy.ops.wm.read_factory_settings(use_empty=True)

    
    try:
        bpy.ops.preferences.addon_enable(module="procedural_human")
    except Exception:
        pass

    
    bpy.ops.mesh.procedural_finger(
        finger_type="INDEX",
        radius=0.007,
        nail_size=0.003,
        taper_factor=0.15,
    )


if __name__ == "__main__":
    run_create_finger()


