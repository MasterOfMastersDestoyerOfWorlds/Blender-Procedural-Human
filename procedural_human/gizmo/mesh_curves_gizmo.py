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

from procedural_human.decorators.gizmo_decorator import procedural_gizmo_group
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger

import numpy as np

HANDLE_COLOR = (1.0, 0.4, 0.1)
HANDLE_COLOR_SELECTED = (1.0, 0.8, 0.2)
LINE_COLOR = (0.5, 0.5, 0.5, 0.8)
CURVE_COLOR = (0.2, 0.8, 0.4, 1.0)
BEZIER_RESOLUTION = 16

LAYER_HANDLE_START_X = "handle_start_x"
LAYER_HANDLE_START_Y = "handle_start_y"
LAYER_HANDLE_START_Z = "handle_start_z"
LAYER_HANDLE_END_X = "handle_end_x"
LAYER_HANDLE_END_Y = "handle_end_y"
LAYER_HANDLE_END_Z = "handle_end_z"


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


def get_edge_layers(bm):
    """Get existing BMesh edge handle layers if they exist."""
    start_x = bm.edges.layers.float.get(LAYER_HANDLE_START_X)
    start_y = bm.edges.layers.float.get(LAYER_HANDLE_START_Y)
    start_z = bm.edges.layers.float.get(LAYER_HANDLE_START_Z)
    end_x = bm.edges.layers.float.get(LAYER_HANDLE_END_X)
    end_y = bm.edges.layers.float.get(LAYER_HANDLE_END_Y)
    end_z = bm.edges.layers.float.get(LAYER_HANDLE_END_Z)
    
    if all([start_x, start_y, start_z, end_x, end_y, end_z]):
        return (start_x, start_y, start_z, end_x, end_y, end_z)
    return None


def get_connected_edges(mesh, vertex_index):
    """Get all edges connected to a vertex."""
    edges = []
    for edge in mesh.edges:
        if vertex_index in edge.vertices:
            other_idx = edge.vertices[1] if edge.vertices[0] == vertex_index else edge.vertices[0]
            v_pos = mesh.vertices[vertex_index].co
            other_pos = mesh.vertices[other_idx].co
            edge_vec = other_pos - v_pos
            edges.append((edge.key, other_idx, edge_vec))
    return edges


def _get_handles_at_vertex(vert, layers):
    """Get all handle offsets at a vertex from connected edges."""
    handles = []
    for edge in vert.link_edges:
        if edge.verts[0] == vert:
            start_x, start_y, start_z, _, _, _ = layers
            handle = Vector((edge[start_x], edge[start_y], edge[start_z]))
            handles.append((edge, "start", handle))
        else:
            _, _, _, end_x, end_y, end_z = layers
            handle = Vector((edge[end_x], edge[end_y], edge[end_z]))
            handles.append((edge, "end", handle))
    return handles


def _set_handle_at_vertex(edge, handle_type, handle_vec, layers):
    """Set a handle vector for a specific edge and handle type."""
    if handle_type == "start":
        start_x, start_y, start_z, _, _, _ = layers
        edge[start_x] = handle_vec.x
        edge[start_y] = handle_vec.y
        edge[start_z] = handle_vec.z
    else:
        _, _, _, end_x, end_y, end_z = layers
        edge[end_x] = handle_vec.x
        edge[end_y] = handle_vec.y
        edge[end_z] = handle_vec.z


def make_handles_coplanar_at_vertex(vert, layers):
    """Project all handles at a vertex onto their best-fit plane using PCA on EDGE TANGENTS."""
    handles = _get_handles_at_vertex(vert, layers)
    
    if len(handles) <= 2:
        return
    
    edge_tangents = []
    for edge in vert.link_edges:
        other_vert = edge.other_vert(vert)
        tangent = (other_vert.co - vert.co).normalized()
        edge_tangents.append(tangent)
    
    if len(edge_tangents) < 2:
        return
    
    points = np.array([[t.x, t.y, t.z] for t in edge_tangents])
    
    cov_matrix = np.cov(points.T)
    
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    
    plane_normal = Vector(eigenvectors[:, 0])
    
    if plane_normal.length < 0.0001:
        return
    
    plane_normal.normalize()
    
    for edge, handle_type, handle_vec in handles:
        original_length = handle_vec.length
        if original_length < 0.0001:
            continue
        
        projection = handle_vec - plane_normal * handle_vec.dot(plane_normal)
        
        if projection.length > 0.0001:
            projection = projection.normalized() * original_length
        else:
            continue
        
        _set_handle_at_vertex(edge, handle_type, projection, layers)


def _capture_all_handles_at_vertex(vert, layers, baselines_dict):
    """Capture baselines for all handles at a vertex if they don't already exist."""
    handles = _get_handles_at_vertex(vert, layers)
    for edge, h_type, handle_vec in handles:
        key = (edge.index, h_type)
        if key not in baselines_dict:
            baselines_dict[key] = handle_vec.copy()


def _rotate_coplanar_handles(vert, moved_edge_index, handle_type, old_handle, new_handle, bm, layers, baselines_dict):
    """Rotate all other handles at this vertex to maintain coplanarity."""
    if old_handle.length < 0.0001 or new_handle.length < 0.0001:
        return
    
    old_dir = old_handle.normalized()
    new_dir = new_handle.normalized()
    
    axis = old_dir.cross(new_dir)
    
    if axis.length < 0.0001:
        return
    
    axis.normalize()
    
    dot = old_dir.dot(new_dir)
    dot = max(-1.0, min(1.0, dot))
    angle = math.acos(dot)
    
    if abs(angle) < 0.0001:
        return
    
    rotation_matrix = Matrix.Rotation(angle, 3, axis)
    
    handles = _get_handles_at_vertex(vert, layers)
    
    for edge, h_type, _ in handles:
        if edge.index == moved_edge_index and h_type == handle_type:
            continue
        
        key = (edge.index, h_type)
        if key not in baselines_dict:
            continue
        
        baseline_handle = baselines_dict[key]
        
        original_length = baseline_handle.length
        if original_length < 0.0001:
            continue
        
        rotated = rotation_matrix @ baseline_handle
        
        rotated = rotated.normalized() * original_length
        
        _set_handle_at_vertex(edge, h_type, rotated, layers)


def get_edge_handle_data(obj, bm=None):
    """Get handle data for all edges in world space."""
    mesh = obj.data
    matrix = obj.matrix_world
    results = []
    
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
            start_handle_world = matrix @ (v0.co + start_handle)
            end_handle_world = matrix @ (v1.co + end_handle)
            
            results.append((edge.index, v0_world, v1_world, start_handle_world, end_handle_world, edge.select))
        
        return results
    
    return []


def get_vertex_handle_data(obj, bm=None):
    """Legacy alias - returns edge handle data."""
    return get_edge_handle_data(obj, bm)


def get_edge_bezier_data(obj, bm=None):
    """Get Bezier curve data for all edges."""
    mesh = obj.data
    matrix = obj.matrix_world
    results = []
    
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
            
            handle1 = matrix @ (v0.co + start_handle)
            handle2 = matrix @ (v1.co + end_handle)
            
            results.append((knot1, handle1, handle2, knot2))
        
        return results
    
    return []


shader = gpu.shader.from_builtin('UNIFORM_COLOR')


def _is_loft_tool_active(context):
    """Check if the loft handles tool is currently active."""

    tool = bpy.context.workspace.tools.from_space_view3d_mode(
        bpy.context.mode, create=False
    )
    if tool.idname == 'mesh_tool.loft_handles':
        return True
    return False


def _get_active_vertex(bm):
    """Get the last selected vertex from select_history."""
    try:
        if not hasattr(bm, 'select_history'):
            return None
        if len(bm.select_history) == 0:
            selected_verts = [v for v in bm.verts if v.select]
            if selected_verts:
                return selected_verts[-1]
            return None
        active = bm.select_history.active
        if active and isinstance(active, bmesh.types.BMVert):
            return active
        for elem in reversed(bm.select_history):
            if isinstance(elem, bmesh.types.BMVert):
                return elem
        selected_verts = [v for v in bm.verts if v.select]
        if selected_verts:
            return selected_verts[-1]
        return None
    except Exception:
        return None


def draw_bezier_curves():
    """Draw Bezier curves for edges connected to the active vertex."""
    context = bpy.context
    obj = context.object
    
    if not obj or obj.type != 'MESH':
        return
    
    if context.mode != 'EDIT_MESH':
        return
    
    try:
        bm = bmesh.from_edit_mesh(obj.data)
        if not has_edge_handle_layers(bm):
            return
        
        active_vert = _get_active_vertex(bm)
        if not active_vert:
            selected_verts = [v for v in bm.verts if v.select]
            if selected_verts:
                active_vert = selected_verts[0]
            else:
                return
        
        layers = get_edge_layers(bm)
        if not layers:
            return
        
        tool_active = _is_loft_tool_active(context)
        if not tool_active:
            return
    except Exception as e:
        return
    
    matrix = obj.matrix_world
    handle_coords = []
    curve_coords = []
    
    for edge in active_vert.link_edges:
        v0 = edge.verts[0]
        v1 = edge.verts[1]
        start_handle, end_handle = get_edge_handles(edge, layers)
        
        v0_world = matrix @ v0.co
        v1_world = matrix @ v1.co
        start_handle_world = matrix @ (v0.co + start_handle)
        end_handle_world = matrix @ (v1.co + end_handle)
        
        handle_coords.append(v0_world)
        handle_coords.append(start_handle_world)
        handle_coords.append(v1_world)
        handle_coords.append(end_handle_world)
        
        knot1 = matrix @ v0.co
        knot2 = matrix @ v1.co
        handle1 = matrix @ (v0.co + start_handle)
        handle2 = matrix @ (v1.co + end_handle)
        
        points = interpolate_bezier(knot1, handle1, handle2, knot2, BEZIER_RESOLUTION)
        
        for i in range(len(points) - 1):
            curve_coords.append(points[i])
            curve_coords.append(points[i + 1])
    
    gpu.state.depth_test_set('LESS_EQUAL')
    if handle_coords:
        batch = batch_for_shader(shader, 'LINES', {"pos": handle_coords})
        gpu.state.blend_set('ALPHA')
        gpu.state.line_width_set(1.0)
        shader.bind()
        shader.uniform_float("color", LINE_COLOR)
        batch.draw(shader)
    
    if curve_coords:
        batch = batch_for_shader(shader, 'LINES', {"pos": curve_coords})
        gpu.state.line_width_set(2.0)
        shader.bind()
        shader.uniform_float("color", CURVE_COLOR)
        batch.draw(shader)
    
    gpu.state.blend_set('NONE')
    gpu.state.depth_test_set('NONE')


@procedural_gizmo_group
class LoftHandleGizmoGroup(GizmoGroup):
    """GizmoGroup for editing Bezier handles on mesh vertices."""
    bl_idname = "MESH_GGT_loft_handles"
    bl_label = "Loft Handles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'DEPTH_3D'}
 
    @classmethod
    def poll(cls, context):
        """Only show in edit mode with a mesh that has BMesh handle layers."""
        if context.mode != 'EDIT_MESH':
            return False
        ob = context.object
        if not (ob and ob.type == 'MESH'):
            return False
        try:
            bm = bmesh.from_edit_mesh(ob.data)
            return has_edge_handle_layers(bm)
        except Exception:
            return False

    def setup(self, context):
        """Initialize gizmo pools."""
        self._gizmos = []
        self._active_count = 0

    def refresh(self, context):
        """Refresh is called when the gizmo group should update."""
        pass

    def _ensure_gizmo_count(self, needed):
        """Ensure we have enough gizmos in the pool."""
        while len(self._gizmos) < needed:
            try:
                gz = self.gizmos.new("GIZMO_GT_loft_handle")
            except Exception:
                gz = self.gizmos.new("GIZMO_GT_move_3d")
                gz.scale_basis = 0.3
                gz.color = HANDLE_COLOR
                gz.alpha = 1.0
                gz.color_highlight = HANDLE_COLOR_SELECTED
                gz.alpha_highlight = 1.0
            self._gizmos.append(gz)

    def draw_prepare(self, context):
        """Update gizmo positions and visibility each frame."""
        # Only show gizmos if the loft tool is active
        if not _is_loft_tool_active(context):
            for gz in self._gizmos:
                gz.hide = True
            return

        ob = context.object
        if not ob or ob.type != 'MESH':
            for gz in self._gizmos:
                gz.hide = True
            return
        
        try:
            mesh = ob.data
            bm = bmesh.from_edit_mesh(mesh)
            layers = get_edge_layers(bm)
            if layers is None:
                for gz in self._gizmos:
                    gz.hide = True
                return
            
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            
            active_vert = _get_active_vertex(bm)
            if not active_vert:
                selected_verts = [v for v in bm.verts if v.select]
                if selected_verts:
                    active_vert = selected_verts[0]
                else:
                    for gz in self._gizmos:
                        gz.hide = True
                    return
        except Exception:
            for gz in self._gizmos:
                gz.hide = True
            return
        
        connected_edges = list(active_vert.link_edges)
        needed = len(connected_edges) * 2
        self._ensure_gizmo_count(needed)
        
        for gz in self._gizmos:
            gz.hide = True
        
        matrix = ob.matrix_world
        gizmo_idx = 0
        
        for edge in connected_edges:
            v0_co = edge.verts[0].co.copy()
            v1_co = edge.verts[1].co.copy()
            start_handle, end_handle = get_edge_handles(edge, layers)
            
            if edge.verts[0] == active_vert:
                if gizmo_idx >= len(self._gizmos):
                    self._ensure_gizmo_count(gizmo_idx + 1)
                gz_start = self._gizmos[gizmo_idx]
                gz_start.hide = False
                gz_start.target_edge_index = edge.index
                gz_start.handle_type = "start"
                start_world = matrix @ (v0_co + start_handle)
                gz_start.matrix_basis = matrix.to_3x3().to_4x4()
                gz_start.matrix_basis.translation = start_world
                gizmo_idx += 1
            
            if edge.verts[1] == active_vert:
                if gizmo_idx >= len(self._gizmos):
                    self._ensure_gizmo_count(gizmo_idx + 1)
                gz_end = self._gizmos[gizmo_idx]
                gz_end.hide = False
                gz_end.target_edge_index = edge.index
                gz_end.handle_type = "end"
                end_world = matrix @ (v1_co + end_handle)
                gz_end.matrix_basis = matrix.to_3x3().to_4x4()
                gz_end.matrix_basis.translation = end_world
                gizmo_idx += 1
        
        self._active_count = gizmo_idx


class LoftHandlesTool(WorkSpaceTool):
    """Edit mode tool for manipulating loft handles"""
    
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'EDIT_MESH'
    bl_idname = "mesh_tool.loft_handles"
    bl_label = "Loft Handles"
    bl_description = "Edit Bezier handles for lofting curves between mesh edges"
    bl_icon = "ops.curve.draw"
    bl_widget = "MESH_GGT_loft_handles"
    bl_keymap = (
        ("mesh.initialize_loft_handles", {"type": 'H', "value": 'PRESS', "ctrl": True, "shift": True}, None),
        ("mesh.recalculate_loft_handles", {"type": 'H', "value": 'PRESS', "shift": True}, None),
    )

    def draw_settings(context, layout, tool):
        """Draw tool settings in the header."""
        layout.operator("mesh.initialize_loft_handles", text="Initialize")
        layout.operator("mesh.recalculate_loft_handles", text="Recalculate")
        layout.operator("mesh.clear_loft_handles", text="Clear")


_draw_handler = None


def register():
    """Register the gizmo system and draw handler."""
    global _draw_handler
    
    from procedural_human.gizmo.loft_handle_gizmo import LoftHandleGizmo
    bpy.utils.register_class(LoftHandleGizmo)
    
    from procedural_human.decorators.gizmo_decorator import procedural_gizmo_group
    _draw_handler = procedural_gizmo_group.register_draw_handler(
        "loft_bezier_curves",
        draw_bezier_curves,
        (),
        'POST_VIEW'
    )
    
    bpy.utils.register_tool(LoftHandlesTool, separator=True, group=False)
    
    logger.info("Loft Handle Gizmo System registered")


def unregister():
    """Unregister the gizmo system."""
    global _draw_handler
    
    try:
        bpy.utils.unregister_tool(LoftHandlesTool)
    except Exception:
        pass
    
    try:
        bpy.utils.unregister_class(LoftHandleGizmo)
    except Exception:
        pass
    
    from procedural_human.decorators.gizmo_decorator import procedural_gizmo_group
    procedural_gizmo_group.unregister_draw_handler("loft_bezier_curves")
    _draw_handler = None


if __name__ == "__main__":
    register()
