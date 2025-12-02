"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes
"""

import bpy
import subprocess
import sys
from pathlib import Path
from procedural_human.dsl.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.logger import *

from procedural_human.decorators.curve_preset_decorator import register_preset_class
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.utils.curve_serialization import unregister_autosave_handlers
from procedural_human.decorators.module_discovery import clear_discovered, import_all_modules

REQUIRED_PACKAGES = [
    ("tree_sitter", "tree-sitter"),
    ("tree_sitter_python", "tree-sitter-python"),
]


def check_dependencies() -> list[tuple[str, str]]:
    """
    Check which required packages are missing.
    Returns list of (import_name, pip_name) tuples for missing packages.
    """
    missing = []
    for import_name, pip_name in REQUIRED_PACKAGES:
        try:
            __import__(import_name)
        except ImportError:
            missing.append((import_name, pip_name))
    return missing


def get_blender_python_executable() -> str:
    """Get the path to Blender's Python executable."""
    return sys.executable


def ensure_pip() -> bool:
    """Ensure pip is available in Blender's Python."""
    python_exe = get_blender_python_executable()
    try:
        result = subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return True
        
        logger.info("[Procedural Human] pip not found, running ensurepip...")
        result = subprocess.run(
            [python_exe, "-m", "ensurepip", "--upgrade"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode == 0
    except Exception as e:
        logger.info(f"[Procedural Human] Error ensuring pip: {e}")
        return False


def install_package(pip_name: str) -> tuple[bool, str]:
    """
    Install a package into Blender's Python.
    Returns (success, message).
    """
    python_exe = get_blender_python_executable()
    try:
        result = subprocess.run(
            [python_exe, "-m", "pip", "install", pip_name],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True, f"Successfully installed {pip_name}"
        else:
            return False, f"Failed to install {pip_name}: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, f"Installation timed out for {pip_name}"
    except Exception as e:
        return False, f"Error installing {pip_name}: {e}"


_DEPENDENCIES_CHECKED = False
_DEPENDENCIES_INSTALLED = False
_MISSING_DEPENDENCIES: list[tuple[str, str]] = []


def ensure_dependencies() -> bool:
    """
    Check for missing dependencies and install them automatically.
    Called at registration.
    """
    global _DEPENDENCIES_CHECKED, _DEPENDENCIES_INSTALLED, _MISSING_DEPENDENCIES
    
    if _DEPENDENCIES_INSTALLED:
        return True
    
    missing = check_dependencies()
    
    if not missing:
        _DEPENDENCIES_CHECKED = True
        _DEPENDENCIES_INSTALLED = True
        _MISSING_DEPENDENCIES = []
        return True
    
    logger.info(f"\n{'='*60}")
    logger.info("PROCEDURAL HUMAN: Installing required dependencies...")
    logger.info(f"{'='*60}")
    
    if not ensure_pip():
        logger.info("ERROR: Could not ensure pip is available.")
        logger.info("Please install pip manually or run Blender as administrator.")
        logger.info(f"{'='*60}\n")
        _DEPENDENCIES_CHECKED = True
        _MISSING_DEPENDENCIES = missing
        return False
    
    all_installed = True
    for import_name, pip_name in missing:
        logger.info(f"  Installing {pip_name}...")
        success, message = install_package(pip_name)
        if success:
            logger.info(f"    ✓ {message}")
        else:
            logger.info(f"    ✗ {message}")
            all_installed = False
    
    final_missing = check_dependencies()
    
    if not final_missing:
        logger.info(f"\n✓ All dependencies installed successfully!")
        logger.info(f"{'='*60}\n")
        _DEPENDENCIES_CHECKED = True
        _DEPENDENCIES_INSTALLED = True
        _MISSING_DEPENDENCIES = []
        return True
    else:
        logger.info(f"\n✗ Some dependencies could not be installed:")
        for import_name, pip_name in final_missing:
            logger.info(f"    - {pip_name}")
        logger.info(f"\nTry running Blender as administrator, or install manually:")
        logger.info(f"  {get_blender_python_executable()} -m pip install {' '.join(pip for _, pip in final_missing)}")
        logger.info(f"{'='*60}\n")
        _DEPENDENCIES_CHECKED = True
        _MISSING_DEPENDENCIES = final_missing
        return False


from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human import menus
from procedural_human import preferences


def update_profile_curves(self, context):
    """
    Update callback for profile curve changes.
    Finds all finger objects and updates their geometry node trees.
    """

    for obj in bpy.data.objects:
        if obj.type == "MESH" and hasattr(obj, "finger_data"):
            if obj.finger_data.is_finger:

                for modifier in obj.modifiers:
                    if modifier.type == "NODES" and modifier.node_group:

                        pass

    if context.view_layer:
        context.view_layer.update()


bl_info = {
    "name": "Procedural Human Generator",
    "author": "Procedural Human Team",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh",
    "description": "Generates complete procedural humans using Geometry Nodes",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


def register_scene_properties():
    """Register scene properties for finger operations"""

    bpy.types.Scene.procedural_finger_curl_direction = bpy.props.EnumProperty(
        name="Curl Direction",
        items=[
            ("X", "X Axis", "Curl along X axis"),
            ("Y", "Y Axis", "Curl along Y axis (default)"),
            ("Z", "Z Axis", "Curl along Z axis"),
        ],
        default="Y",
        description="Axis along which the finger curls",
    )

    bpy.types.Scene.procedural_create_animation_finger = bpy.props.BoolProperty(
        name="Create Animation",
        default=True,
        description="Create keyframe animation for finger curl",
    )

    bpy.types.Scene.procedural_finger_expanded = bpy.props.BoolProperty(
        name="Finger Expanded",
        default=True,
        description="Show/hide finger panel content",
    )

    bpy.types.Scene.procedural_finger_nail_expanded = bpy.props.BoolProperty(
        name="Finger Nail Expanded",
        default=False,
        description="Show/hide finger nail panel content",
    )

    bpy.types.Scene.procedural_finger_segment_expanded = bpy.props.BoolProperty(
        name="Finger Segment Expanded",
        default=False,
        description="Show/hide finger segment panel content",
    )

    bpy.types.Scene.procedural_finger_segment_sample_count = bpy.props.IntProperty(
        name="Sample Count",
        default=SEGMENT_SAMPLE_COUNT,
        min=3,
        description="Number of samples for profile curve resolution. Higher values improve quality but increase geometry count",
        update=update_profile_curves,
    )

    bpy.types.Scene.procedural_segment_proximal_x_profile = bpy.props.PointerProperty(
        name="Proximal X Profile",
        type=bpy.types.Object,
        description="X-axis profile curve for proximal finger segment",
        poll=lambda self, obj: obj.type == "CURVE",
        update=update_profile_curves,
    )

    bpy.types.Scene.procedural_segment_proximal_y_profile = bpy.props.PointerProperty(
        name="Proximal Y Profile",
        type=bpy.types.Object,
        description="Y-axis profile curve for proximal finger segment",
        poll=lambda self, obj: obj.type == "CURVE",
        update=update_profile_curves,
    )

    bpy.types.Scene.procedural_segment_middle_x_profile = bpy.props.PointerProperty(
        name="Middle X Profile",
        type=bpy.types.Object,
        description="X-axis profile curve for middle finger segment",
        poll=lambda self, obj: obj.type == "CURVE",
        update=update_profile_curves,
    )

    bpy.types.Scene.procedural_segment_middle_y_profile = bpy.props.PointerProperty(
        name="Middle Y Profile",
        type=bpy.types.Object,
        description="Y-axis profile curve for middle finger segment",
        poll=lambda self, obj: obj.type == "CURVE",
        update=update_profile_curves,
    )

    bpy.types.Scene.procedural_segment_distal_x_profile = bpy.props.PointerProperty(
        name="Distal X Profile",
        type=bpy.types.Object,
        description="X-axis profile curve for distal finger segment",
        poll=lambda self, obj: obj.type == "CURVE",
        update=update_profile_curves,
    )

    bpy.types.Scene.procedural_segment_distal_y_profile = bpy.props.PointerProperty(
        name="Distal Y Profile",
        type=bpy.types.Object,
        description="Y-axis profile curve for distal finger segment",
        poll=lambda self, obj: obj.type == "CURVE",
        update=update_profile_curves,
    )


def unregister_scene_properties():
    """Unregister scene properties"""
    del bpy.types.Scene.procedural_finger_type
    del bpy.types.Scene.procedural_finger_curl_direction
    del bpy.types.Scene.procedural_create_animation_finger

    del bpy.types.Scene.procedural_finger_expanded
    del bpy.types.Scene.procedural_finger_nail_expanded
    del bpy.types.Scene.procedural_finger_segment_expanded
    del bpy.types.Scene.procedural_finger_segment_sample_count

    del bpy.types.Scene.procedural_segment_proximal_x_profile
    del bpy.types.Scene.procedural_segment_proximal_y_profile
    del bpy.types.Scene.procedural_segment_middle_x_profile
    del bpy.types.Scene.procedural_segment_middle_y_profile
    del bpy.types.Scene.procedural_segment_distal_x_profile
    del bpy.types.Scene.procedural_segment_distal_y_profile


def register():
    preferences.register()
    
    deps_ok = ensure_dependencies()
    if not deps_ok:
        logger.info("Procedural Human: Some features disabled due to missing dependencies.")
        logger.info("Install dependencies via addon preferences to enable all features.")
    
    register_scene_properties()
    
    import_all_modules()
    procedural_panel.discover_and_register_all_decorators()
    procedural_operator.discover_and_register_all_decorators()
    register_preset_class.discover_and_register_all_decorators()
    menus.register()
    
    try:
        from procedural_human.utils.curve_serialization import register_autosave_handlers
        register_autosave_handlers()
    except ImportError as e:
        logger.info(f"[Procedural Human] Could not register curve autosave: {e}")


def unregister():
    try:
        unregister_autosave_handlers()
    except ImportError:
        pass
    
    menus.unregister()
    procedural_panel.unregister_all_decorators()
    procedural_operator.unregister_all_decorators()
    register_preset_class.unregister_all_decorators()
    unregister_scene_properties()
    preferences.unregister()
    clear_discovered()


if __name__ == "__main__":
    register() 
