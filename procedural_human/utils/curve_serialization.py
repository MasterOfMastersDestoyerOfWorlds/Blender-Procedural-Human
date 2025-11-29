import bpy
import json
import importlib
import os
import hashlib
from bpy.types import Operator
from bpy.app.handlers import persistent
from procedural_human.decorators.operator_decorator import (
    procedural_operator,
)
from procedural_human.decorators.curve_preset_decorator import (
    register_preset_class,
)
from procedural_human.utils.tree_sitter_utils import replace_get_data_method
import inspect
import os

_curve_hashes = {}
_autosave_enabled = True
_autosave_timer = None


def load_presets_from_file():
    """
    Loads presets from the decorator-based registry and legacy file-based presets.
    """

    count = 0

    registered_presets = register_preset_class.get_all_presets()
    count += len(registered_presets)

    print(
        f"Loaded {count} presets ({len(registered_presets)} from registry, {count - len(registered_presets)} from file)."
    )


def serialize_float_curve_node(node):
    """
    Serializes a ShaderNodeFloatCurve's points into a list of dicts.
    """
    if node.type != "FLOAT_CURVE" and node.bl_idname != "ShaderNodeFloatCurve":
        return None

    curve = node.mapping.curves[0]
    data = []
    for p in curve.points:
        point_data = {
            "x": p.location[0],
            "y": p.location[1],
            "handle_type": p.handle_type,
        }
        data.append(point_data)
    return data


def apply_data_to_float_curve_node(node, data):
    """
    Applies serialized point data to a ShaderNodeFloatCurve.
    """
    if node.type != "FLOAT_CURVE" and node.bl_idname != "ShaderNodeFloatCurve":
        return False

    curve = node.mapping.curves[0]

    num_points_needed = len(data)

    while len(curve.points) < num_points_needed:
        curve.points.new(0.5, 0.5)

    if len(curve.points) > num_points_needed:
        for i in range(len(curve.points) - 1, num_points_needed - 1, -1):
            curve.points.remove(curve.points[i])

    for i, point_data in enumerate(data):
        p = curve.points[i]
        p.location = (point_data["x"], point_data["y"])
        if "handle_type" in point_data:
            p.handle_type = point_data["handle_type"]

    node.mapping.update()
    node.update()

    if node.id_data:
        node.id_data.update_tag()
    return True


def find_float_curve_nodes_in_finger(obj):
    """
    Walks the geometry node modifiers of the object to find Float Curve nodes.
    Returns a dict: { "SegmentName_X": node, "SegmentName_Y": node, ... }

    Key format: "{SegmentName}_X" or "{SegmentName}_Y"
    Where SegmentName is extracted from the label by removing axis indicators.
    """
    found_nodes = {}

    if not obj or obj.type != "MESH":
        return found_nodes

    print(f"Searching for curves in {obj.name}...")

    for mod in obj.modifiers:
        if mod.type == "NODES" and mod.node_group:
            main_group = mod.node_group
            print(f"  Checking modifier {mod.name} with group {main_group.name}")

            for node in main_group.nodes:
                if (
                    node.type == "FLOAT_CURVE"
                    or node.bl_idname == "ShaderNodeFloatCurve"
                ):
                    label = node.label or ""

                    if " X " in label or label.endswith(" X") or "_X" in label:
                        axis = "X"
                        seg_name = (
                            label.replace(" X Profile", "")
                            .replace(" X Segment", "")
                            .replace("_X", "")
                            .replace(" X", "")
                            .strip()
                        )
                    elif " Y " in label or label.endswith(" Y") or "_Y" in label:
                        axis = "Y"
                        seg_name = (
                            label.replace(" Y Profile", "")
                            .replace(" Y Segment", "")
                            .replace("_Y", "")
                            .replace(" Y", "")
                            .strip()
                        )
                    else:
                        axis = "Unknown"
                        seg_name = label
                    if not seg_name:
                        seg_name = "Unknown"
                    key = (
                        f"{seg_name}_X"
                        if axis == "X"
                        else f"{seg_name}_Y" if axis == "Y" else f"{seg_name}_{axis}"
                    )
                    found_nodes[key] = node
                    print(f"        Found Curve: {key}")

    return found_nodes


@procedural_operator(
    bl_idname="node.procedural_save_float_curve_preset",
    bl_label="Save All Curves to Preset",
    bl_description="Save all finger segment profile curves as a preset",
)
class SaveFloatCurvePreset(Operator):
    preset_name: bpy.props.StringProperty(
        name="Preset Name", default="New Finger Style"
    )

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and context.active_object.type == "MESH"
            and hasattr(context.active_object, "finger_data")
        )

    def execute(self, context):
        obj = context.active_object
        nodes_dict = find_float_curve_nodes_in_finger(obj)

        if not nodes_dict:
            self.report({"WARNING"}, "No profile curve nodes found in active object")

            return {"CANCELLED"}

        preset_data = {}
        for key, node in nodes_dict.items():
            data = serialize_float_curve_node(node)
            if data:
                preset_data[key] = data

        if preset_data:
            register_preset_class.register_preset_data(self.preset_name, preset_data)

            frame = inspect.currentframe()
            try:
                caller_file = frame.f_back.f_code.co_filename if frame.f_back else None
                if caller_file and os.path.exists(caller_file):
                    caller_file = os.path.abspath(caller_file)
                else:
                    caller_file = None
            finally:
                del frame

            register_preset_class.register_preset_data(
                self.preset_name, preset_data, caller_file
            )
            self.report(
                {"INFO"},
                f"Saved preset '{self.preset_name}' with {len(preset_data)} curves",
            )

            update_profiles_file(self.preset_name, preset_data)

            load_presets_from_file()

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def update_profiles_file(preset_name, preset_data):
    """
    Updates preset data in the codebase. If preset exists, replaces it;
    otherwise appends to finger_segment_profiles.py.
    """
    import os

    # Check if preset already exists in registry
    location = register_preset_class.get_preset_location(preset_name)

    if location and location.get("file_path") and os.path.exists(location["file_path"]):
        # Preset exists, replace it using tree-sitter
        file_path = location["file_path"]
        success = replace_get_data_method(file_path, preset_name, preset_data)

        if success:
            print(f"Updated preset '{preset_name}' in {file_path}")
            return
        else:
            print(
                f"Warning: Could not replace preset '{preset_name}' in {file_path}, appending instead"
            )

    # Preset doesn't exist or replacement failed, append to default location
    current_dir = os.path.dirname(os.path.abspath(__file__))

    target_path = os.path.join(
        current_dir,
        "..",
        "hand",
        "finger",
        "finger_segment",
        "finger_segment_profiles.py",
    )
    target_path = os.path.abspath(target_path)

    if not os.path.exists(target_path):
        print(f"Error: Could not find profiles file at {target_path}")
        return

    safe_class_name = "Preset" + "".join(
        c.title() if c.isalnum() else "" for c in preset_name
    )

    formatted_data = json.dumps(preset_data, indent=4)

    with open(target_path, "a") as f:
        f.write(f"\n\n# User Preset: {preset_name}\n")
        f.write(f'@register_preset_class("{preset_name}")\n')
        f.write(f"class {safe_class_name}(Preset):\n")
        f.write(f'    """Preset for {preset_name}"""\n')
        f.write(f"    \n")
        f.write(f"    def get_data(self):\n")
        f.write(f"        return {formatted_data}\n")

    print(f"Appended preset class {safe_class_name} to {target_path}")


def get_preset_enum_items():
    """
    Returns enum items for presets from the registry.
    This ensures the enum always shows all presets from the registry.
    """

    load_presets_from_file()

    all_presets = register_preset_class.get_all_presets()

    if not all_presets:
        return [("", "No presets available", "")]

    items = [(k, k, "") for k in sorted(all_presets.keys())]
    return items


load_presets_from_file()


def _get_curve_hash(node):
    """Get a hash of a float curve node's current state."""
    if node.type != "FLOAT_CURVE" and node.bl_idname != "ShaderNodeFloatCurve":
        return None

    curve = node.mapping.curves[0]
    data = []
    for p in curve.points:
        data.append((round(p.location[0], 4), round(p.location[1], 4), p.handle_type))
    return hashlib.md5(str(data).encode()).hexdigest()


def _get_dsl_object_curves(obj):
    """Get all float curve nodes from a DSL-generated object."""
    curves = {}

    if not obj or obj.type != "MESH":
        return curves

    if not obj.get("dsl_source_file"):
        return curves

    for mod in obj.modifiers:
        if mod.type == "NODES" and mod.node_group:
            for node in mod.node_group.nodes:
                if (
                    node.type == "FLOAT_CURVE"
                    or node.bl_idname == "ShaderNodeFloatCurve"
                ):
                    label = node.label or node.name
                    curves[label] = {
                        "node": node,
                        "hash": _get_curve_hash(node),
                        "object": obj,
                        "modifier": mod,
                    }

    return curves


def check_curves_for_changes():
    """Check all DSL objects for curve changes and save if modified."""
    global _curve_hashes, _autosave_enabled

    if not _autosave_enabled:
        return 1.0

    changed_objects = {}

    for obj in bpy.data.objects:
        if not obj.get("dsl_source_file"):
            continue

        curves = _get_dsl_object_curves(obj)
        obj_name = obj.name

        for label, curve_data in curves.items():
            key = f"{obj_name}:{label}"
            new_hash = curve_data["hash"]

            if key in _curve_hashes:
                if _curve_hashes[key] != new_hash:
                    if obj_name not in changed_objects:
                        changed_objects[obj_name] = {"object": obj, "curves": {}}
                    changed_objects[obj_name]["curves"][label] = curve_data
                    _curve_hashes[key] = new_hash
            else:
                _curve_hashes[key] = new_hash

    for obj_name, obj_data in changed_objects.items():
        _auto_save_curves(obj_data["object"], obj_data["curves"])

    return 1.0


def _auto_save_curves(obj, changed_curves):
    """Auto-save changed curves for a DSL object to a separate presets file."""
    from procedural_human.utils.tree_sitter_utils import (
        ensure_presets_file_exists,
        batch_update_preset_classes,
    )

    source_file = obj.get("dsl_source_file", "")
    instance_name = obj.get("dsl_instance_name", "")

    if not source_file or not instance_name:
        return

    if not os.path.exists(source_file):
        print(f"[AutoSave] Source file not found: {source_file}")
        return

    presets_file = ensure_presets_file_exists(source_file)

    segments_data = {}
    all_curves = _get_dsl_object_curves(obj)

    for label, curve_data in all_curves.items():
        node = curve_data["node"]
        data = serialize_float_curve_node(node)
        if data:
            if " X Profile" in label:
                seg_name = label.replace(" X Profile", "").strip()
                axis = "X"
            elif " Y Profile" in label:
                seg_name = label.replace(" Y Profile", "").strip()
                axis = "Y"
            else:
                continue

            if seg_name not in segments_data:
                segments_data[seg_name] = {}
            segments_data[seg_name][f"{seg_name}_{axis}"] = data

    if not segments_data:
        return

    presets_to_update = []
    for seg_name, curves in segments_data.items():
        safe_class_name = (
            f"Preset{instance_name}{seg_name.replace('_', '').replace(' ', '')}Curves"
        )
        preset_name = f"{instance_name}_{seg_name}"
        presets_to_update.append(
            {
                "preset_name": preset_name,
                "class_name": safe_class_name,
                "curves_data": curves,
            }
        )

    success = batch_update_preset_classes(presets_file, presets_to_update)

    if success:
        preset_name = f"{instance_name}_Curves"
        combined_data = {}
        for seg_name, seg_curves in segments_data.items():
            combined_data.update(seg_curves)
        register_preset_class.register_preset_data(
            preset_name, combined_data, presets_file
        )

        print(
            f"[AutoSave] Saved curves for {instance_name} to {presets_file}: {list(changed_curves.keys())}"
        )


def start_curve_autosave():
    """Start the curve auto-save timer."""
    global _autosave_timer, _autosave_enabled
    _autosave_enabled = True

    if _autosave_timer is None:
        _autosave_timer = bpy.app.timers.register(
            check_curves_for_changes, first_interval=2.0, persistent=True
        )
        print("[AutoSave] Float curve auto-save started")


def stop_curve_autosave():
    """Stop the curve auto-save timer."""
    global _autosave_timer, _autosave_enabled
    _autosave_enabled = False

    if _autosave_timer is not None:
        try:
            bpy.app.timers.unregister(check_curves_for_changes)
        except ValueError:
            pass
        _autosave_timer = None
        print("[AutoSave] Float curve auto-save stopped")


def initialize_curve_tracking():
    """Initialize curve tracking for all DSL objects."""
    global _curve_hashes
    _curve_hashes.clear()

    for obj in bpy.data.objects:
        if obj.get("dsl_source_file"):
            curves = _get_dsl_object_curves(obj)
            for label, curve_data in curves.items():
                key = f"{obj.name}:{label}"
                _curve_hashes[key] = curve_data["hash"]

    print(f"[AutoSave] Initialized tracking for {len(_curve_hashes)} curves")


@persistent
def on_load_handler(dummy):
    """Re-initialize curve tracking when a file is loaded."""
    initialize_curve_tracking()


def register_autosave_handlers():
    """Register auto-save handlers."""
    if on_load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_load_handler)
    start_curve_autosave()


def unregister_autosave_handlers():
    """Unregister auto-save handlers."""
    stop_curve_autosave()
    if on_load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_load_handler)
