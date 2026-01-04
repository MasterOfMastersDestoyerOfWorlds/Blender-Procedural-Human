"""
Mesh Bezier Handle Gizmo System

Provides edit-mode gizmos for manipulating Bezier handles on mesh vertices.
Each vertex has left and right handle offsets, similar to curve control points.
The handles are used for lofting smooth surfaces between mesh edges.
"""

import bpy
import bmesh
import gpu
import math
from gpu_extras.batch import batch_for_shader
from bpy.types import GizmoGroup, Operator, WorkSpaceTool
from mathutils import Vector, Matrix
from mathutils.geometry import interpolate_bezier

from procedural_human.decorators.gizmo_decorator import procedural_gizmo
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger

import time

# Gizmo drag state management
# Stores baseline handle values at drag start, keyed by (edge_index, "start"|"end")
_drag_start_baselines = {}
_last_set_fn_time = 0  # Timestamp for detecting new drag sessions
_DRAG_GAP_THRESHOLD_MS = 50  # Time gap to consider as potential new drag
_NEW_DRAG_VALUE_THRESHOLD = 0.15  # Value magnitude threshold - new drags start near zero

# --- CONFIGURATION ---
# BMesh EDGE layer names for storing handle offsets (6 floats per edge)
# Each edge has 2 handles: one at start vertex, one at end vertex
LAYER_HANDLE_START_X = "handle_start_x"  # Handle at edge.verts[0]
LAYER_HANDLE_START_Y = "handle_start_y"
LAYER_HANDLE_START_Z = "handle_start_z"
LAYER_HANDLE_END_X = "handle_end_x"      # Handle at edge.verts[1]
LAYER_HANDLE_END_Y = "handle_end_y"
LAYER_HANDLE_END_Z = "handle_end_z"

# Legacy names (kept for reference)
ATTR_HANDLE_LEFT = "handle_left"
ATTR_HANDLE_RIGHT = "handle_right"

HANDLE_COLOR = (1.0, 0.4, 0.1)      # Orange (RGB only)
HANDLE_COLOR_SELECTED = (1.0, 0.8, 0.2)  # Yellow for selected
LINE_COLOR = (0.5, 0.5, 0.5, 0.8)   # Grey for handle lines
CURVE_COLOR = (0.2, 0.8, 0.4, 1.0)  # Green for Bezier curves
BEZIER_RESOLUTION = 16              # Segments per curve

# Quarter-circle handle ratio: for a perfect quarter circle arc,
# the handle length should be edge_length * QUARTER_CIRCLE_RATIO
QUARTER_CIRCLE_RATIO = 0.5523  # 4 * (sqrt(2) - 1) / 3


# --- PART 1: DATA HELPERS ---

def ensure_edge_layers(bm):
    """
    Ensure BMesh has the required float layers for per-edge handle data.
    Each edge has 2 handles: start (at verts[0]) and end (at verts[1]).
    
    Args:
        bm: The BMesh object
        
    Returns:
        Tuple of (start_x, start_y, start_z, end_x, end_y, end_z) layer references
    """
    # Get or create layers for start handle (at edge.verts[0])
    start_x = bm.edges.layers.float.get(LAYER_HANDLE_START_X)
    if start_x is None:
        start_x = bm.edges.layers.float.new(LAYER_HANDLE_START_X)
    
    start_y = bm.edges.layers.float.get(LAYER_HANDLE_START_Y)
    if start_y is None:
        start_y = bm.edges.layers.float.new(LAYER_HANDLE_START_Y)
    
    start_z = bm.edges.layers.float.get(LAYER_HANDLE_START_Z)
    if start_z is None:
        start_z = bm.edges.layers.float.new(LAYER_HANDLE_START_Z)
    
    # Get or create layers for end handle (at edge.verts[1])
    end_x = bm.edges.layers.float.get(LAYER_HANDLE_END_X)
    if end_x is None:
        end_x = bm.edges.layers.float.new(LAYER_HANDLE_END_X)
    
    end_y = bm.edges.layers.float.get(LAYER_HANDLE_END_Y)
    if end_y is None:
        end_y = bm.edges.layers.float.new(LAYER_HANDLE_END_Y)
    
    end_z = bm.edges.layers.float.get(LAYER_HANDLE_END_Z)
    if end_z is None:
        end_z = bm.edges.layers.float.new(LAYER_HANDLE_END_Z)
    
    return (start_x, start_y, start_z, end_x, end_y, end_z)


def get_edge_layers(bm):
    """
    Get existing BMesh edge handle layers if they exist.
    
    Args:
        bm: The BMesh object
        
    Returns:
        Tuple of layer references or None if layers don't exist
    """
    start_x = bm.edges.layers.float.get(LAYER_HANDLE_START_X)
    start_y = bm.edges.layers.float.get(LAYER_HANDLE_START_Y)
    start_z = bm.edges.layers.float.get(LAYER_HANDLE_START_Z)
    end_x = bm.edges.layers.float.get(LAYER_HANDLE_END_X)
    end_y = bm.edges.layers.float.get(LAYER_HANDLE_END_Y)
    end_z = bm.edges.layers.float.get(LAYER_HANDLE_END_Z)
    
    if all([start_x, start_y, start_z, end_x, end_y, end_z]):
        return (start_x, start_y, start_z, end_x, end_y, end_z)
    return None


def has_edge_handle_layers(bm):
    """Check if BMesh has edge handle layers."""
    return get_edge_layers(bm) is not None


def get_edge_handles(edge, layers):
    """Get start and end handle vectors from an edge's BMesh layers."""
    start_x, start_y, start_z, end_x, end_y, end_z = layers
    start = Vector((edge[start_x], edge[start_y], edge[start_z]))
    end = Vector((edge[end_x], edge[end_y], edge[end_z]))
    return start, end


def set_edge_handles(edge, layers, start_vec, end_vec):
    """Set start and end handle vectors to an edge's BMesh layers."""
    start_x, start_y, start_z, end_x, end_y, end_z = layers
    edge[start_x] = start_vec.x
    edge[start_y] = start_vec.y
    edge[start_z] = start_vec.z
    edge[end_x] = end_vec.x
    edge[end_y] = end_vec.y
    edge[end_z] = end_vec.z


# Legacy aliases for compatibility
def ensure_bmesh_layers(bm):
    return ensure_edge_layers(bm)

def get_bmesh_layers(bm):
    return get_edge_layers(bm)

def has_bmesh_handle_layers(bm):
    return has_edge_handle_layers(bm)


def ensure_handle_attributes(obj):
    """
    Ensures the mesh has the required vector attributes on the POINT (vertex) domain.
    
    Args:
        obj: The Blender mesh object
        
    Returns:
        True if attributes exist or were created successfully
    """
    if obj.type != 'MESH':
        return False
        
    mesh = obj.data
    
    if ATTR_HANDLE_LEFT not in mesh.attributes:
        mesh.attributes.new(name=ATTR_HANDLE_LEFT, type='FLOAT_VECTOR', domain='POINT')
        logger.info(f"Created attribute: {ATTR_HANDLE_LEFT}")
        
    if ATTR_HANDLE_RIGHT not in mesh.attributes:
        mesh.attributes.new(name=ATTR_HANDLE_RIGHT, type='FLOAT_VECTOR', domain='POINT')
        logger.info(f"Created attribute: {ATTR_HANDLE_RIGHT}")
    
    return True


def get_connected_edges(mesh, vertex_index):
    """
    Get all edges connected to a vertex.
    
    Args:
        mesh: The Blender mesh data
        vertex_index: Index of the vertex
        
    Returns:
        List of (edge_index, other_vertex_index, edge_vector) tuples
    """
    edges = []
    for edge in mesh.edges:
        if vertex_index in edge.vertices:
            other_idx = edge.vertices[1] if edge.vertices[0] == vertex_index else edge.vertices[0]
            v_pos = mesh.vertices[vertex_index].co
            other_pos = mesh.vertices[other_idx].co
            edge_vec = other_pos - v_pos
            edges.append((edge.key, other_idx, edge_vec))
    return edges


def _calculate_handle_for_vertex(edge, vert, mesh_center, handle_len):
    """
    Calculate handle direction for an edge at a specific vertex.
    
    Uses adjacent edge averaging: the handle points OPPOSITE to the average
    direction of OTHER edges at this vertex (i.e., outward from the mesh),
    creating smooth convex surface transitions when lofting.
    
    Args:
        edge: The BMesh edge
        vert: The vertex (either edge.verts[0] or edge.verts[1])
        mesh_center: Center of the mesh for fallback outward direction
        handle_len: Length of the handle
        
    Returns:
        Vector: The handle offset from the vertex
    """
    # Get directions of other edges at this vertex
    other_dirs = []
    for other_edge in vert.link_edges:
        if other_edge != edge:
            other_vert = other_edge.other_vert(vert)
            other_dir = (other_vert.co - vert.co).normalized()
            other_dirs.append(other_dir)
    
    if other_dirs:
        # Average direction of other edges
        avg_dir = Vector((0, 0, 0))
        for d in other_dirs:
            avg_dir += d
        avg_dir /= len(other_dirs)
        
        if avg_dir.length > 0.0001:
            return -avg_dir.normalized() * handle_len  # NEGATE to point outward
    
    # Fallback: use perpendicular outward direction
    edge_vec = edge.other_vert(vert).co - vert.co
    edge_dir = edge_vec.normalized()
    
    # Outward from mesh center
    outward = vert.co - mesh_center
    if outward.length < 0.0001:
        outward = Vector((0, 0, 1))
    else:
        outward.normalize()
    
    # Project onto plane perpendicular to edge
    outward_perp = outward - edge_dir * outward.dot(edge_dir)
    if outward_perp.length > 0.0001:
        return outward_perp.normalized() * handle_len
    
    # Last resort: use vertex normal
    if vert.normal.length > 0:
        return vert.normal.normalized() * handle_len
    
    return Vector((0, 0, 1)) * handle_len


def calculate_auto_handles_bmesh(bm):
    """
    Calculate per-edge Bezier handles for smooth curve lofting.
    
    Each edge gets 2 handles:
    - start_handle: offset from edge.verts[0]
    - end_handle: offset from edge.verts[1]
    
    Handles point toward the average direction of other edges at each vertex,
    creating smooth surface transitions when lofting between edges.
    
    Args:
        bm: The BMesh object
    """
    layers = ensure_edge_layers(bm)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    # Calculate mesh center for fallback direction
    mesh_center = Vector((0, 0, 0))
    for v in bm.verts:
        mesh_center += v.co
    if len(bm.verts) > 0:
        mesh_center /= len(bm.verts)
    
    for edge in bm.edges:
        v0 = edge.verts[0]
        v1 = edge.verts[1]
        
        edge_vec = v1.co - v0.co
        edge_len = edge_vec.length
        
        if edge_len < 0.0001:
            # Degenerate edge - zero handles
            set_edge_handles(edge, layers, Vector((0, 0, 0)), Vector((0, 0, 0)))
            continue
        
        # Handle length for quarter-circle arc
        handle_len = edge_len * QUARTER_CIRCLE_RATIO
        
        # Calculate handles using adjacent edge averaging
        start_handle = _calculate_handle_for_vertex(edge, v0, mesh_center, handle_len)
        end_handle = _calculate_handle_for_vertex(edge, v1, mesh_center, handle_len)
        
        set_edge_handles(edge, layers, start_handle, end_handle)


def calculate_auto_handles(obj):
    """
    Calculate Catmull-Rom inspired auto-handles for all vertices.
    Works in both edit mode (BMesh) and object mode (mesh attributes).
    
    Args:
        obj: The Blender mesh object
    """
    if obj.type != 'MESH':
        return
    
    mesh = obj.data
    
    # Check if we're in edit mode - use BMesh
    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(mesh)
        calculate_auto_handles_bmesh(bm)
        bmesh.update_edit_mesh(mesh)
        return
    
    # Object mode - use mesh attributes (legacy support)
    ensure_handle_attributes(obj)
    
    handle_left_attr = mesh.attributes[ATTR_HANDLE_LEFT]
    handle_right_attr = mesh.attributes[ATTR_HANDLE_RIGHT]
    
    for v_idx, vertex in enumerate(mesh.vertices):
        connected = get_connected_edges(mesh, v_idx)
        
        if len(connected) == 0:
            handle_left_attr.data[v_idx].vector = Vector((0, 0, 0))
            handle_right_attr.data[v_idx].vector = Vector((0, 0, 0))
            continue
        
        if len(connected) == 1:
            edge_vec = connected[0][2]
            edge_len = edge_vec.length
            if edge_len > 0:
                handle_dir = edge_vec.normalized()
                handle_len = edge_len * QUARTER_CIRCLE_RATIO
                handle_left_attr.data[v_idx].vector = -handle_dir * handle_len
                handle_right_attr.data[v_idx].vector = handle_dir * handle_len
            continue
        
        avg_tangent = Vector((0, 0, 0))
        total_weight = 0
        
        for _, _, edge_vec in connected:
            edge_len = edge_vec.length
            if edge_len > 0:
                avg_tangent += edge_vec.normalized() * edge_len
                total_weight += edge_len
        
        if total_weight > 0:
            avg_tangent /= total_weight
        
        if avg_tangent.length > 0.0001:
            primary_dir = avg_tangent.normalized()
            normal = vertex.normal if hasattr(vertex, 'normal') else Vector((0, 0, 1))
            perp = primary_dir.cross(normal)
            if perp.length < 0.0001:
                perp = primary_dir.cross(Vector((0, 0, 1)))
            if perp.length < 0.0001:
                perp = primary_dir.cross(Vector((0, 1, 0)))
            perp.normalize()
            
            avg_edge_len = total_weight / len(connected)
            handle_len = avg_edge_len * QUARTER_CIRCLE_RATIO
            
            best_left = None
            best_right = None
            best_left_dot = 1
            best_right_dot = -1
            
            for _, _, edge_vec in connected:
                if edge_vec.length > 0:
                    edge_dir = edge_vec.normalized()
                    dot = edge_dir.dot(perp)
                    if dot < best_left_dot:
                        best_left_dot = dot
                        best_left = edge_vec
                    if dot > best_right_dot:
                        best_right_dot = dot
                        best_right = edge_vec
            
            if best_left is not None and best_left.length > 0:
                left_dir = best_left.normalized()
                left_blend = (left_dir * 0.7 + (-perp) * 0.3).normalized()
                handle_left_attr.data[v_idx].vector = left_blend * handle_len
            else:
                handle_left_attr.data[v_idx].vector = -perp * handle_len
            
            if best_right is not None and best_right.length > 0:
                right_dir = best_right.normalized()
                right_blend = (right_dir * 0.7 + perp * 0.3).normalized()
                handle_right_attr.data[v_idx].vector = right_blend * handle_len
            else:
                handle_right_attr.data[v_idx].vector = perp * handle_len
        else:
            if len(connected) >= 2:
                e1 = connected[0][2]
                e2 = connected[1][2]
                if e1.length > 0 and e2.length > 0:
                    handle_left_attr.data[v_idx].vector = e1.normalized() * (e1.length * QUARTER_CIRCLE_RATIO)
                    handle_right_attr.data[v_idx].vector = e2.normalized() * (e2.length * QUARTER_CIRCLE_RATIO)
    
    mesh.update()
    logger.info(f"Calculated auto-handles for {len(mesh.vertices)} vertices")


def get_edge_handle_data(obj, bm=None):
    """
    Get handle data for all edges in world space.
    Each edge has 2 handles: start (at verts[0]) and end (at verts[1]).
    
    Args:
        obj: The mesh object
        bm: Optional BMesh for edit mode access
        
    Returns:
        List of (edge_index, v0_pos, v1_pos, start_handle_pos, end_handle_pos, is_selected) tuples
    """
    mesh = obj.data
    matrix = obj.matrix_world
    results = []
    
    # In edit mode, use BMesh edge layers
    if bm is not None:
        layers = get_edge_layers(bm)
        if layers is None:
            return []
        
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        
        for edge in bm.edges:
            v0 = edge.verts[0]
            v1 = edge.verts[1]
            start_handle, end_handle = get_edge_handles(edge, layers)
            
            v0_world = matrix @ v0.co
            v1_world = matrix @ v1.co
            # Handles are offsets from their respective vertices
            start_handle_world = matrix @ (v0.co + start_handle)
            end_handle_world = matrix @ (v1.co + end_handle)
            
            results.append((edge.index, v0_world, v1_world, start_handle_world, end_handle_world, edge.select))
        
        return results
    
    return []  # Edge mode only supported in edit mode


# Backward compatible alias
def get_vertex_handle_data(obj, bm=None):
    """Legacy alias - returns edge handle data."""
    return get_edge_handle_data(obj, bm)


def get_edge_bezier_data(obj, bm=None):
    """
    Get Bezier curve data for all edges.
    
    For each edge, returns the knots and handles needed for interpolate_bezier.
    
    Args:
        obj: The mesh object
        bm: Optional BMesh for edit mode access
        
    Returns:
        List of (knot1, handle1, handle2, knot2) tuples in world space
    """
    mesh = obj.data
    matrix = obj.matrix_world
    results = []
    
    # In edit mode, use BMesh edge layers
    if bm is not None:
        layers = get_edge_layers(bm)
        if layers is None:
            return []
        
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        
        for edge in bm.edges:
            v0 = edge.verts[0]
            v1 = edge.verts[1]
            start_handle, end_handle = get_edge_handles(edge, layers)
            
            knot1 = matrix @ v0.co
            knot2 = matrix @ v1.co
            
            # start_handle is at v0, end_handle is at v1
            handle1 = matrix @ (v0.co + start_handle)
            handle2 = matrix @ (v1.co + end_handle)
            
            results.append((knot1, handle1, handle2, knot2))
        
        return results
    
    return []  # Edge mode only supported in edit mode


# --- PART 2: GPU DRAWING ---

shader = gpu.shader.from_builtin('UNIFORM_COLOR')

def draw_bezier_curves():
    """
    Draw Bezier curves for all edges using the per-edge handle data.
    Uses mathutils.geometry.interpolate_bezier for curve calculation.
    """
    context = bpy.context
    obj = context.object
    
    if not obj or obj.type != 'MESH':
        return
    
    # Get bmesh in edit mode and check for handle layers
    bm = None
    if context.mode == 'EDIT_MESH':
        bm = bmesh.from_edit_mesh(obj.data)
        if not has_edge_handle_layers(bm):
            return
    else:
        # Edge mode only supported in edit mode
        return
    
    # Draw handle lines (vertex to handles) - one line per handle
    handle_data = get_edge_handle_data(obj, bm)
    handle_coords = []
    
    for edge_idx, v0_pos, v1_pos, start_handle_pos, end_handle_pos, is_selected in handle_data:
        # Line from v0 to start handle
        handle_coords.append(v0_pos)
        handle_coords.append(start_handle_pos)
        # Line from v1 to end handle
        handle_coords.append(v1_pos)
        handle_coords.append(end_handle_pos)
    
    if handle_coords:
        batch = batch_for_shader(shader, 'LINES', {"pos": handle_coords})
        gpu.state.blend_set('ALPHA')
        gpu.state.line_width_set(1.0)
        shader.bind()
        shader.uniform_float("color", LINE_COLOR)
        batch.draw(shader)
    
    # Draw Bezier curves
    bezier_data = get_edge_bezier_data(obj, bm)
    curve_coords = []
    
    for knot1, handle1, handle2, knot2 in bezier_data:
        # Use Blender's built-in Bezier interpolation
        points = interpolate_bezier(knot1, handle1, handle2, knot2, BEZIER_RESOLUTION)
        
        # Convert to line segments
        for i in range(len(points) - 1):
            curve_coords.append(points[i])
            curve_coords.append(points[i + 1])
    
    if curve_coords:
        batch = batch_for_shader(shader, 'LINES', {"pos": curve_coords})
        gpu.state.line_width_set(2.0)
        shader.bind()
        shader.uniform_float("color", CURVE_COLOR)
        batch.draw(shader)
    
    gpu.state.blend_set('NONE')


# --- PART 3: GIZMO GROUP ---

@procedural_gizmo
class LoftHandleGizmoGroup(GizmoGroup):
    """
    GizmoGroup for editing Bezier handles on mesh vertices.
    Works in EDIT mode using BMesh custom layers for real-time editing.
    """
    bl_idname = "MESH_GGT_loft_handles"
    bl_label = "Loft Handles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        """Only show in edit mode with a mesh that has BMesh handle layers."""
        if context.mode != 'EDIT_MESH':
            return False
        ob = context.object
        if not (ob and ob.type == 'MESH'):
            return False
        # Check if BMesh has handle layers
        try:
            bm = bmesh.from_edit_mesh(ob.data)
            return has_bmesh_handle_layers(bm)
        except Exception:
            return False

    def setup(self, context):
        """Initialize gizmo pools (one pair per edge)."""
        self._gizmos_start = []  # Handle at edge.verts[0]
        self._gizmos_end = []    # Handle at edge.verts[1]
        self._active_count = 0

    def refresh(self, context):
        """Refresh is called when the gizmo group should update."""
        pass

    def _ensure_gizmo_count(self, needed):
        """Ensure we have enough gizmos in the pool (2 per edge)."""
        while len(self._gizmos_start) < needed:
            # Create start handle gizmo (at edge.verts[0])
            gz_start = self.gizmos.new("GIZMO_GT_move_3d")
            gz_start.scale_basis = 0.12
            gz_start.use_draw_modal = True
            gz_start.color = HANDLE_COLOR
            gz_start.alpha = 0.8
            gz_start.color_highlight = HANDLE_COLOR_SELECTED
            gz_start.alpha_highlight = 1.0
            self._gizmos_start.append(gz_start)
            
            # Create end handle gizmo (at edge.verts[1])
            gz_end = self.gizmos.new("GIZMO_GT_move_3d")
            gz_end.scale_basis = 0.12
            gz_end.use_draw_modal = True
            gz_end.color = HANDLE_COLOR
            gz_end.alpha = 0.8
            gz_end.color_highlight = HANDLE_COLOR_SELECTED
            gz_end.alpha_highlight = 1.0
            self._gizmos_end.append(gz_end)

    def draw_prepare(self, context):
        """Update gizmo positions and visibility each frame using per-edge BMesh layers."""
        ob = context.object
        if not ob or ob.type != 'MESH':
            return
        
        mesh = ob.data
        
        # Get bmesh for edit mode
        bm = bmesh.from_edit_mesh(mesh)
        layers = get_edge_layers(bm)
        if layers is None:
            return
        
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        
        # Get all edges (or just selected if some are selected)
        selected_edges = [e for e in bm.edges if e.select]
        if not selected_edges:
            # Show handles for all edges if none selected
            target_edges = list(bm.edges)
        else:
            target_edges = selected_edges
        
        needed = len(target_edges)
        self._ensure_gizmo_count(needed)
        
        # Hide all gizmos first
        for gz in self._gizmos_start:
            gz.hide = True
        for gz in self._gizmos_end:
            gz.hide = True
        
        matrix = ob.matrix_world
        
        # Position and show gizmos for target edges (2 gizmos per edge)
        for i, edge in enumerate(target_edges):
            edge_idx = edge.index  # Capture index
            v0_co = edge.verts[0].co.copy()
            v1_co = edge.verts[1].co.copy()
            start_handle, end_handle = get_edge_handles(edge, layers)
            
            # Start handle gizmo (at v0) - ALWAYS update position
            gz_start = self._gizmos_start[i]
            gz_start.hide = False
            start_world = matrix @ (v0_co + start_handle)
            gz_start.matrix_basis = matrix.to_3x3().to_4x4()
            gz_start.matrix_basis.translation = start_world
            
            # End handle gizmo (at v1) - ALWAYS update position
            gz_end = self._gizmos_end[i]
            gz_end.hide = False
            end_world = matrix @ (v1_co + end_handle)
            gz_end.matrix_basis = matrix.to_3x3().to_4x4()
            gz_end.matrix_basis.translation = end_world
            
            
            # Set up target handler for start handle using edge INDEX
            # Note: get_fn returns (0,0,0) because the gizmo position is already set via matrix_basis
            # set_fn receives the offset in gizmo-local space (affected by matrix_basis rotation)
            def make_start_handler(edge_index, mesh_data, world_matrix):
                def get_fn():
                    return Vector((0, 0, 0))
                
                def set_fn(value):
                    global _drag_start_baselines, _last_set_fn_time
                    
                    # Detect new drag session using timestamps AND value magnitude
                    # A TRUE new drag has: time gap > threshold AND value near zero
                    current_time = int(time.time() * 1000)
                    time_since_last = current_time - _last_set_fn_time if _last_set_fn_time > 0 else 0
                    value_magnitude = Vector(value).length
                    is_new_drag = (
                        _last_set_fn_time > 0 and 
                        time_since_last > _DRAG_GAP_THRESHOLD_MS and 
                        value_magnitude < _NEW_DRAG_VALUE_THRESHOLD and
                        _drag_start_baselines
                    )
                    if is_new_drag:
                        _drag_start_baselines.clear()
                    _last_set_fn_time = current_time
                    
                    bm_fresh = bmesh.from_edit_mesh(mesh_data)
                    bm_fresh.edges.ensure_lookup_table()
                    edge_fresh = bm_fresh.edges[edge_index]
                    lyrs = get_edge_layers(bm_fresh)
                    if lyrs:
                        start_x_layer, start_y_layer, start_z_layer, _, _, _ = lyrs
                        current_handle = Vector((
                            edge_fresh[start_x_layer],
                            edge_fresh[start_y_layer],
                            edge_fresh[start_z_layer]
                        ))
                        
                        # On first call for this edge/handle, capture current BMesh value as baseline
                        baseline_key = (edge_index, "start")
                        if baseline_key not in _drag_start_baselines:
                            _drag_start_baselines[baseline_key] = current_handle.copy()
                        
                        baseline = _drag_start_baselines[baseline_key]
                        
                        # Convert world-space offset to local-space offset
                        rot_inv = world_matrix.to_3x3().inverted()
                        local_delta = rot_inv @ Vector(value)
                        
                        # Apply delta to the baseline
                        new_handle = baseline + local_delta
                        
                        edge_fresh[start_x_layer] = new_handle.x
                        edge_fresh[start_y_layer] = new_handle.y
                        edge_fresh[start_z_layer] = new_handle.z
                        bmesh.update_edit_mesh(mesh_data)
                    
                return get_fn, set_fn
            
            get_s, set_s = make_start_handler(edge_idx, mesh, matrix)
            gz_start.target_set_handler("offset", get=get_s, set=set_s)
            
            # Set up target handler for end handle using edge INDEX
            def make_end_handler(edge_index, mesh_data, world_matrix):
                def get_fn():
                    return Vector((0, 0, 0))
                
                def set_fn(value):
                    global _drag_start_baselines, _last_set_fn_time
                    
                    # Detect new drag session using timestamps AND value magnitude
                    current_time = int(time.time() * 1000)
                    time_since_last = current_time - _last_set_fn_time if _last_set_fn_time > 0 else 0
                    value_magnitude = Vector(value).length
                    is_new_drag = (
                        _last_set_fn_time > 0 and 
                        time_since_last > _DRAG_GAP_THRESHOLD_MS and 
                        value_magnitude < _NEW_DRAG_VALUE_THRESHOLD and
                        _drag_start_baselines
                    )
                    if is_new_drag:
                        _drag_start_baselines.clear()
                    _last_set_fn_time = current_time
                    
                    bm_fresh = bmesh.from_edit_mesh(mesh_data)
                    bm_fresh.edges.ensure_lookup_table()
                    edge_fresh = bm_fresh.edges[edge_index]
                    lyrs = get_edge_layers(bm_fresh)
                    if lyrs:
                        _, _, _, end_x_layer, end_y_layer, end_z_layer = lyrs
                        current_handle = Vector((
                            edge_fresh[end_x_layer],
                            edge_fresh[end_y_layer],
                            edge_fresh[end_z_layer]
                        ))
                        
                        # On first call for this edge/handle, capture current BMesh value as baseline
                        baseline_key = (edge_index, "end")
                        if baseline_key not in _drag_start_baselines:
                            _drag_start_baselines[baseline_key] = current_handle.copy()
                        
                        baseline = _drag_start_baselines[baseline_key]
                        
                        # Convert world-space offset to local-space offset
                        rot_inv = world_matrix.to_3x3().inverted()
                        local_delta = rot_inv @ Vector(value)
                        
                        # Apply delta to the baseline
                        new_handle = baseline + local_delta
                        
                        edge_fresh[end_x_layer] = new_handle.x
                        edge_fresh[end_y_layer] = new_handle.y
                        edge_fresh[end_z_layer] = new_handle.z
                        bmesh.update_edit_mesh(mesh_data)
                    
                return get_fn, set_fn
            
            get_e, set_e = make_end_handler(edge_idx, mesh, matrix)
            gz_end.target_set_handler("offset", get=get_e, set=set_e)
        
        self._active_count = needed


# --- PART 4: OPERATORS ---

@procedural_operator
class InitializeLoftHandlesOperator(Operator):
    """Initialize Bezier handles on mesh vertices for lofting"""
    
    bl_idname = "mesh.initialize_loft_handles"
    bl_label = "Initialize Loft Handles"
    bl_description = "Create and initialize Bezier handles on mesh vertices using auto-smoothing"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'
    
    def execute(self, context):
        obj = context.object
        mesh = obj.data
        
        # Enter edit mode if not already
        if context.mode != 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='EDIT')
        
        # Get BMesh and create/populate layers
        bm = bmesh.from_edit_mesh(mesh)
        calculate_auto_handles_bmesh(bm)
        bmesh.update_edit_mesh(mesh)
        
        self.report({'INFO'}, f"Initialized loft handles for {len(bm.verts)} vertices")
        return {'FINISHED'}


@procedural_operator
class RecalculateLoftHandlesOperator(Operator):
    """Recalculate handles using auto-smoothing algorithm"""
    
    bl_idname = "mesh.recalculate_loft_handles"
    bl_label = "Recalculate Loft Handles"
    bl_description = "Recalculate Bezier handles using Catmull-Rom inspired smoothing"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if context.mode != 'EDIT_MESH':
            return False
        obj = context.object
        if not (obj and obj.type == 'MESH'):
            return False
        # Check if BMesh has handle layers
        try:
            bm = bmesh.from_edit_mesh(obj.data)
            return has_bmesh_handle_layers(bm)
        except Exception:
            return False
    
    def execute(self, context):
        obj = context.object
        mesh = obj.data
        
        bm = bmesh.from_edit_mesh(mesh)
        calculate_auto_handles_bmesh(bm)
        bmesh.update_edit_mesh(mesh)
        
        self.report({'INFO'}, "Recalculated loft handles")
        return {'FINISHED'}


@procedural_operator  
class ClearLoftHandlesOperator(Operator):
    """Remove loft handle layers from mesh"""
    
    bl_idname = "mesh.clear_loft_handles"
    bl_label = "Clear Loft Handles"
    bl_description = "Remove all Bezier handle data from the mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if context.mode != 'EDIT_MESH':
            return False
        obj = context.object
        if not (obj and obj.type == 'MESH'):
            return False
        try:
            bm = bmesh.from_edit_mesh(obj.data)
            return has_bmesh_handle_layers(bm)
        except Exception:
            return False
    
    def execute(self, context):
        obj = context.object
        mesh = obj.data
        
        bm = bmesh.from_edit_mesh(mesh)
        
        # Remove BMesh edge float layers (new per-edge system)
        edge_layer_names = [
            LAYER_HANDLE_START_X, LAYER_HANDLE_START_Y, LAYER_HANDLE_START_Z,
            LAYER_HANDLE_END_X, LAYER_HANDLE_END_Y, LAYER_HANDLE_END_Z
        ]
        
        for layer_name in edge_layer_names:
            layer = bm.edges.layers.float.get(layer_name)
            if layer:
                bm.edges.layers.float.remove(layer)
        
        bmesh.update_edit_mesh(mesh)
        
        self.report({'INFO'}, "Cleared loft handles")
        return {'FINISHED'}


# --- PART 5: TOOLBAR TOOL ---

class LoftHandlesTool(WorkSpaceTool):
    """Edit mode tool for manipulating loft handles"""
    
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'EDIT_MESH'
    bl_idname = "mesh_tool.loft_handles"
    bl_label = "Loft Handles"
    bl_description = "Edit Bezier handles for lofting curves between mesh edges"
    bl_icon = "ops.curve.draw"  # Use curve draw icon
    bl_widget = "MESH_GGT_loft_handles"
    bl_keymap = (
        # Initialize handles with Ctrl+Shift+H
        ("mesh.initialize_loft_handles", {"type": 'H', "value": 'PRESS', "ctrl": True, "shift": True}, None),
        # Recalculate with Shift+H
        ("mesh.recalculate_loft_handles", {"type": 'H', "value": 'PRESS', "shift": True}, None),
    )

    def draw_settings(context, layout, tool):
        """Draw tool settings in the header."""
        layout.operator("mesh.initialize_loft_handles", text="Initialize")
        layout.operator("mesh.recalculate_loft_handles", text="Recalculate")
        layout.operator("mesh.clear_loft_handles", text="Clear")


# --- PART 6: REGISTRATION ---

_draw_handler = None

def register():
    """Register the gizmo system and draw handler."""
    global _draw_handler
    
    # Register draw handler for Bezier curves
    from procedural_human.decorators.gizmo_decorator import procedural_gizmo
    _draw_handler = procedural_gizmo.register_draw_handler(
        "loft_bezier_curves",
        draw_bezier_curves,
        (),
        'POST_VIEW'
    )
    
    # Register the tool
    bpy.utils.register_tool(LoftHandlesTool, separator=True, group=False)
    
    logger.info("Loft Handle Gizmo System registered")


def unregister():
    """Unregister the gizmo system."""
    global _draw_handler
    
    # Unregister tool
    try:
        bpy.utils.unregister_tool(LoftHandlesTool)
    except Exception:
        pass
    
    # Unregister draw handler
    from procedural_human.decorators.gizmo_decorator import procedural_gizmo
    procedural_gizmo.unregister_draw_handler("loft_bezier_curves")
    _draw_handler = None


if __name__ == "__main__":
    register()
