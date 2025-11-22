import bpy
import json
import importlib
import os
from bpy.types import Operator
from procedural_human.operator_decorator import (
    procedural_operator,
    dynamic_enum_operator,
    register_all_operators,
    get_all_presets,
    register_preset_data,
    Preset,
    register_preset_class,
)
from procedural_human.hand.finger.finger_segment import finger_segment_profiles


FLOAT_CURVE_PRESETS = {}


def load_presets_from_file():
    """
    Loads presets from the decorator-based registry and legacy file-based presets.
    """

    FLOAT_CURVE_PRESETS.clear()

    count = 0

    registered_presets = get_all_presets()
    FLOAT_CURVE_PRESETS.update(registered_presets)
    count += len(registered_presets)

    importlib.reload(finger_segment_profiles)

    for name in dir(finger_segment_profiles):
        if name.startswith("PRESET_"):
            data = getattr(finger_segment_profiles, name)

            display_name = name[7:].replace("_", " ").title()

            if display_name not in FLOAT_CURVE_PRESETS:
                FLOAT_CURVE_PRESETS[display_name] = data
                count += 1

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
        return

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

    if node.id_data:
        node.id_data.update_tag()


def find_float_curve_nodes_in_finger(obj):
    """
    Walks the geometry node modifiers of the object to find the Radial Profile (Dual) groups
    and extracts their internal Float Curve nodes (X Profile, Y Profile).
    Returns a dict: { "SegmentName_X": node, "SegmentName_Y": node, ... }
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
                if node.type == "GROUP" and node.node_tree:

                    seg_name = node.label
                    if not seg_name:

                        seg_name = node.node_tree.name

                    print(
                        f"    Found group node: {node.name} (Label: {node.label}, Tree: {node.node_tree.name})"
                    )

                    for inner_node in node.node_tree.nodes:
                        if inner_node.type == "GROUP" and inner_node.node_tree:

                            if (
                                "Radial Profile (Dual)" in inner_node.node_tree.name
                                or "Radial Profile (Dual)" in inner_node.label
                            ):
                                print(f"      Found Radial Profile group in {seg_name}")
                                radial_group = inner_node.node_tree
                                for deep_node in radial_group.nodes:

                                    if (
                                        deep_node.type == "FLOAT_CURVE"
                                        or deep_node.bl_idname == "ShaderNodeFloatCurve"
                                    ):

                                        if "X" in deep_node.label:
                                            axis = "X"
                                        elif "Y" in deep_node.label:
                                            axis = "Y"
                                        else:
                                            axis = "Unknown"

                                        key = f"{seg_name}_{axis}"
                                        found_nodes[key] = deep_node
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
            FLOAT_CURVE_PRESETS[self.preset_name] = preset_data

            register_preset_data(self.preset_name, preset_data)
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
    Writes the new preset data to finger_segment_profiles.py.
    """
    import os

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

    safe_name = (
        "PRESET_" + "".join(c for c in preset_name if c.isalnum() or c == "_").upper()
    )

    formatted_data = json.dumps(preset_data, indent=4)

    with open(target_path, "a") as f:
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

    all_presets = get_all_presets()

    FLOAT_CURVE_PRESETS.update(all_presets)

    return [(k, k, "") for k in sorted(all_presets.keys())]


@dynamic_enum_operator("preset_name", get_preset_enum_items, name="Preset")
@procedural_operator(
    bl_idname="node.procedural_load_float_curve_preset",
    bl_label="Load Float Curve Preset",
    bl_description="Load a preset into all finger segment profile curves",
)
class LoadFloatCurvePreset(Operator):
    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and context.active_object.type == "MESH"
            and hasattr(context.active_object, "finger_data")
        )

    def execute(self, context):
        obj = context.active_object

        load_presets_from_file()

        preset_name_value = self.preset_name

        preset_str = str(preset_name_value)
        if (
            "_PropertyDeferred" in preset_str
            or "<built-in function EnumProperty>" in preset_str
            or "EnumProperty" in preset_str
        ):

            items = get_preset_enum_items()
            if items:
                preset_name_value = items[0][0]
                self.report(
                    {"WARNING"},
                    f"No preset selected, using first available: {preset_name_value}",
                )
            else:
                self.report({"ERROR"}, "No presets available")
                return {"CANCELLED"}

        if not isinstance(preset_name_value, str):
            preset_name_value = str(preset_name_value)

        all_presets = get_all_presets()
        if preset_name_value in all_presets:
            preset_data = all_presets[preset_name_value]
        elif preset_name_value in FLOAT_CURVE_PRESETS:
            preset_data = FLOAT_CURVE_PRESETS[preset_name_value]
        else:
            self.report({"ERROR"}, f"Preset '{preset_name_value}' not found")
            return {"CANCELLED"}
        nodes_dict = find_float_curve_nodes_in_finger(obj)

        if not nodes_dict:
            self.report({"WARNING"}, "No profile curve nodes found in active object")
            return {"CANCELLED"}

        applied_count = 0
        updated_node_groups = set()

        for key, data in preset_data.items():

            target_node = nodes_dict.get(key)

            if target_node:
                apply_data_to_float_curve_node(target_node, data)

                if target_node.id_data:
                    updated_node_groups.add(target_node.id_data)
                applied_count += 1

        if applied_count > 0:

            for node_group in updated_node_groups:
                node_group.update_tag()

            for mod in obj.modifiers:
                if mod.type == "NODES" and mod.node_group:
                    mod.node_group.update_tag()

            context.view_layer.update()
            bpy.context.evaluated_depsgraph_get().update()

            self.report(
                {"INFO"},
                f"Applied preset '{self.preset_name}' to {applied_count} curves",
            )
        else:
            self.report({"WARNING"}, "No matching curves found to apply preset")

        return {"FINISHED"}


load_presets_from_file()
