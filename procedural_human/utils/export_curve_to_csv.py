"""
Export Curve/Spline Data to CSV

Exports all curve and control point data from the active object's
evaluated geometry (after geometry nodes) to CSV files in the tmp folder.

Works with:
- Native CURVE objects
- Mesh/other objects with geometry nodes that output curves
"""

import bpy
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


def format_vector(vec):
    """Format a vector as separate values."""
    return list(vec[:])


# ============================================================================
# EVALUATED CURVES EXPORT (Geometry Nodes output)
# ============================================================================

def get_evaluated_curves(obj):
    """
    Get the evaluated curves data from an object.
    Works with geometry nodes that output curves.
    
    Returns:
        Curves data block or None if no curves found
    """
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    
    # Check if evaluated object has curves data
    if eval_obj.type == 'CURVES':
        return eval_obj.data
    
    # Try to get curves from geometry nodes output
    # The evaluated data might be a Curves type even if original is Mesh
    eval_data = eval_obj.data
    
    # Check if it's a Curves datablock
    if hasattr(eval_data, 'curves') and hasattr(eval_data, 'points'):
        return eval_data
    
    # For CURVE type objects, we need different handling
    if eval_obj.type == 'CURVE':
        return eval_data
    
    return None


def export_curves_geometry_to_csv(curves_data, output_dir, obj_name):
    """
    Export curves using the new Curves API (Blender 3.x+).
    This is used for geometry nodes curve output.
    
    The Curves datablock has:
    - curves_data.curves: Collection of individual curves (like splines)
    - curves_data.points: All control points across all curves
    - curves_data.attributes: All attributes
    """
    created_files = []
    
    # -------------------------------------------------------------------------
    # 1. Export curve (spline) level data
    # -------------------------------------------------------------------------
    if hasattr(curves_data, 'curves'):
        csv_path = get_next_csv_path(output_dir, f"{obj_name}_curves")
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Get curve-domain attributes
            curve_attrs = {}
            if hasattr(curves_data, 'attributes'):
                for attr in curves_data.attributes:
                    if attr.domain == 'CURVE':
                        curve_attrs[attr.name] = attr
            
            # Build header
            header = ["curve_index", "point_count", "first_point_index"]
            for attr_name in curve_attrs.keys():
                attr = curve_attrs[attr_name]
                header.extend(_get_attr_header_columns(attr_name, attr.data_type))
            
            writer.writerow(header)
            
            # Write curve data
            for i, curve in enumerate(curves_data.curves):
                row = [
                    i,
                    curve.points_length,
                    curve.first_point_index,
                ]
                
                # Add attribute values
                for attr_name, attr in curve_attrs.items():
                    row.extend(_get_attr_value(attr, i))
                
                writer.writerow(row)
        
        created_files.append(csv_path)
    
    # -------------------------------------------------------------------------
    # 2. Export point level data with all attributes
    # -------------------------------------------------------------------------
    if hasattr(curves_data, 'points') or hasattr(curves_data, 'attributes'):
        csv_path = get_next_csv_path(output_dir, f"{obj_name}_points")
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Get point-domain attributes
            point_attrs = {}
            if hasattr(curves_data, 'attributes'):
                for attr in curves_data.attributes:
                    if attr.domain == 'POINT':
                        point_attrs[attr.name] = attr
            
            # Build header - always include position
            header = ["point_index", "curve_index"]
            for attr_name in point_attrs.keys():
                attr = point_attrs[attr_name]
                header.extend(_get_attr_header_columns(attr_name, attr.data_type))
            
            writer.writerow(header)
            
            # Build curve index lookup
            curve_for_point = []
            if hasattr(curves_data, 'curves'):
                for curve_idx, curve in enumerate(curves_data.curves):
                    for _ in range(curve.points_length):
                        curve_for_point.append(curve_idx)
            
            # Write point data
            point_count = len(curves_data.points) if hasattr(curves_data, 'points') else 0
            if point_count == 0 and point_attrs:
                # Get count from first attribute
                first_attr = next(iter(point_attrs.values()))
                point_count = len(first_attr.data)
            
            for i in range(point_count):
                curve_idx = curve_for_point[i] if i < len(curve_for_point) else -1
                row = [i, curve_idx]
                
                # Add attribute values
                for attr_name, attr in point_attrs.items():
                    row.extend(_get_attr_value(attr, i))
                
                writer.writerow(row)
        
        created_files.append(csv_path)
    
    return created_files


def _get_attr_header_columns(attr_name, data_type):
    """Get header column names for an attribute based on its data type."""
    if data_type in ('FLOAT', 'INT', 'INT8', 'INT_8', 'BOOLEAN', 'STRING'):
        return [attr_name]
    elif data_type == 'FLOAT_VECTOR':
        return [f"{attr_name}.x", f"{attr_name}.y", f"{attr_name}.z"]
    elif data_type in ('FLOAT_COLOR', 'BYTE_COLOR'):
        return [f"{attr_name}.r", f"{attr_name}.g", f"{attr_name}.b", f"{attr_name}.a"]
    elif data_type in ('FLOAT2', 'INT32_2D'):
        return [f"{attr_name}.x", f"{attr_name}.y"]
    elif data_type == 'QUATERNION':
        return [f"{attr_name}.w", f"{attr_name}.x", f"{attr_name}.y", f"{attr_name}.z"]
    return [attr_name]


def _get_attr_value(attr, index):
    """Get attribute value at index, handling different data types."""
    try:
        data_type = attr.data_type
        
        if data_type in ('FLOAT', 'INT', 'INT8', 'INT_8', 'BOOLEAN', 'STRING'):
            return [attr.data[index].value]
        elif data_type in ('FLOAT_VECTOR', 'FLOAT2'):
            return list(attr.data[index].vector[:])
        elif data_type in ('FLOAT_COLOR', 'BYTE_COLOR'):
            return list(attr.data[index].color[:])
        elif data_type in ('INT32_2D', 'QUATERNION'):
            return list(attr.data[index].value[:])
        else:
            return [str(attr.data[index].value)]
    except Exception:
        # Return empty values based on expected column count
        return _get_empty_values(attr.data_type)


def _get_empty_values(data_type):
    """Return empty placeholder values for a given data type."""
    if data_type in ('FLOAT', 'INT', 'INT8', 'INT_8', 'BOOLEAN', 'STRING'):
        return ['']
    elif data_type == 'FLOAT_VECTOR':
        return ['', '', '']
    elif data_type in ('FLOAT_COLOR', 'BYTE_COLOR'):
        return ['', '', '', '']
    elif data_type in ('FLOAT2', 'INT32_2D'):
        return ['', '']
    elif data_type == 'QUATERNION':
        return ['', '', '', '']
    return ['']


# ============================================================================
# LEGACY CURVE EXPORT (for native CURVE objects)
# ============================================================================

def export_legacy_splines_to_csv(curve_data, output_dir, obj_name):
    """Export spline-level metadata for legacy Curve objects."""
    
    if not hasattr(curve_data, 'splines'):
        return None
    
    csv_path = get_next_csv_path(output_dir, f"{obj_name}_splines")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        header = [
            "spline_index",
            "type",
            "point_count",
            "use_cyclic_u",
            "resolution_u",
            "tilt_interpolation",
            "radius_interpolation",
        ]
        writer.writerow(header)
        
        for i, spline in enumerate(curve_data.splines):
            point_count = len(spline.bezier_points) if spline.type == 'BEZIER' else len(spline.points)
            
            row = [
                i,
                spline.type,
                point_count,
                spline.use_cyclic_u,
                spline.resolution_u,
                spline.tilt_interpolation,
                spline.radius_interpolation,
            ]
            writer.writerow(row)
    
    return csv_path


def export_legacy_bezier_points_to_csv(curve_data, output_dir, obj_name):
    """Export Bezier control point data for legacy Curve objects."""
    
    if not hasattr(curve_data, 'splines'):
        return None
    
    has_bezier = any(s.type == 'BEZIER' for s in curve_data.splines)
    if not has_bezier:
        return None
    
    csv_path = get_next_csv_path(output_dir, f"{obj_name}_bezier_points")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        header = [
            "spline_index",
            "point_index",
            "co.x", "co.y", "co.z",
            "handle_left.x", "handle_left.y", "handle_left.z",
            "handle_right.x", "handle_right.y", "handle_right.z",
            "handle_left_type",
            "handle_right_type",
            "radius",
            "tilt",
        ]
        writer.writerow(header)
        
        for spline_idx, spline in enumerate(curve_data.splines):
            if spline.type != 'BEZIER':
                continue
                
            for pt_idx, pt in enumerate(spline.bezier_points):
                row = [
                    spline_idx,
                    pt_idx,
                    *format_vector(pt.co),
                    *format_vector(pt.handle_left),
                    *format_vector(pt.handle_right),
                    pt.handle_left_type,
                    pt.handle_right_type,
                    pt.radius,
                    pt.tilt,
                ]
                writer.writerow(row)
    
    return csv_path


def export_legacy_nurbs_poly_points_to_csv(curve_data, output_dir, obj_name):
    """Export NURBS/Poly control point data for legacy Curve objects."""
    
    if not hasattr(curve_data, 'splines'):
        return None
    
    has_nurbs_poly = any(s.type != 'BEZIER' for s in curve_data.splines)
    if not has_nurbs_poly:
        return None
    
    csv_path = get_next_csv_path(output_dir, f"{obj_name}_nurbs_poly_points")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        header = [
            "spline_index",
            "point_index",
            "co.x", "co.y", "co.z", "co.w",
            "radius",
            "tilt",
        ]
        writer.writerow(header)
        
        for spline_idx, spline in enumerate(curve_data.splines):
            if spline.type == 'BEZIER':
                continue
                
            for pt_idx, pt in enumerate(spline.points):
                row = [
                    spline_idx,
                    pt_idx,
                    *format_vector(pt.co),
                    pt.radius,
                    pt.tilt,
                ]
                writer.writerow(row)
    
    return csv_path


# ============================================================================
# OPERATOR
# ============================================================================

@procedural_operator
class CURVE_OT_export_curve_to_csv(Operator):
    """Export curve data from evaluated geometry (including geometry nodes output) to CSV"""
    
    bl_idname = "curve.export_curve_to_csv"
    bl_label = "Export Curve to CSV"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}
        
        output_dir = get_tmp_base_dir()
        created_files = []
        obj_name = obj.name.replace(" ", "_").replace(".", "_")
        
        # Get evaluated curves data
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        eval_data = eval_obj.data
        
        try:
            # Check what type of data we have
            is_new_curves_api = hasattr(eval_data, 'curves') and hasattr(eval_data, 'points')
            is_legacy_curve = hasattr(eval_data, 'splines')
            
            if is_new_curves_api:
                # New Curves API (geometry nodes output, CURVES object type)
                self.report({'INFO'}, "Exporting using new Curves API...")
                files = export_curves_geometry_to_csv(eval_data, output_dir, obj_name)
                created_files.extend(files)
                
            elif is_legacy_curve:
                # Legacy Curve API (native CURVE objects)
                self.report({'INFO'}, "Exporting using legacy Curve API...")
                
                csv_path = export_legacy_splines_to_csv(eval_data, output_dir, obj_name)
                if csv_path:
                    created_files.append(csv_path)
                
                csv_path = export_legacy_bezier_points_to_csv(eval_data, output_dir, obj_name)
                if csv_path:
                    created_files.append(csv_path)
                
                csv_path = export_legacy_nurbs_poly_points_to_csv(eval_data, output_dir, obj_name)
                if csv_path:
                    created_files.append(csv_path)
            
            else:
                self.report({'ERROR'}, f"Object '{obj.name}' has no curve data in evaluated geometry")
                return {'CANCELLED'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}
        
        if not created_files:
            self.report({'WARNING'}, "No curve data found to export")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"Exported {len(created_files)} CSV files to {output_dir}")
        return {'FINISHED'}
