"""
Export Curve/Spline Data to CSV

This script exports all spline and control point data from the active curve object
to CSV files in the tmp folder. It captures:
- Spline metadata (type, point count, cyclic, resolution, etc.)
- Control point data (position, handles, radius, tilt, weight)
- All custom attributes on the curve

Run this script in Blender's Python console or Text Editor with a curve object selected.
"""

import bpy
import csv
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Output directory (defaults to same folder as this script)
OUTPUT_DIR = Path(__file__).parent

# Whether to export the evaluated (post-modifier) curve
USE_EVALUATED = True

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_tmp_dir():
    """Get the tmp directory for exports."""
    return OUTPUT_DIR


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
    """Format a vector as separate x, y, z values."""
    return list(vec[:])


# ============================================================================
# MAIN EXPORT FUNCTIONS
# ============================================================================

def export_splines_to_csv(curve_obj, output_dir):
    """Export spline-level metadata to CSV."""
    
    if curve_obj.type != 'CURVE':
        raise ValueError(f"Object '{curve_obj.name}' is not a curve (type: {curve_obj.type})")
    
    curve_data = curve_obj.data
    
    csv_path = get_next_csv_path(output_dir, "splines")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        header = [
            "spline_index",
            "type",
            "point_count",
            "use_cyclic_u",
            "use_bezier_u",
            "use_endpoint_u",
            "resolution_u",
            "order_u",
            "tilt_interpolation",
            "radius_interpolation",
        ]
        writer.writerow(header)
        
        # Data rows
        for i, spline in enumerate(curve_data.splines):
            point_count = len(spline.bezier_points) if spline.type == 'BEZIER' else len(spline.points)
            
            row = [
                i,
                spline.type,
                point_count,
                spline.use_cyclic_u,
                spline.use_bezier_u if hasattr(spline, 'use_bezier_u') else '',
                spline.use_endpoint_u if hasattr(spline, 'use_endpoint_u') else '',
                spline.resolution_u,
                spline.order_u if hasattr(spline, 'order_u') else '',
                spline.tilt_interpolation,
                spline.radius_interpolation,
            ]
            writer.writerow(row)
    
    print(f"Exported spline metadata to: {csv_path}")
    return csv_path


def export_bezier_points_to_csv(curve_obj, output_dir):
    """Export Bezier control point data to CSV."""
    
    curve_data = curve_obj.data
    
    csv_path = get_next_csv_path(output_dir, "bezier_points")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
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
            "weight",
        ]
        writer.writerow(header)
        
        # Data rows
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
                    pt.weight_softbody,
                ]
                writer.writerow(row)
    
    print(f"Exported Bezier points to: {csv_path}")
    return csv_path


def export_nurbs_poly_points_to_csv(curve_obj, output_dir):
    """Export NURBS/Poly control point data to CSV."""
    
    curve_data = curve_obj.data
    
    csv_path = get_next_csv_path(output_dir, "nurbs_poly_points")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header (NURBS/Poly points use 4D coordinates with weight as w)
        header = [
            "spline_index",
            "point_index",
            "co.x", "co.y", "co.z", "co.w",
            "radius",
            "tilt",
            "weight_softbody",
        ]
        writer.writerow(header)
        
        # Data rows
        for spline_idx, spline in enumerate(curve_data.splines):
            if spline.type == 'BEZIER':
                continue
                
            for pt_idx, pt in enumerate(spline.points):
                row = [
                    spline_idx,
                    pt_idx,
                    *format_vector(pt.co),  # This includes w for NURBS
                    pt.radius,
                    pt.tilt,
                    pt.weight_softbody,
                ]
                writer.writerow(row)
    
    print(f"Exported NURBS/Poly points to: {csv_path}")
    return csv_path


def export_evaluated_curve_to_csv(curve_obj, output_dir):
    """
    Export evaluated curve data using the new Curves API.
    This exports the actual geometry after modifiers are applied.
    """
    
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = curve_obj.evaluated_get(depsgraph)
    
    # Convert to curves (new Blender 3.x+ API)
    # This gives us access to all attributes
    try:
        curves = eval_obj.to_curve(depsgraph, apply_modifiers=True)
    except:
        # Fallback for older API
        curves = eval_obj.data
    
    # Export curve-level attributes (per-curve data)
    csv_path_curves = get_next_csv_path(output_dir, "curve_attributes")
    
    # Collect all attribute names and their data types
    attr_info = {}
    if hasattr(curves, 'attributes'):
        for attr in curves.attributes:
            attr_info[attr.name] = {
                'data_type': attr.data_type,
                'domain': attr.domain
            }
    
    # Separate by domain
    point_attrs = {k: v for k, v in attr_info.items() if v['domain'] == 'POINT'}
    curve_attrs = {k: v for k, v in attr_info.items() if v['domain'] == 'CURVE'}
    
    # Export point-domain attributes
    if point_attrs:
        csv_path_points = get_next_csv_path(output_dir, "point_attributes")
        export_attributes_to_csv(curves, point_attrs, csv_path_points, 'POINT')
    
    # Export curve-domain attributes  
    if curve_attrs:
        csv_path_curves = get_next_csv_path(output_dir, "curve_domain_attributes")
        export_attributes_to_csv(curves, curve_attrs, csv_path_curves, 'CURVE')
    
    return csv_path_curves if curve_attrs else None


def export_attributes_to_csv(data, attr_info, csv_path, domain):
    """Export attributes of a specific domain to CSV."""
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Build header
        header = ["index"]
        for attr_name, info in attr_info.items():
            data_type = info['data_type']
            if data_type in ('FLOAT', 'INT', 'INT_8', 'BOOLEAN', 'STRING'):
                header.append(attr_name)
            elif data_type == 'FLOAT_VECTOR':
                header.extend([f"{attr_name}.x", f"{attr_name}.y", f"{attr_name}.z"])
            elif data_type in ('FLOAT_COLOR', 'BYTE_COLOR'):
                header.extend([f"{attr_name}.r", f"{attr_name}.g", f"{attr_name}.b", f"{attr_name}.a"])
            elif data_type in ('FLOAT2', 'INT32_2D'):
                header.extend([f"{attr_name}.x", f"{attr_name}.y"])
            elif data_type == 'QUATERNION':
                header.extend([f"{attr_name}.w", f"{attr_name}.x", f"{attr_name}.y", f"{attr_name}.z"])
        
        writer.writerow(header)
        
        # Determine domain size
        if domain == 'POINT':
            if hasattr(data, 'points'):
                count = len(data.points)
            elif hasattr(data, 'vertices'):
                count = len(data.vertices)
            else:
                count = 0
        elif domain == 'CURVE':
            if hasattr(data, 'curves'):
                count = len(data.curves)
            elif hasattr(data, 'splines'):
                count = len(data.splines)
            else:
                count = 0
        else:
            count = 0
        
        # Get attribute data
        attrs = {name: data.attributes[name] for name in attr_info.keys() if name in data.attributes}
        
        # Write rows
        for i in range(count):
            row = [i]
            for attr_name, info in attr_info.items():
                if attr_name not in attrs:
                    # Add empty values
                    data_type = info['data_type']
                    if data_type in ('FLOAT', 'INT', 'INT_8', 'BOOLEAN', 'STRING'):
                        row.append('')
                    elif data_type == 'FLOAT_VECTOR':
                        row.extend(['', '', ''])
                    elif data_type in ('FLOAT_COLOR', 'BYTE_COLOR'):
                        row.extend(['', '', '', ''])
                    elif data_type in ('FLOAT2', 'INT32_2D'):
                        row.extend(['', ''])
                    elif data_type == 'QUATERNION':
                        row.extend(['', '', '', ''])
                    continue
                
                attr = attrs[attr_name]
                data_type = info['data_type']
                
                try:
                    if data_type in ('FLOAT', 'INT', 'INT_8', 'BOOLEAN', 'STRING'):
                        row.append(attr.data[i].value)
                    elif data_type in ('FLOAT_VECTOR', 'FLOAT2'):
                        row.extend(attr.data[i].vector[:])
                    elif data_type in ('FLOAT_COLOR', 'BYTE_COLOR'):
                        row.extend(attr.data[i].color[:])
                    elif data_type in ('INT32_2D', 'QUATERNION'):
                        row.extend(attr.data[i].value[:])
                except Exception as e:
                    print(f"Error reading attribute {attr_name}[{i}]: {e}")
                    # Add placeholder values
                    if data_type in ('FLOAT', 'INT', 'INT_8', 'BOOLEAN', 'STRING'):
                        row.append('')
                    elif data_type == 'FLOAT_VECTOR':
                        row.extend(['', '', ''])
                    elif data_type in ('FLOAT_COLOR', 'BYTE_COLOR'):
                        row.extend(['', '', '', ''])
                    elif data_type in ('FLOAT2', 'INT32_2D'):
                        row.extend(['', ''])
                    elif data_type == 'QUATERNION':
                        row.extend(['', '', '', ''])
            
            writer.writerow(row)
    
    print(f"Exported {domain} attributes to: {csv_path}")


def export_all_curve_data(curve_obj=None, output_dir=None):
    """
    Main export function - exports all curve data to CSV files.
    
    Args:
        curve_obj: The curve object to export (defaults to active object)
        output_dir: Output directory (defaults to tmp folder)
    
    Returns:
        List of paths to created CSV files
    """
    
    if curve_obj is None:
        curve_obj = bpy.context.active_object
    
    if curve_obj is None:
        raise ValueError("No active object selected")
    
    if curve_obj.type != 'CURVE':
        raise ValueError(f"Active object '{curve_obj.name}' is not a curve (type: {curve_obj.type})")
    
    if output_dir is None:
        output_dir = get_tmp_dir()
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Exporting curve data for: {curve_obj.name}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    created_files = []
    
    # 1. Export spline metadata
    csv_path = export_splines_to_csv(curve_obj, output_dir)
    created_files.append(csv_path)
    
    # 2. Export Bezier points (if any Bezier splines exist)
    has_bezier = any(s.type == 'BEZIER' for s in curve_obj.data.splines)
    if has_bezier:
        csv_path = export_bezier_points_to_csv(curve_obj, output_dir)
        created_files.append(csv_path)
    
    # 3. Export NURBS/Poly points (if any non-Bezier splines exist)
    has_nurbs_poly = any(s.type != 'BEZIER' for s in curve_obj.data.splines)
    if has_nurbs_poly:
        csv_path = export_nurbs_poly_points_to_csv(curve_obj, output_dir)
        created_files.append(csv_path)
    
    # 4. Export evaluated curve attributes (if using new Curves API)
    if USE_EVALUATED:
        try:
            export_evaluated_curve_to_csv(curve_obj, output_dir)
        except Exception as e:
            print(f"Note: Could not export evaluated curve attributes: {e}")
    
    print(f"\n{'='*60}")
    print(f"Export complete! Created {len(created_files)} CSV files.")
    print(f"{'='*60}\n")
    
    return created_files


# ============================================================================
# RUN EXPORT
# ============================================================================

if __name__ == "__main__":
    export_all_curve_data()

