"""
Mesh Curve operators for creating dual-contour mesh objects.

Creates mesh objects with two edge loops (front and side view contours)
that share vertices at top and bottom, forming two N-gon faces suitable
for Coons patch surface generation.
"""

import bpy
import bmesh
import numpy as np
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty
from mathutils import Vector

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


def normalize_contour(contour: np.ndarray, target_height: float = 1.0) -> np.ndarray:
    """
    Normalize a contour to unit height centered at origin.
    
    Args:
        contour: Nx2 array of contour points
        target_height: Height to scale to
        
    Returns:
        Normalized contour array
    """
    if len(contour) == 0:
        return contour
    center = contour.mean(axis=0)
    centered = contour - center
    height = contour[:, 1].max() - contour[:, 1].min()
    if height > 0:
        scale = target_height / height
        centered *= scale
    
    return centered


def find_extrema_indices(contour: np.ndarray) -> tuple:
    """
    Find the indices of top and bottom extrema points in a contour.
    
    Args:
        contour: Nx2 array of contour points
        
    Returns:
        Tuple of (top_index, bottom_index)
    """
    top_idx = np.argmax(contour[:, 1])
    bottom_idx = np.argmin(contour[:, 1])
    return top_idx, bottom_idx


def find_axis_crossing_indices(contour: np.ndarray) -> tuple:
    """
    Find where a contour crosses the Y-axis (X=0) and return the segment indices
    and interpolated crossing points.
    
    For a closed contour centered on X, there should be exactly 2 crossings:
    one where the contour goes from negative X to positive X, and one where
    it goes from positive X to negative X.
    
    Args:
        contour: Nx2 array of contour points (should be centered on X=0)
        
    Returns:
        Tuple of ((idx1, point1), (idx2, point2)) where:
        - idx is the segment index (crossing occurs between contour[idx] and contour[idx+1])
        - point is the interpolated (0, y) crossing point
        Crossings are sorted so the first has higher Y (top) and second has lower Y (bottom).
    """
    crossings = []
    n = len(contour)
    
    for i in range(n):
        p1 = contour[i]
        p2 = contour[(i + 1) % n]
        
        x1, y1 = p1
        x2, y2 = p2
        if (x1 < 0 < x2) or (x2 < 0 < x1):
            t = -x1 / (x2 - x1)
            y_crossing = y1 + t * (y2 - y1)
            crossings.append((i, (0.0, y_crossing), t))
    
    if len(crossings) < 2:
        top_idx = np.argmax(contour[:, 1])
        bottom_idx = np.argmin(contour[:, 1])
        return (
            (top_idx, (0.0, contour[top_idx, 1]), 0.0),
            (bottom_idx, (0.0, contour[bottom_idx, 1]), 0.0)
        )
    crossings.sort(key=lambda c: c[1][1], reverse=True)
    top_crossing = crossings[0]
    bottom_crossing = crossings[-1]
    
    return top_crossing, bottom_crossing


def split_contour_at_crossings(contour: np.ndarray, top_crossing: tuple, bottom_crossing: tuple) -> tuple:
    """
    Split a contour into two halves at the X=0 crossing points.
    
    Each half starts at the TOP crossing point and ends at the BOTTOM crossing point.
    The two halves traverse the contour in opposite directions.
    
    Args:
        contour: Nx2 array of contour points
        top_crossing: (segment_idx, (x, y), t) for top crossing (higher Y)
        bottom_crossing: (segment_idx, (x, y), t) for bottom crossing (lower Y)
        
    Returns:
        Tuple of (half1, half2) arrays, each starting at top and ending at bottom.
    """
    n = len(contour)
    top_idx, top_point, _ = top_crossing
    bottom_idx, bottom_point, _ = bottom_crossing
    half1_points = [top_point]
    i = (top_idx + 1) % n
    while i != (bottom_idx + 1) % n:
        half1_points.append(tuple(contour[i]))
        i = (i + 1) % n
    half1_points.append(bottom_point)
    half2_points = [top_point]
    i = top_idx
    while i != bottom_idx:
        half2_points.append(tuple(contour[i]))
        i = (i - 1) % n
    half2_points.append(bottom_point)
    
    return np.array(half1_points), np.array(half2_points)


def split_contour_at_extrema(contour: np.ndarray, top_idx: int, bottom_idx: int) -> tuple:
    """
    Split a contour into two halves at the top and bottom extrema.
    
    Args:
        contour: Nx2 array of contour points
        top_idx: Index of top extremum
        bottom_idx: Index of bottom extremum
        
    Returns:
        Tuple of (left_half, right_half) arrays, each including both extrema
    """
    n = len(contour)
    if top_idx > bottom_idx:
        top_idx, bottom_idx = bottom_idx, top_idx
    left_half = contour[top_idx:bottom_idx + 1]
    right_half = np.vstack([contour[bottom_idx:], contour[:top_idx + 1]])
    
    return left_half, right_half


def resample_contour(contour: np.ndarray, num_points: int) -> np.ndarray:
    """
    Resample a contour to have a specific number of points.
    
    Args:
        contour: Nx2 array of contour points
        num_points: Number of points in output
        
    Returns:
        Resampled contour with num_points points
    """
    if len(contour) < 2:
        return contour
    diffs = np.diff(contour, axis=0)
    segment_lengths = np.sqrt((diffs ** 2).sum(axis=1))
    cumulative = np.zeros(len(contour))
    cumulative[1:] = np.cumsum(segment_lengths)
    total_length = cumulative[-1]
    
    if total_length == 0:
        return contour[:num_points] if len(contour) >= num_points else contour
    target_lengths = np.linspace(0, total_length, num_points)
    resampled = np.zeros((num_points, 2))
    for i, t in enumerate(target_lengths):
        idx = np.searchsorted(cumulative, t) - 1
        idx = max(0, min(idx, len(contour) - 2))
        seg_start = cumulative[idx]
        seg_length = segment_lengths[idx] if idx < len(segment_lengths) else 0
        
        if seg_length > 0:
            alpha = (t - seg_start) / seg_length
        else:
            alpha = 0
        
        resampled[i] = contour[idx] * (1 - alpha) + contour[idx + 1] * alpha
    
    return resampled


def create_dual_loop_mesh(
    front_contour: np.ndarray,
    side_contour: np.ndarray,
    name: str = "DualContourMesh",
    points_per_half: int = 16,
) -> bpy.types.Object:
    """
    Create a mesh with two edge loops sharing top and bottom vertices.
    
    The mesh has:
    - Two shared vertices (poles) where both contours cross X=0
    - Two edge loops (front and side view contours)
    - Two N-gon faces (one per loop)
    
    The poles are found by locating where each contour crosses the Y-axis (X=0),
    which is where the front (XY plane) and side (YZ plane) views intersect.
    
    Args:
        front_contour: Front view contour (Nx2 in XY plane)
        side_contour: Side view contour (Mx2 in YZ plane)
        name: Name for the mesh object
        points_per_half: Number of points per half-loop (excluding shared vertices)
        
    Returns:
        The created Blender mesh object
    """
    front_norm = normalize_contour(front_contour)
    side_norm = normalize_contour(side_contour)
    front_top_cross, front_bottom_cross = find_axis_crossing_indices(front_norm)
    side_top_cross, side_bottom_cross = find_axis_crossing_indices(side_norm)
    top_y = (front_top_cross[1][1] + side_top_cross[1][1]) / 2
    bottom_y = (front_bottom_cross[1][1] + side_bottom_cross[1][1]) / 2
    
    logger.info(f"Pole positions: top_y={top_y:.3f}, bottom_y={bottom_y:.3f}")
    front_half1, front_half2 = split_contour_at_crossings(front_norm, front_top_cross, front_bottom_cross)
    side_half1, side_half2 = split_contour_at_crossings(side_norm, side_top_cross, side_bottom_cross)
    def get_dominant_x_sign(half):
        """Return -1 if half is mostly on left (X<0), +1 if mostly on right (X>0)"""
        mid_idx = len(half) // 2
        if mid_idx < len(half):
            return -1 if half[mid_idx, 0] < 0 else 1
        return 0
    
    if get_dominant_x_sign(front_half1) < 0:
        front_left, front_right = front_half1, front_half2
    else:
        front_left, front_right = front_half2, front_half1
        
    if get_dominant_x_sign(side_half1) < 0:
        side_left, side_right = side_half1, side_half2
    else:
        side_left, side_right = side_half2, side_half1
    front_left_rs = resample_contour(front_left, points_per_half + 2)
    front_right_rs = resample_contour(front_right, points_per_half + 2)
    side_left_rs = resample_contour(side_left, points_per_half + 2)
    side_right_rs = resample_contour(side_right, points_per_half + 2)
    bm = bmesh.new()
    top_vert = bm.verts.new((0, top_y, 0))
    bottom_vert = bm.verts.new((0, bottom_y, 0))
    front_left_verts = []
    for i in range(1, len(front_left_rs) - 1):
        x, y = front_left_rs[i]
        v = bm.verts.new((x, y, 0))
        front_left_verts.append(v)
    front_right_verts = []
    for i in range(1, len(front_right_rs) - 1):
        x, y = front_right_rs[i]
        v = bm.verts.new((x, y, 0))
        front_right_verts.append(v)
    side_left_verts = []
    for i in range(1, len(side_left_rs) - 1):
        x, y = side_left_rs[i]  # x becomes Z, y stays Y
        v = bm.verts.new((0, y, x))
        side_left_verts.append(v)
    side_right_verts = []
    for i in range(1, len(side_right_rs) - 1):
        x, y = side_right_rs[i]
        v = bm.verts.new((0, y, x))
        side_right_verts.append(v)
    
    bm.verts.ensure_lookup_table()
    q1_verts = [top_vert] + front_left_verts + [bottom_vert] + list(reversed(side_left_verts))
    if len(q1_verts) >= 3:
        try:
            bm.faces.new(q1_verts)
        except ValueError as e:
            logger.warning(f"Could not create quadrant 1 face: {e}")
    q2_verts = [top_vert] + side_right_verts + [bottom_vert] + list(reversed(front_left_verts))
    if len(q2_verts) >= 3:
        try:
            bm.faces.new(q2_verts)
        except ValueError as e:
            logger.warning(f"Could not create quadrant 2 face: {e}")
    q3_verts = [top_vert] + front_right_verts + [bottom_vert] + list(reversed(side_right_verts))
    if len(q3_verts) >= 3:
        try:
            bm.faces.new(q3_verts)
        except ValueError as e:
            logger.warning(f"Could not create quadrant 3 face: {e}")
    q4_verts = [top_vert] + side_left_verts + [bottom_vert] + list(reversed(front_right_verts))
    if len(q4_verts) >= 3:
        try:
            bm.faces.new(q4_verts)
        except ValueError as e:
            logger.warning(f"Could not create quadrant 4 face: {e}")
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    return obj


def apply_bezier_handles(obj: bpy.types.Object):
    """
    Calculate and apply Bezier handles to mesh edges.
    
    Args:
        obj: Blender mesh object
    """
    from procedural_human.gizmo.mesh_curves_operators import (
        calculate_auto_handles_bmesh,
        ensure_edge_layers,
    )
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    ensure_edge_layers(bm)
    calculate_auto_handles_bmesh(bm)
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')


def apply_coons_patch_modifier(obj: bpy.types.Object, subdivisions: int = 4, merge_by_distance: bool = True):
    """
    Apply the CoonNGonPatchGenerator geometry nodes modifier.
    
    The node group is created at addon startup by the @geo_node_group decorator.
    We just look it up by name rather than calling the creation function at runtime.
    
    Args:
        obj: Blender mesh object
        subdivisions: Number of subdivisions for patch generation
        merge_by_distance: Whether to merge vertices by distance (default True)
    """
    group_name = "CoonNGonPatchGenerator"
    node_group = bpy.data.node_groups.get(group_name)
    
    if node_group is None:
        logger.warning(f"Node group '{group_name}' not found, attempting to create...")
        try:
            from procedural_human.geo_node_groups.charrot_gregory_patch import create_charrot_gregory_group
            node_group = create_charrot_gregory_group()
        except Exception as e:
            logger.error(f"Failed to create node group: {e}")
            raise RuntimeError(f"CoonNGonPatchGenerator node group not available: {e}")
    modifier = obj.modifiers.new(name="CoonPatch", type='NODES')
    modifier.node_group = node_group
    for item in node_group.interface.items_tree:
        if item.name == "Subdivisions":
            modifier[item.identifier] = subdivisions
        elif item.name == "Merge By Distance":
            modifier[item.identifier] = merge_by_distance


@procedural_operator
class CreateDualMeshCurvesOperator(Operator):
    """Create a mesh with dual edge loops from front and side view contours"""
    
    bl_idname = "segmentation.create_dual_mesh_curves"
    bl_label = "Create Dual Mesh Curves"
    bl_description = "Create mesh with front/side edge loops sharing top/bottom vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    points_per_half: IntProperty(
        name="Points per Half",
        description="Number of vertices per half-loop (excluding shared vertices)",
        default=16,
        min=4,
        max=64
    )
    
    apply_handles: BoolProperty(
        name="Apply Bezier Handles",
        description="Calculate and apply Bezier handles to edges",
        default=True
    )
    
    apply_coons_patch: BoolProperty(
        name="Apply Coons Patch",
        description="Apply CoonNGonPatchGenerator modifier for smooth surface",
        default=True
    )
    
    subdivisions: IntProperty(
        name="Patch Subdivisions",
        description="Subdivisions for Coons patch surface",
        default=4,
        min=1,
        max=8
    )
    
    merge_by_distance: BoolProperty(
        name="Merge By Distance",
        description="Merge vertices at patch boundaries for smooth surface",
        default=True
    )
    
    use_convex_hull: BoolProperty(
        name="Use Convex Hull for Side",
        description="Use convex hull of side contour instead of full contour",
        default=True
    )
    
    def execute(self, context):
        from procedural_human.segmentation.operators.novel_view_operators import (
            get_front_contour,
            get_side_contour,
            get_side_convex_hull,
        )
        
        front_contour = get_front_contour()
        side_contour = get_side_contour()
        side_hull = get_side_convex_hull()
        
        if front_contour is None or len(front_contour) < 3:
            self.report({'WARNING'}, "No front contour available. Run novel view generation first.")
            return {'CANCELLED'}
        
        if side_contour is None or len(side_contour) < 3:
            self.report({'WARNING'}, "No side contour available. Run novel view generation first.")
            return {'CANCELLED'}
        
        try:
            if self.use_convex_hull and side_hull is not None:
                side_to_use = side_hull
                logger.info(f"Using convex hull ({len(side_hull)} points) for side contour")
            else:
                side_to_use = side_contour
            obj = create_dual_loop_mesh(
                front_contour,
                side_to_use,
                name="DualContourMesh",
                points_per_half=self.points_per_half,
            )
            
            logger.info(f"Created dual mesh: {obj.name}")
            if self.apply_handles:
                try:
                    apply_bezier_handles(obj)
                    logger.info("Applied Bezier handles")
                except Exception as e:
                    logger.warning(f"Could not apply Bezier handles: {e}")
            if self.apply_coons_patch:
                try:
                    apply_coons_patch_modifier(obj, self.subdivisions, self.merge_by_distance)
                    logger.info(f"Applied Coons patch modifier (subdivisions={self.subdivisions}, merge={self.merge_by_distance})")
                except Exception as e:
                    logger.warning(f"Could not apply Coons patch: {e}")
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            self.report({'INFO'}, f"Created dual contour mesh: {obj.name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to create dual mesh curves: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "points_per_half")
        layout.prop(self, "use_convex_hull")
        layout.separator()
        layout.prop(self, "apply_handles")
        layout.prop(self, "apply_coons_patch")
        if self.apply_coons_patch:
            layout.prop(self, "subdivisions")
            layout.prop(self, "merge_by_distance")


@procedural_operator
class CreateMeshCurvesFromContoursOperator(Operator):
    """Create mesh curves from manually provided contours (for testing)"""
    
    bl_idname = "segmentation.create_mesh_from_test_contours"
    bl_label = "Create Test Mesh Curves"
    bl_description = "Create dual mesh curves from simple test contours (circle and ellipse)"
    bl_options = {'REGISTER', 'UNDO'}
    
    points_per_half: IntProperty(
        name="Points per Half",
        description="Number of vertices per half-loop",
        default=16,
        min=4,
        max=64
    )
    
    def execute(self, context):
        t = np.linspace(0, 2 * np.pi, 64, endpoint=False)
        front = np.column_stack([np.cos(t) * 0.5, np.sin(t)])
        side = np.column_stack([np.cos(t) * 0.3, np.sin(t)])
        
        try:
            obj = create_dual_loop_mesh(
                front,
                side,
                name="TestDualMesh",
                points_per_half=self.points_per_half,
            )
            apply_bezier_handles(obj)
            apply_coons_patch_modifier(obj, subdivisions=4)
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            self.report({'INFO'}, f"Created test mesh: {obj.name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Test mesh creation failed: {e}")
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}


def apply_charrot_gregory_patch_modifier(obj: bpy.types.Object, subdivisions: int = 4, merge_by_distance: bool = True):
    """
    Apply the CharrotGregoryPatch geometry nodes modifier.
    
    Args:
        obj: Blender mesh object
        subdivisions: Number of subdivisions for patch generation
        merge_by_distance: Whether to merge vertices by distance (default True)
    """
    node_group = bpy.data.node_groups.get("CoonNGonPatchGenerator")
    
    if node_group is None:
        logger.warning("CharrotGregoryPatch node group not found, attempting to create...")
        try:
            from procedural_human.geo_node_groups.charrot_gregory_patch import create_charrot_gregory_group
            node_group = create_charrot_gregory_group()
        except Exception as e:
            logger.error(f"Failed to create CharrotGregoryPatch node group: {e}")
            raise RuntimeError(f"CharrotGregoryPatch node group not available: {e}")
    modifier = obj.modifiers.new(name="CharrotGregoryPatch", type='NODES')
    modifier.node_group = node_group
    for item in node_group.interface.items_tree:
        if item.name == "Subdivisions":
            modifier[item.identifier] = subdivisions
        elif item.name == "Merge By Distance":
            modifier[item.identifier] = merge_by_distance