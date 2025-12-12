import bpy
import os
import re
from pathlib import Path
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.config import get_codebase_path
from bpy.types import Operator, Panel
from collections.abc import Iterable

CODEBASE_PATH = get_codebase_path()

def get_next_temp_file_path(base_dir, prefix="temp_"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    files = os.listdir(base_dir)
    count = 0
    pattern = re.compile(f"{prefix}(\d+).py")
    
    existing_indices = []
    for f in files:
        match = pattern.match(f)
        if match:
            existing_indices.append(int(match.group(1)))
    
    if existing_indices:
        count = max(existing_indices) + 1
    
    return os.path.join(base_dir, f"{prefix}{count}.py")

def clean_string(s):
    return s.replace('"', '\\"').replace('\n', '\\n')

def to_python_repr(val):
    if isinstance(val, str):
        return f'"{clean_string(val)}"'
    if isinstance(val, (int, float, bool)):
        return str(val)
    if hasattr(val, "to_tuple"): # Vector, Color, Euler, Quaternion
        return str(val.to_tuple())
    if hasattr(val, "to_list"):
        return str(val.to_list())
    # Handle bpy_prop_array and other iterables
    if isinstance(val, Iterable):
        try:
            return str(list(val))
        except:
            pass
    # Fallback
    return str(val)

def to_snake_case(name):
    s = name.replace(" ", "_").replace(".", "_")
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def get_unique_var_name(name, existing_names):
    base_name = to_snake_case(name)
    # Remove consecutive underscores
    base_name = re.sub(r'_{2,}', '_', base_name)
    
    if base_name not in existing_names:
        return base_name
    
    # If ends with number, might be cleaner to handle?
    # But simple increment logic is fine
    count = 1
    while f"{base_name}_{count}" in existing_names:
        count += 1
    return f"{base_name}_{count}"

def generate_python_code(node_group, function_name="create_node_group"):
    lines = []
    lines.append("import bpy")
    lines.append("import math")
    lines.append("from mathutils import Vector, Color, Matrix, Euler")
    lines.append("from procedural_human.utils.node_layout import auto_layout_nodes")
    lines.append("")
    
    lines.append(f"def {function_name}():")
    lines.append(f'    group_name = "{node_group.name}"')
    lines.append(f"    if group_name in bpy.data.node_groups:")
    lines.append(f"        return bpy.data.node_groups[group_name]")
    lines.append("")
    lines.append(f'    group = bpy.data.node_groups.new(group_name, "{node_group.bl_idname}")')
    lines.append("")
    
    # Interface
    lines.append("    # --- Interface ---")
    for item in node_group.interface.items_tree:
        socket_type = item.socket_type
        name = clean_string(item.name)
        # item_type is 'INPUT', 'OUTPUT', 'PANEL'
        if item.item_type == 'PANEL':
            continue 
            
        io_type = item.in_out
        
        lines.append(f'    socket = group.interface.new_socket(name="{name}", in_out="{io_type}", socket_type="{socket_type}")')
        
        # Defaults (only for inputs usually)
        if io_type == 'INPUT':
            if hasattr(item, "default_value"):
                val = item.default_value
                # Check type
                if not isinstance(val, (bpy.types.Object, bpy.types.Collection, bpy.types.Image, bpy.types.Material, bpy.types.Texture)):
                     lines.append(f'    socket.default_value = {to_python_repr(val)}')
        
        # Attributes
        if hasattr(item, "min_value"):
             lines.append(f'    socket.min_value = {item.min_value}')
        if hasattr(item, "max_value"):
             lines.append(f'    socket.max_value = {item.max_value}')
             
    lines.append("")
    lines.append("    # --- Nodes ---")
    lines.append("    nodes = group.nodes")
    lines.append("    links = group.links")
    
    node_var_map = {} # node.name -> var_name
    existing_var_names = set()
    
    # Pre-calculate variable names
    for node in node_group.nodes:
        var_name = get_unique_var_name(node.name, existing_var_names)
        existing_var_names.add(var_name)
        node_var_map[node.name] = var_name

    processed_nodes = set()
    
    # Attributes to skip
    skip_props = {
        'rna_type', 'name', 'label', 'location', 'width', 'height', 'inputs', 'outputs', 
        'parent', 'color', 'select', 'dimensions', 'interface',
        'bl_icon', 'bl_width_default', 'bl_width_min', 'bl_width_max', 
        'bl_height_default', 'bl_height_min', 'bl_height_max', 
        'location_absolute', 'warning_propagation', 'use_custom_color', 
        'show_options', 'show_preview', 'hide', 'mute', 'show_texture', 
        'bl_description', 'bl_idname'
    }

    # Create nodes
    for node in node_group.nodes:
        var_name = node_var_map[node.name]
        
        lines.append(f'    {var_name} = nodes.new("{node.bl_idname}")')
        lines.append(f'    {var_name}.name = "{clean_string(node.name)}"')
        lines.append(f'    {var_name}.label = "{clean_string(node.label)}"')
        lines.append(f'    {var_name}.location = ({node.location.x}, {node.location.y})')
        
        # Properties
        for prop in node.bl_rna.properties:
            if prop.identifier in skip_props:
                continue
            if prop.is_readonly:
                continue
                
            try:
                val = getattr(node, prop.identifier)
                # Skip if it is a bpy_prop_collection or complex object
                if isinstance(val, (bpy.types.NodeSocket, bpy.types.NodeInputs, bpy.types.NodeOutputs)):
                    continue
                    
                # Handling Enums, Ints, Floats, Strings, Booleans, Vectors, Colors
                lines.append(f'    {var_name}.{prop.identifier} = {to_python_repr(val)}')
            except:
                pass
        
        # Input Defaults
        for j, inp in enumerate(node.inputs):
            if not inp.is_linked:
                # Set default value if it exists and is not an ID pointer
                if hasattr(inp, "default_value"):
                    val = inp.default_value
                    if val is not None and not isinstance(val, (bpy.types.Object, bpy.types.Collection, bpy.types.Image, bpy.types.Material, bpy.types.Texture)):
                         # Only write if it's not the standard default? 
                         # For now write all to be safe, or user might want clean output. 
                         # User complained about format, not redundancy.
                         lines.append(f'    # {inp.name}')
                         lines.append(f'    {var_name}.inputs[{j}].default_value = {to_python_repr(val)}')

        # Mark as processed
        processed_nodes.add(node.name)
        
        # --- Generate Links involving this node ---
        # Links should be generated if the other end of the link is already processed
        lines.append(f'    # Links for {var_name}')
        
        for link in node_group.links:
            if not link.is_valid:
                continue
                
            from_node = link.from_node
            to_node = link.to_node
            
            # Identify if this link connects current node to a previously processed node (or itself)
            other_node = None
            if from_node == node and to_node.name in processed_nodes:
                other_node = to_node
            elif to_node == node and from_node.name in processed_nodes:
                other_node = from_node
            
            if other_node:
                from_var = node_var_map.get(from_node.name)
                to_var = node_var_map.get(to_node.name)
                
                # Find socket indices
                from_idx = -1
                for k, out in enumerate(from_node.outputs):
                    if out == link.from_socket:
                        from_idx = k
                        break
                
                to_idx = -1
                for k, inp in enumerate(to_node.inputs):
                    if inp == link.to_socket:
                        to_idx = k
                        break
                
                if from_idx != -1 and to_idx != -1:
                    lines.append(f'    links.new({from_var}.outputs[{from_idx}], {to_var}.inputs[{to_idx}])')

        lines.append("")

    lines.append("    auto_layout_nodes(group)")
    lines.append("    return group")
    
    return "\n".join(lines)

@procedural_operator
class NODE_OT_export_active_group_to_python(Operator):
    """Export the currently active node group to a Python script"""
    bl_idname = "node.export_active_group_to_python"
    bl_label = "Export Active Node Group to Python"
    
    def execute(self, context):
        # Determine active node group
        node_group = None
        
        # Try Context Space Data (Node Editor)
        if context.space_data and context.space_data.type == 'NODE_EDITOR':
            node_group = context.space_data.edit_tree
            if not node_group:
                node_group = context.space_data.node_tree
        
        # Try Active Object Modifier
        if not node_group and context.active_object:
            for mod in context.active_object.modifiers:
                if mod.type == 'NODES' and mod.node_group:
                    node_group = mod.node_group
                    break
        
        if not node_group:
            self.report({'ERROR'}, "No active node group found")
            return {'CANCELLED'}
            
        code = generate_python_code(node_group, function_name=f"create_{clean_string(node_group.name).replace(' ', '_').lower()}_group")
        
        # Determine export directory
        if CODEBASE_PATH:
            base_dir = CODEBASE_PATH / "procedural_human" / "tmp"
        else:
            # Fallback to local temp directory if codebase path not found
            base_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "tmp"
        
        # Ensure directory exists
        try:
            base_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.report({'WARNING'}, f"Could not create directory {base_dir}: {e}. Falling back to default.")
            base_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "tmp"
            if not os.path.exists(str(base_dir)):
                os.makedirs(str(base_dir))
        
        file_path = get_next_temp_file_path(str(base_dir))
        
        with open(file_path, "w") as f:
            f.write(code)
            
        self.report({'INFO'}, f"Exported to {file_path}")
        return {'FINISHED'}

@procedural_panel
class NODE_PT_node_export(Panel):
    bl_label = "Node Export"
    bl_idname = "PROCEDURAL_PT_node_export"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Procedural"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("node.export_active_group_to_python")
