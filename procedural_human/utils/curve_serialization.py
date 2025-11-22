import bpy
import json
from bpy.types import Operator
from procedural_human.operator_decorator import procedural_operator, register_all_operators

# Registry to hold named presets in memory (could be saved to disk/addon preferences)
FLOAT_CURVE_PRESETS = {
    # "Template": {
    #     "X Profile Shape": [...], 
    #     "Y Profile Shape": [...] 
    # }
}


def serialize_float_curve_node(node):
    """
    Serializes a ShaderNodeFloatCurve's points into a list of dicts.
    """
    if node.type != 'FLOAT_CURVE':
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
    if node.type != 'FLOAT_CURVE':
        return
    
    curve = node.mapping.curves[0]
    
    num_points_needed = len(data)
    
    # Add needed points
    while len(curve.points) < num_points_needed:
        curve.points.new(0.5, 0.5)
        
    # Remove excess points
    if len(curve.points) > num_points_needed:
        for i in range(len(curve.points) - 1, num_points_needed - 1, -1):
            curve.points.remove(curve.points[i])
            
    # Update locations
    for i, point_data in enumerate(data):
        p = curve.points[i]
        p.location = (point_data["x"], point_data["y"])
        if "handle_type" in point_data:
            p.handle_type = point_data["handle_type"]
            
    node.mapping.update()


def find_float_curve_nodes_in_finger(obj):
    """
    Walks the geometry node modifiers of the object to find the Radial Profile (Dual) groups
    and extracts their internal Float Curve nodes (X Profile, Y Profile).
    Returns a dict: { "SegmentName_X": node, "SegmentName_Y": node, ... }
    """
    found_nodes = {}
    
    if not obj or obj.type != 'MESH':
        return found_nodes

    print(f"Searching for curves in {obj.name}...")

    # 1. Find the main Geometry Nodes modifier
    for mod in obj.modifiers:
        if mod.type == 'NODES' and mod.node_group:
            main_group = mod.node_group
            print(f"  Checking modifier {mod.name} with group {main_group.name}")
            
            # Iterate through nodes in the main group to find segment groups
            for node in main_group.nodes:
                if node.type == 'GROUP' and node.node_tree:
                    # Identify if this is a finger segment group
                    # We assume the label or name contains "Segment" or specific types like "Proximal"
                    # Or better, check if the group has "Radial Profile (Dual)" inside it by checking structure?
                    # Using label matching for now as we set it in creation.
                    
                    seg_name = node.label
                    if not seg_name:
                        # Try to infer from node_tree name
                        seg_name = node.node_tree.name
                        
                    # Filter to relevant groups if possible
                    # e.g., Proximal, Middle, Distal
                    
                    print(f"    Found group node: {node.name} (Label: {node.label}, Tree: {node.node_tree.name})")
                    
                    # Dive into the segment group
                    for inner_node in node.node_tree.nodes:
                        if inner_node.type == 'GROUP' and inner_node.node_tree:
                            # Check for Radial Profile group
                            # Name set in code: "Radial Profile (Dual)"
                            if "Radial Profile (Dual)" in inner_node.node_tree.name or "Radial Profile (Dual)" in inner_node.label:
                                print(f"      Found Radial Profile group in {seg_name}")
                                radial_group = inner_node.node_tree
                                for deep_node in radial_group.nodes:
                                    # Debug print to identify node types
                                    # print(f"        Node: {deep_node.name}, Type: {deep_node.type}, ID: {deep_node.bl_idname}")
                                    
                                    if deep_node.type == 'FLOAT_CURVE' or deep_node.bl_idname == 'ShaderNodeFloatCurve':
                                        # Label should be "X Profile" or "Y Profile"
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
    bl_label="Save Float Curve Preset",
    bl_description="Save all finger segment profile curves as a preset"
)
class SaveFloatCurvePreset(Operator):
    preset_name: bpy.props.StringProperty(name="Preset Name", default="New Finger Style")

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH' and hasattr(context.active_object, "finger_data")

    def execute(self, context):
        obj = context.active_object
        nodes_dict = find_float_curve_nodes_in_finger(obj)
        
        if not nodes_dict:
            self.report({'WARNING'}, "No profile curve nodes found in active object")
            # Don't cancel, just warn, maybe the structure is different
            return {'CANCELLED'}
            
        preset_data = {}
        for key, node in nodes_dict.items():
            data = serialize_float_curve_node(node)
            if data:
                preset_data[key] = data
        
        if preset_data:
            FLOAT_CURVE_PRESETS[self.preset_name] = preset_data
            self.report({'INFO'}, f"Saved preset '{self.preset_name}' with {len(preset_data)} curves")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


@procedural_operator(
    bl_idname="node.procedural_load_float_curve_preset",
    bl_label="Load Float Curve Preset",
    bl_description="Load a preset into all finger segment profile curves"
)
class LoadFloatCurvePreset(Operator):
    preset_name: bpy.props.EnumProperty(
        name="Preset",
        items=lambda self, context: [(k, k, "") for k in FLOAT_CURVE_PRESETS.keys()]
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH' and hasattr(context.active_object, "finger_data")

    def execute(self, context):
        obj = context.active_object
        if self.preset_name not in FLOAT_CURVE_PRESETS:
            return {'CANCELLED'}
            
        preset_data = FLOAT_CURVE_PRESETS[self.preset_name]
        nodes_dict = find_float_curve_nodes_in_finger(obj)
        
        applied_count = 0
        for key, data in preset_data.items():
            # Try to match keys loosely if exact match fails?
            # E.g. "Proximal Segment_X"
            target_node = nodes_dict.get(key)
            
            # Fallback: if preset has generic keys like "X" or "Y" (not implemented yet, but good for future)
            
            if target_node:
                apply_data_to_float_curve_node(target_node, data)
                applied_count += 1
                
        if applied_count > 0:
            self.report({'INFO'}, f"Applied preset to {applied_count} curves")
        else:
            self.report({'WARNING'}, "No matching curves found to apply preset")
            
        # Force update
        context.view_layer.update()
        return {'FINISHED'}
