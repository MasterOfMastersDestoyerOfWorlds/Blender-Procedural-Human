"""
Utilities for creating and managing profile curves for finger segments.
"""

import bpy
from mathutils import Vector
from .finger_segment_profiles import ProfileType, SegmentType, get_profile_data


def create_profile_curve_from_data(name, profile_data, segment_length=1.0, base_radius=1.0):
    """
    Create a Blender bezier curve from profile data.
    
    The profile data is normalized (0-1 along length), this function scales it
    to the actual segment length and base radius.
    
    Args:
        name: Name for the curve object
        profile_data: Dictionary containing 'points' list with curve data
        segment_length: Length of the segment to scale the curve
        base_radius: Base radius to scale the radius values
        
    Returns:
        Blender curve object
    """
    # Create curve data
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    
    # Create spline
    spline = curve_data.splines.new('BEZIER')
    points = profile_data["points"]
    spline.bezier_points.add(len(points) - 1)  # Already has 1 point
    
    # Set point data
    for i, point_data in enumerate(points):
        point = spline.bezier_points[i]
        
        # Scale coordinates by segment length
        co = point_data["co"]
        point.co = Vector((co[0], co[1], co[2] * segment_length))
        
        # Scale handles by segment length
        handle_left = point_data["handle_left"]
        handle_right = point_data["handle_right"]
        point.handle_left = point.co + Vector((handle_left[0], handle_left[1], handle_left[2] * segment_length))
        point.handle_right = point.co + Vector((handle_right[0], handle_right[1], handle_right[2] * segment_length))
        
        # Set handle types
        point.handle_left_type = point_data.get("handle_left_type", "AUTO")
        point.handle_right_type = point_data.get("handle_right_type", "AUTO")
    
    # Create object
    curve_obj = bpy.data.objects.new(name, curve_data)
    
    return curve_obj


def extract_profile_curve_data(curve_object):
    """
    Extract profile data from a Blender curve object and format as Python code.
    
    This allows you to edit curves in Blender and save them back to code.
    
    Args:
        curve_object: Blender curve object
        
    Returns:
        Dictionary with profile data, and string with formatted Python code
    """
    if curve_object.type != 'CURVE':
        raise ValueError("Object must be a curve")
    
    curve_data = curve_object.data
    
    # Get the first spline (assuming single spline curves)
    if len(curve_data.splines) == 0:
        raise ValueError("Curve has no splines")
    
    spline = curve_data.splines[0]
    
    if spline.type != 'BEZIER':
        raise ValueError("Spline must be BEZIER type")
    
    # Extract points
    points = []
    for point in spline.bezier_points:
        point_data = {
            "co": tuple(point.co),
            "handle_left": tuple(point.handle_left - point.co),
            "handle_right": tuple(point.handle_right - point.co),
            "handle_left_type": point.handle_left_type,
            "handle_right_type": point.handle_right_type,
        }
        points.append(point_data)
    
    profile_data = {"points": points}
    
    # Format as Python code
    python_code = format_profile_data_as_code(profile_data, curve_object.name)
    
    return profile_data, python_code


def format_profile_data_as_code(profile_data, variable_name="PROFILE_DATA"):
    """
    Format profile data as copy-pasteable Python code.
    
    Args:
        profile_data: Dictionary with profile data
        variable_name: Name for the variable in generated code
        
    Returns:
        String with formatted Python code
    """
    lines = [f"{variable_name} = {{"]
    lines.append('    "points": [')
    
    for i, point in enumerate(profile_data["points"]):
        lines.append("        {")
        lines.append(f'            "co": {point["co"]},')
        lines.append(f'            "handle_left": {point["handle_left"]},')
        lines.append(f'            "handle_right": {point["handle_right"]},')
        lines.append(f'            "handle_left_type": "{point["handle_left_type"]}",')
        lines.append(f'            "handle_right_type": "{point["handle_right_type"]}",')
        
        if i < len(profile_data["points"]) - 1:
            lines.append("        },")
        else:
            lines.append("        }")
    
    lines.append("    ]")
    lines.append("}")
    
    return "\n".join(lines)


def get_default_profile_curve(segment_type: SegmentType, profile_type: ProfileType, segment_length=1.0, base_radius=1.0):
    """
    Get a default profile curve for a given segment and profile type.
    
    Args:
        segment_type: SegmentType enum
        profile_type: ProfileType enum
        segment_length: Length of the segment
        base_radius: Base radius of the segment
        
    Returns:
        Blender curve object
    """
    profile_data = get_profile_data(segment_type, profile_type)
    
    name = f"{segment_type.value}_{profile_type.value}"
    
    return create_profile_curve_from_data(name, profile_data, segment_length, base_radius)


def normalize_profile_curve(curve_object, segment_length=1.0):
    """
    Normalize a profile curve to 0-1 range for storage.
    
    Args:
        curve_object: Blender curve object
        segment_length: Original segment length to normalize by
        
    Returns:
        Normalized profile data dictionary
    """
    profile_data, _ = extract_profile_curve_data(curve_object)
    
    # Normalize coordinates
    for point in profile_data["points"]:
        co = list(point["co"])
        co[2] = co[2] / segment_length if segment_length > 0 else co[2]
        point["co"] = tuple(co)
        
        # Normalize handles
        handle_left = list(point["handle_left"])
        handle_left[2] = handle_left[2] / segment_length if segment_length > 0 else handle_left[2]
        point["handle_left"] = tuple(handle_left)
        
        handle_right = list(point["handle_right"])
        handle_right[2] = handle_right[2] / segment_length if segment_length > 0 else handle_right[2]
        point["handle_right"] = tuple(handle_right)
    
    return profile_data


__all__ = [
    "create_profile_curve_from_data",
    "extract_profile_curve_data",
    "format_profile_data_as_code",
    "get_default_profile_curve",
    "normalize_profile_curve",
]


