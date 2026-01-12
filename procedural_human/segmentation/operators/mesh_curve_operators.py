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
    
    # Center the contour
    center = contour.mean(axis=0)
    centered = contour - center
    
    # Scale to target height
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
    
    # Ensure top comes before bottom in the index order
    if top_idx > bottom_idx:
        top_idx, bottom_idx = bottom_idx, top_idx
    
    # Left half: from top to bottom going one way
    left_half = contour[top_idx:bottom_idx + 1]
    
    # Right half: from bottom back to top going the other way
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
    
    # Compute cumulative arc length
    diffs = np.diff(contour, axis=0)
    segment_lengths = np.sqrt((diffs ** 2).sum(axis=1))
    cumulative = np.zeros(len(contour))
    cumulative[1:] = np.cumsum(segment_lengths)
    total_length = cumulative[-1]
    
    if total_length == 0:
        return contour[:num_points] if len(contour) >= num_points else contour
    
    # Generate evenly spaced parameter values
    target_lengths = np.linspace(0, total_length, num_points)
    
    # Interpolate
    resampled = np.zeros((num_points, 2))
    for i, t in enumerate(target_lengths):
        # Find segment containing t
        idx = np.searchsorted(cumulative, t) - 1
        idx = max(0, min(idx, len(contour) - 2))
        
        # Interpolate within segment
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
    - Two shared vertices (top and bottom extrema)
    - Two edge loops (front and side view contours)
    - Two N-gon faces (one per loop)
    
    Args:
        front_contour: Front view contour (Nx2 in XY plane)
        side_contour: Side view contour (Mx2 in YZ plane)
        name: Name for the mesh object
        points_per_half: Number of points per half-loop (excluding shared vertices)
        
    Returns:
        The created Blender mesh object
    """
    # Normalize contours
    front_norm = normalize_contour(front_contour)
    side_norm = normalize_contour(side_contour)
    
    # Find extrema
    front_top, front_bottom = find_extrema_indices(front_norm)
    side_top, side_bottom = find_extrema_indices(side_norm)
    
    # Split contours at extrema
    front_left, front_right = split_contour_at_extrema(front_norm, front_top, front_bottom)
    side_left, side_right = split_contour_at_extrema(side_norm, side_top, side_bottom)
    
    # Resample each half to same number of points
    front_left_rs = resample_contour(front_left, points_per_half + 2)
    front_right_rs = resample_contour(front_right, points_per_half + 2)
    side_left_rs = resample_contour(side_left, points_per_half + 2)
    side_right_rs = resample_contour(side_right, points_per_half + 2)
    
    # Get shared top and bottom positions (average of all contour extrema)
    top_y = (front_norm[front_top, 1] + side_norm[side_top, 1]) / 2
    bottom_y = (front_norm[front_bottom, 1] + side_norm[side_bottom, 1]) / 2
    
    # Create BMesh
    bm = bmesh.new()
    
    # Create shared vertices at top and bottom
    # Top vertex at (0, top_y, 0)
    top_vert = bm.verts.new((0, top_y, 0))
    # Bottom vertex at (0, bottom_y, 0)
    bottom_vert = bm.verts.new((0, bottom_y, 0))
    
    # Create front loop vertices (in XY plane, Z=0)
    # Exclude first and last points (shared vertices)
    front_verts = [top_vert]
    for i in range(1, len(front_left_rs) - 1):
        x, y = front_left_rs[i]
        v = bm.verts.new((x, y, 0))
        front_verts.append(v)
    front_verts.append(bottom_vert)
    for i in range(1, len(front_right_rs) - 1):
        x, y = front_right_rs[i]
        v = bm.verts.new((x, y, 0))
        front_verts.append(v)
    # Close the loop back to top
    front_verts.append(top_vert)
    
    # Create side loop vertices (in YZ plane, X=0)
    # Exclude first and last points (shared vertices)
    side_verts = [top_vert]
    for i in range(1, len(side_left_rs) - 1):
        x, y = side_left_rs[i]  # x becomes Z, y stays Y
        v = bm.verts.new((0, y, x))
        side_verts.append(v)
    side_verts.append(bottom_vert)
    for i in range(1, len(side_right_rs) - 1):
        x, y = side_right_rs[i]
        v = bm.verts.new((0, y, x))
        side_verts.append(v)
    # Close the loop back to top
    side_verts.append(top_vert)
    
    bm.verts.ensure_lookup_table()
    
    # Create front face (all verts except the duplicate at end)
    front_face_verts = front_verts[:-1]  # Remove duplicate top_vert at end
    if len(front_face_verts) >= 3:
        try:
            front_face = bm.faces.new(front_face_verts)
        except ValueError as e:
            logger.warning(f"Could not create front face: {e}")
    
    # Create side face (all verts except the duplicate at end)
    side_face_verts = side_verts[:-1]  # Remove duplicate top_vert at end
    if len(side_face_verts) >= 3:
        try:
            side_face = bm.faces.new(side_face_verts)
        except ValueError as e:
            logger.warning(f"Could not create side face: {e}")
    
    # Create mesh data
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    
    # Create object
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    return obj


def apply_bezier_handles(obj: bpy.types.Object):
    """
    Calculate and apply Bezier handles to mesh edges.
    
    Args:
        obj: Blender mesh object
    """
    from procedural_human.gizmo.mesh_curves_gizmo import (
        calculate_auto_handles_bmesh,
        ensure_edge_layers,
    )
    
    # Enter edit mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Get BMesh
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Ensure layers exist
    ensure_edge_layers(bm)
    
    # Calculate auto handles
    calculate_auto_handles_bmesh(bm)
    
    # Update mesh
    bmesh.update_edit_mesh(obj.data)
    
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')


def apply_coons_patch_modifier(obj: bpy.types.Object, subdivisions: int = 4):
    """
    Apply the CoonNGonPatchGenerator geometry nodes modifier.
    
    Args:
        obj: Blender mesh object
        subdivisions: Number of subdivisions for patch generation
    """
    from procedural_human.geo_node_groups.charrot_gregory_patch import create_charrot_gregory_group
    
    # Get or create the node group
    node_group = create_charrot_gregory_group()
    
    # Add modifier
    modifier = obj.modifiers.new(name="CoonPatch", type='NODES')
    modifier.node_group = node_group
    
    # Set subdivisions (Input_2 based on the interface)
    # Find the subdivisions input
    for item in node_group.interface.items_tree:
        if item.name == "Subdivisions":
            # Set via identifier
            modifier[item.identifier] = subdivisions
            break


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
            # Use convex hull if available and requested
            if self.use_convex_hull and side_hull is not None:
                side_to_use = side_hull
                logger.info(f"Using convex hull ({len(side_hull)} points) for side contour")
            else:
                side_to_use = side_contour
            
            # Create the mesh
            obj = create_dual_loop_mesh(
                front_contour,
                side_to_use,
                name="DualContourMesh",
                points_per_half=self.points_per_half,
            )
            
            logger.info(f"Created dual mesh: {obj.name}")
            
            # Apply Bezier handles
            if self.apply_handles:
                try:
                    apply_bezier_handles(obj)
                    logger.info("Applied Bezier handles")
                except Exception as e:
                    logger.warning(f"Could not apply Bezier handles: {e}")
            
            # Apply Coons patch modifier
            if self.apply_coons_patch:
                try:
                    apply_coons_patch_modifier(obj, self.subdivisions)
                    logger.info(f"Applied Coons patch modifier (subdivisions={self.subdivisions})")
                except Exception as e:
                    logger.warning(f"Could not apply Coons patch: {e}")
            
            # Select the new object
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
        # Generate test contours: circle for front, ellipse for side
        t = np.linspace(0, 2 * np.pi, 64, endpoint=False)
        
        # Circle for front view
        front = np.column_stack([np.cos(t) * 0.5, np.sin(t)])
        
        # Ellipse for side view (narrower)
        side = np.column_stack([np.cos(t) * 0.3, np.sin(t)])
        
        try:
            obj = create_dual_loop_mesh(
                front,
                side,
                name="TestDualMesh",
                points_per_half=self.points_per_half,
            )
            
            # Apply handles and Coons patch
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
