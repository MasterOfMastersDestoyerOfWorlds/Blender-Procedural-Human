"""
Export Spreadsheet Data to CSV

Exports attribute data from the active object based on the Spreadsheet editor settings.
Works with any geometry type (MESH, CURVE, CURVES) and any domain (POINT, EDGE, FACE, CURVE).

Supports:
- Mesh attributes (object mode)
- BMesh layers (edit mode) - including edge float layers from loft handle gizmos
"""

import bpy
import bmesh
import csv
import os
from pathlib import Path
from bpy.types import Operator
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.config import get_codebase_path

CODEBASE_PATH = get_codebase_path()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_tmp_base_dir():
    """Get the tmp directory path for exports."""
    if CODEBASE_PATH:
        base_dir = CODEBASE_PATH / "tmp"
    else:
        base_dir = Path(os.path.dirname(__file__)).parent / "tmp"
    
    base_dir.mkdir(parents=True, exist_ok=True)
    
    init_path = base_dir / "__init__.py"
    if not init_path.exists():
        try:
            init_path.touch()
        except Exception:
            pass
    
    return base_dir


def get_next_csv_path(base_dir, prefix):
    """Get next available numbered CSV path."""
    base_dir = Path(base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    
    i = 0
    while True:
        path = base_dir / f"{prefix}_{i}.csv"
        if not path.exists():
            return path
        i += 1


def find_spreadsheet_area():
    """Find the first Spreadsheet editor in the current screen."""
    for area in bpy.context.screen.areas:
        if area.type == 'SPREADSHEET':
            return area
    return None


def get_spreadsheet_settings(area):
    """Get the current settings from a Spreadsheet editor."""
    space = area.spaces.active
    return {
        'domain': space.attribute_domain,  # 'POINT', 'FACE', 'EDGE', 'CURVE', 'CORNER'
        'component': space.geometry_component_type,  # 'MESH', 'CURVE', 'CURVES', 'INSTANCES'
        'eval_state': space.object_eval_state,  # 'EVALUATED' or 'VIEWER_NODE'
    }


def get_domain_row_count(data, component, domain):
    """
    Get the row count for a domain from the geometry structure.
    This is more reliable than len(attr.data) for evaluated geometry.
    """
    row_count = 0
    
    if component == 'MESH':
        if domain == 'POINT' and hasattr(data, 'vertices'):
            row_count = len(data.vertices)
        elif domain == 'EDGE' and hasattr(data, 'edges'):
            row_count = len(data.edges)
        elif domain == 'FACE' and hasattr(data, 'polygons'):
            row_count = len(data.polygons)
        elif domain == 'CORNER' and hasattr(data, 'loops'):
            row_count = len(data.loops)
            
    elif component == 'CURVE' and hasattr(data, 'splines'):
        if domain == 'POINT':
            row_count = sum(len(s.points) + len(s.bezier_points) for s in data.splines)
        elif domain == 'CURVE':
            row_count = len(data.splines)
            
    elif component == 'CURVES':
        if domain == 'POINT':
            if hasattr(data, 'points'):
                row_count = len(data.points)
            elif hasattr(data, 'attributes') and 'position' in data.attributes:
                try:
                    row_count = len(data.attributes['position'].data)
                except Exception:
                    pass
        elif domain == 'CURVE' and hasattr(data, 'curves'):
            row_count = len(data.curves)
    
    return row_count


def export_bmesh_edge_layers(obj, output_dir):
    """
    Export BMesh edge float layers to CSV.
    Used when in edit mode with BMesh layer data (like loft handles).
    
    Args:
        obj: The mesh object (must be in edit mode)
        output_dir: Output directory path
        
    Returns:
        Tuple of (csv_path, row_count, headers) or None if no layers found
    """
    if obj.mode != 'EDIT':
        return None
    
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)
    bm.edges.ensure_lookup_table()
    
    # Collect all edge float layers
    float_layers = {}
    for layer in bm.edges.layers.float:
        float_layers[layer.name] = layer
    
    if not float_layers:
        return None
    
    row_count = len(bm.edges)
    if row_count == 0:
        return None
    
    print(f"Found {len(float_layers)} BMesh edge float layers with {row_count} edges")
    
    # Build columns
    columns = {}
    headers = []
    
    # Add edge index and vertex indices
    columns["edge_index"] = list(range(row_count))
    headers.append("edge_index")
    
    columns["vert0_index"] = [e.verts[0].index for e in bm.edges]
    columns["vert1_index"] = [e.verts[1].index for e in bm.edges]
    headers.extend(["vert0_index", "vert1_index"])
    
    # Add vertex positions
    columns["vert0_x"] = [e.verts[0].co.x for e in bm.edges]
    columns["vert0_y"] = [e.verts[0].co.y for e in bm.edges]
    columns["vert0_z"] = [e.verts[0].co.z for e in bm.edges]
    columns["vert1_x"] = [e.verts[1].co.x for e in bm.edges]
    columns["vert1_y"] = [e.verts[1].co.y for e in bm.edges]
    columns["vert1_z"] = [e.verts[1].co.z for e in bm.edges]
    headers.extend(["vert0_x", "vert0_y", "vert0_z", "vert1_x", "vert1_y", "vert1_z"])
    
    # Add all float layers
    for layer_name, layer in float_layers.items():
        columns[layer_name] = [e[layer] for e in bm.edges]
        headers.append(layer_name)
    
    # Generate filename
    obj_name = obj.name.replace(" ", "_").replace(".", "_")
    csv_path = get_next_csv_path(output_dir, f"bmesh_{obj_name}_edges")
    
    # Write CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(zip(*[columns[h] for h in headers]))
    
    return csv_path, row_count, headers


def read_attr_float(attr, buf_len):
    """Read a FLOAT attribute, with fallback to direct item access."""
    try:
        buf = [0.0] * buf_len
        attr.data.foreach_get("value", buf)
        return buf
    except Exception:
        # Fallback to direct access
        return [attr.data[i].value for i in range(buf_len)]


def read_attr_int(attr, buf_len):
    """Read an INT attribute, with fallback to direct item access."""
    try:
        buf = [0] * buf_len
        attr.data.foreach_get("value", buf)
        return buf
    except Exception:
        # Fallback to direct access
        return [attr.data[i].value for i in range(buf_len)]


def read_attr_bool(attr, buf_len):
    """Read a BOOLEAN attribute, with fallback to direct item access."""
    try:
        buf = [False] * buf_len
        attr.data.foreach_get("value", buf)
        return buf
    except Exception:
        # Fallback to direct access
        return [attr.data[i].value for i in range(buf_len)]


def read_attr_vector(attr, buf_len, components):
    """Read a vector attribute (FLOAT_VECTOR, FLOAT2, QUATERNION), with fallback."""
    try:
        buf = [0.0] * (buf_len * components)
        # Try 'vector' first (for FLOAT_VECTOR, FLOAT2)
        try:
            attr.data.foreach_get("vector", buf)
        except Exception:
            # Try 'value' (for QUATERNION)
            attr.data.foreach_get("value", buf)
        return buf
    except Exception:
        # Fallback to direct access
        result = []
        for i in range(buf_len):
            item = attr.data[i]
            # Try different attribute names
            if hasattr(item, 'vector'):
                vec = item.vector
            elif hasattr(item, 'value'):
                vec = item.value
            else:
                vec = [0.0] * components
            result.extend(vec[:components])
        return result


def read_attr_color(attr, buf_len):
    """Read a color attribute (FLOAT_COLOR, BYTE_COLOR), with fallback."""
    try:
        buf = [0.0] * (buf_len * 4)
        attr.data.foreach_get("color", buf)
        return buf
    except Exception:
        # Fallback to direct access
        result = []
        for i in range(buf_len):
            c = attr.data[i].color
            result.extend([c[0], c[1], c[2], c[3]])
        return result


def read_attr_generic(attr, buf_len):
    """Try to read any attribute type by probing for common properties."""
    try:
        item = attr.data[0]
        
        # Try common property names
        for prop in ['value', 'vector', 'color']:
            if hasattr(item, prop):
                val = getattr(item, prop)
                if isinstance(val, (int, float, bool)):
                    return [getattr(attr.data[i], prop) for i in range(buf_len)]
                elif hasattr(val, '__iter__'):
                    # It's a sequence
                    result = []
                    for i in range(buf_len):
                        v = getattr(attr.data[i], prop)
                        result.extend(list(v))
                    return result
        
        return None
    except Exception:
        return None


def export_spreadsheet_data(obj, settings, output_dir):
    """
    Export data based on spreadsheet settings.
    
    Args:
        obj: The object to export from
        settings: Dict with 'domain', 'component', 'eval_state'
        output_dir: Output directory path
        
    Returns:
        Tuple of (csv_path, row_count, headers)
    """
    domain = settings['domain']
    component = settings['component']
    
    # Special case: In edit mode with EDGE domain, try BMesh layers first
    if obj.mode == 'EDIT' and domain == 'EDGE' and obj.type == 'MESH':
        result = export_bmesh_edge_layers(obj, output_dir)
        if result:
            print("Exported from BMesh edge layers (edit mode)")
            return result
        print("No BMesh edge layers found, falling back to mesh attributes...")
    
    # Get evaluated data
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    data = eval_obj.data
    
    # Get row count from geometry structure (more reliable than attr.data length)
    row_count = get_domain_row_count(data, component, domain)
    
    if row_count == 0:
        raise ValueError(f"No geometry data found for Component: {component} / Domain: {domain}")
    
    print(f"Exporting {component}/{domain} with {row_count} rows")
    
    # Build columns and headers
    columns = {}
    headers = []
    
    # --- Standard Position (special case for POINT domain on MESH) ---
    if domain == 'POINT' and component == 'MESH' and row_count > 0:
        raw_pos = [0.0] * (row_count * 3)
        try:
            if hasattr(data, "vertices") and len(data.vertices) == row_count:
                data.vertices.foreach_get("co", raw_pos)
                if any(v != 0.0 for v in raw_pos):
                    columns["Position_X"] = raw_pos[0::3]
                    columns["Position_Y"] = raw_pos[1::3]
                    columns["Position_Z"] = raw_pos[2::3]
                    headers.extend(["Position_X", "Position_Y", "Position_Z"])
        except Exception as e:
            print(f"Note: Could not export vertex positions: {e}")
    
    # --- Export all attributes matching the domain ---
    if hasattr(data, 'attributes'):
        print(f"Found {len(data.attributes)} total attributes, filtering for domain '{domain}'")
        
        for name, attr in data.attributes.items():
            if attr.domain != domain:
                continue
            
            # Skip position if already exported
            if name == 'position' and 'Position_X' in columns:
                continue
            
            # Check actual data length
            try:
                actual_len = len(attr.data)
            except Exception:
                actual_len = 0
            
            # Skip attributes with no data
            if actual_len == 0:
                print(f"Skipping attribute '{name}': has 0 data items (attribute defined but not populated)")
                continue
            
            # Use actual_len for buffer if it differs from row_count
            buf_len = actual_len if actual_len > 0 else row_count
            
            d_type = attr.data_type
            print(f"  Processing attribute '{name}': type={d_type}, len={buf_len}")
            
            try:
                if d_type == 'FLOAT':
                    buf = read_attr_float(attr, buf_len)
                    columns[name] = buf
                    headers.append(name)
                    
                elif d_type in ('INT', 'INT32'):
                    buf = read_attr_int(attr, buf_len)
                    columns[name] = buf
                    headers.append(name)
                    
                elif d_type == 'FLOAT_VECTOR':
                    buf = read_attr_vector(attr, buf_len, 3)
                    columns[f"{name}_X"] = buf[0::3]
                    columns[f"{name}_Y"] = buf[1::3]
                    columns[f"{name}_Z"] = buf[2::3]
                    headers.extend([f"{name}_X", f"{name}_Y", f"{name}_Z"])
                    
                elif d_type in ('FLOAT2', 'INT32_2D'):
                    buf = read_attr_vector(attr, buf_len, 2)
                    columns[f"{name}_X"] = buf[0::2]
                    columns[f"{name}_Y"] = buf[1::2]
                    headers.extend([f"{name}_X", f"{name}_Y"])
                    
                elif d_type == 'FLOAT_COLOR' or d_type == 'BYTE_COLOR':
                    buf = read_attr_color(attr, buf_len)
                    columns[f"{name}_R"] = buf[0::4]
                    columns[f"{name}_G"] = buf[1::4]
                    columns[f"{name}_B"] = buf[2::4]
                    columns[f"{name}_A"] = buf[3::4]
                    headers.extend([f"{name}_R", f"{name}_G", f"{name}_B", f"{name}_A"])
                    
                elif d_type == 'BOOLEAN':
                    buf = read_attr_bool(attr, buf_len)
                    columns[name] = buf
                    headers.append(name)
                    
                elif d_type == 'INT8':
                    buf = read_attr_int(attr, buf_len)
                    columns[name] = buf
                    headers.append(name)
                    
                elif d_type == 'QUATERNION':
                    buf = read_attr_vector(attr, buf_len, 4)
                    columns[f"{name}_W"] = buf[0::4]
                    columns[f"{name}_X"] = buf[1::4]
                    columns[f"{name}_Y"] = buf[2::4]
                    columns[f"{name}_Z"] = buf[3::4]
                    headers.extend([f"{name}_W", f"{name}_X", f"{name}_Y", f"{name}_Z"])
                    
                else:
                    # Try generic fallback for unknown types
                    print(f"    Unknown type '{d_type}', trying generic read...")
                    buf = read_attr_generic(attr, buf_len)
                    if buf:
                        columns[name] = buf
                        headers.append(name)
                    
            except Exception as e:
                import traceback
                print(f"Warning: Could not export attribute '{name}': {e}")
                traceback.print_exc()
    
    if not headers:
        # List what we found for debugging
        all_attrs = []
        empty_attrs = []
        if hasattr(data, 'attributes'):
            for name, attr in data.attributes.items():
                try:
                    attr_len = len(attr.data)
                except Exception:
                    attr_len = 0
                info = f"{name} ({attr.domain}, {attr.data_type}, len={attr_len})"
                all_attrs.append(info)
                if attr.domain == domain and attr_len == 0:
                    empty_attrs.append(name)
        
        msg = f"No exportable attributes found for domain '{domain}'.\n"
        msg += f"Geometry has {row_count} {domain.lower()}s.\n"
        if empty_attrs:
            msg += f"\nAttributes DEFINED on {domain} but with NO DATA (len=0):\n"
            msg += f"  {', '.join(empty_attrs)}\n"
            msg += "\nThis means these attributes exist in the definition but were never populated.\n"
            msg += "Check your geometry nodes - use 'Store Named Attribute' to actually write data.\n"
        msg += f"\nAll available attributes: {', '.join(all_attrs) if all_attrs else 'None'}"
        
        raise ValueError(msg)
    
    # Generate filename based on object and settings
    obj_name = obj.name.replace(" ", "_").replace(".", "_")
    csv_path = get_next_csv_path(output_dir, f"spreadsheet_{obj_name}_{component}_{domain}")
    
    # Write CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(zip(*[columns[h] for h in headers]))
    
    return csv_path, row_count, headers


# ============================================================================
# OPERATOR
# ============================================================================

@procedural_operator
class CURVE_OT_export_curve_to_csv(Operator):
    """Export evaluated geometry data from the active Spreadsheet to CSV"""
    
    bl_idname = "curve.export_curve_to_csv"
    bl_label = "Export Spreadsheet to CSV"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}
        
        # Find the Spreadsheet editor
        area = find_spreadsheet_area()
        
        if area:
            settings = get_spreadsheet_settings(area)
            
            if settings['eval_state'] == 'VIEWER_NODE':
                self.report({'WARNING'}, 
                    "Spreadsheet is looking at a VIEWER NODE. "
                    "Python cannot access Viewer Nodes directly. "
                    "Connect your geometry to Group Output instead. "
                    "Falling back to Group Output data...")
        else:
            # No spreadsheet found - use sensible defaults
            settings = {
                'domain': 'POINT',
                'component': 'MESH',
                'eval_state': 'EVALUATED',
            }
            self.report({'INFO'}, "No Spreadsheet found, using MESH/POINT defaults")
        
        output_dir = get_tmp_base_dir()
        
        try:
            csv_path, row_count, headers = export_spreadsheet_data(obj, settings, output_dir)
            
            self.report({'INFO'}, 
                f"Exported {row_count} rows ({len(headers)} columns) to {csv_path.name}")
            return {'FINISHED'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}
