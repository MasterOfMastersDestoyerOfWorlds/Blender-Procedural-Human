"""
Custom Gizmo for Loft Handle manipulation.

Handles mouse interaction and undo buffer management for Bezier handle editing.
"""

import bpy
import bmesh
import gpu
import gpu.matrix
import math
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils
from bpy.types import Gizmo
from mathutils import Vector, Matrix
from procedural_human.gizmo.mesh_curves_gizmo import get_edge_layers
from procedural_human.logger import logger

HANDLE_COLOR = (1.0, 0.4, 0.1)
HANDLE_COLOR_SELECTED = (1.0, 0.8, 0.2)


class LoftHandleGizmo(Gizmo):
    """Custom gizmo for editing Bezier handles on mesh edges."""
    
    bl_idname = "GIZMO_GT_loft_handle"
    bl_label = "Loft Handle"
    bl_options = {'3D', 'PERSISTENT', 'DEPTH_3D'}
    
    def setup(self):
        """Initialize gizmo properties."""
        self.target_edge_index = -1
        self.handle_type = "start"
        self.baseline_pos = Vector((0, 0, 0))
        self.drag_start_mouse = Vector((0, 0))
        self.drag_start_handle = Vector((0, 0, 0))
        self.is_dragging = False
        self.has_moved = False
        
        self.scale_basis = 0.1
        self.color = HANDLE_COLOR
        self.alpha = 1.0
        self.color_highlight = HANDLE_COLOR_SELECTED
        self.alpha_highlight = 1.0
        self.use_draw_modal = True
    
    def draw(self, context):
        """Draw the gizmo handle."""
        if self.target_edge_index < 0 or self.hide:
            return
        
        gpu.state.depth_test_set('NONE')
        shape = self._get_custom_shape()
        if shape:
            rv3d = context.space_data.region_3d
            view_inv = rv3d.view_matrix.inverted()
            matrix = view_inv.to_3x3().to_4x4()
            matrix.translation = self.matrix_basis.translation
            self.draw_custom_shape(shape, matrix=matrix)
        gpu.state.depth_test_set('LESS_EQUAL')
    
    def draw_select(self, context, select_id):
        """Draw selection shape for picking."""
        if self.target_edge_index < 0 or self.hide:
            return
        
        gpu.state.depth_test_set('NONE')
        shape = self._get_custom_shape()
        if shape:
            rv3d = context.space_data.region_3d
            view_inv = rv3d.view_matrix.inverted()
            matrix = view_inv.to_3x3().to_4x4()
            matrix.translation = self.matrix_basis.translation
            self.draw_custom_shape(shape, matrix=matrix, select_id=select_id)
        gpu.state.depth_test_set('LESS_EQUAL')
    
    def _get_custom_shape(self):
        """Get or create the custom shape for this gizmo as a circle (triangle fan)."""
        scale = self.scale_basis
        num_segments = 32
        
        coords = []
        center = [0.0, 0.0, 0.0]
        
        for i in range(num_segments):
            angle = (i / num_segments) * 2.0 * math.pi
            x = scale * math.cos(angle)
            y = scale * math.sin(angle)
            z = 0.0
            coords.append([x, y, z])
        
        coords_list = []
        for i in range(num_segments):
            next_i = (i + 1) % num_segments
            coords_list.append(center)
            coords_list.append(coords[i])
            coords_list.append(coords[next_i])
        
        return self.new_custom_shape('TRIS', coords_list)
    
    def invoke(self, context, event):
        """Called when gizmo interaction starts."""
        if event.type != 'LEFTMOUSE' or event.value != 'PRESS':
            return {'PASS_THROUGH'}
        
        from procedural_human.gizmo.mesh_curves_gizmo import (
            get_edge_layers,
            get_edge_handles,
            _capture_all_handles_at_vertex,
        )
        
        if self.target_edge_index < 0:
            return {'CANCELLED'}
        
        obj = context.object
        if not obj or obj.type != 'MESH' or context.mode != 'EDIT_MESH':
            return {'CANCELLED'}
        
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        layers = get_edge_layers(bm)
        
        if not layers:
            return {'CANCELLED'}
        
        bm.edges.ensure_lookup_table()
        edge = bm.edges[self.target_edge_index]
        
        start_handle, end_handle = get_edge_handles(edge, layers)
        current_handle = start_handle if self.handle_type == "start" else end_handle
        
        self.drag_start_mouse = Vector((event.mouse_region_x, event.mouse_region_y))
        self.drag_start_handle = current_handle.copy()
        self.baseline_pos = self.matrix_basis.translation.copy()
        self.is_dragging = True
        self.has_moved = False
        
        baseline_key = (self.target_edge_index, self.handle_type)
        self.baselines_dict = {}
        self.baselines_dict[baseline_key] = current_handle.copy()
        
        vert = edge.verts[0] if self.handle_type == "start" else edge.verts[1]
        from procedural_human.gizmo.mesh_curves_gizmo import _capture_all_handles_at_vertex
        _capture_all_handles_at_vertex(vert, layers, self.baselines_dict)
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event, tweak):
        """Handle modal interaction."""
        if not self.is_dragging:
            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                return {'FINISHED'}
            return {'PASS_THROUGH'}
        
        if event.type == 'MOUSEMOVE':
            result = self._handle_mousemove(context, event)
            if result:
                return result

        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            return self._handle_cancel(context, event)
        
        return {'RUNNING_MODAL'}
    
    def _handle_mousemove(self, context, event):
        """Handle mouse movement during drag."""
        obj = context.object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        layers = get_edge_layers(bm)
        
        if not layers:
            return None
        
        bm.edges.ensure_lookup_table()
        edge = bm.edges[self.target_edge_index]
        vert = edge.verts[0] if self.handle_type == "start" else edge.verts[1]
        
        region = context.region
        region_3d = context.space_data.region_3d
        
        mouse_current = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_delta = mouse_current - self.drag_start_mouse
        
        if mouse_delta.length < 0.1:
            return None
        
        self.has_moved = True
        
        world_pos_start = self.baseline_pos
        start_2d = view3d_utils.location_3d_to_region_2d(region, region_3d, world_pos_start)
        
        if start_2d is None:
            return None
        
        end_2d = start_2d + mouse_delta
        
        end_3d = view3d_utils.region_2d_to_location_3d(region, region_3d, end_2d, world_pos_start)
        
        if end_3d is None:
            return None
        
        world_delta = end_3d - world_pos_start
        
        matrix = obj.matrix_world
        rot_inv = matrix.to_3x3().inverted()
        local_delta = rot_inv @ world_delta
        
        new_handle = self.drag_start_handle + local_delta
        
        from procedural_human.gizmo.mesh_curves_gizmo import _rotate_coplanar_handles
        
        _rotate_coplanar_handles(
            vert, self.target_edge_index, self.handle_type,
            self.drag_start_handle, new_handle, bm, layers, self.baselines_dict
        )
        
        if self.handle_type == "start":
            start_x, start_y, start_z, _, _, _ = layers
            edge[start_x] = new_handle.x
            edge[start_y] = new_handle.y
            edge[start_z] = new_handle.z
        else:
            _, _, _, end_x, end_y, end_z = layers
            edge[end_x] = new_handle.x
            edge[end_y] = new_handle.y
            edge[end_z] = new_handle.z
        
        bmesh.update_edit_mesh(mesh)
        
        self.matrix_basis.translation = matrix @ (vert.co + new_handle)
        
        return None

    def _handle_cancel(self, context, event):
        """Handle cancel - restore all handles to original positions."""
        obj = context.object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        layers = get_edge_layers(bm)
        
        if layers and hasattr(self, 'baselines_dict'):
            from procedural_human.gizmo.mesh_curves_gizmo import _set_handle_at_vertex
            
            bm.edges.ensure_lookup_table()
            for (edge_index, handle_type), baseline_handle in self.baselines_dict.items():
                edge = bm.edges[edge_index]
                _set_handle_at_vertex(edge, handle_type, baseline_handle, layers)
            
            bmesh.update_edit_mesh(mesh)
        
        self.is_dragging = False
        self.has_moved = False
        return {'CANCELLED'}
    
    def exit(self, context, cancel):
        """Called when gizmo interaction ends."""
        if cancel:
            if self.is_dragging:
                self._handle_cancel(context, None)
        else:
            if self.is_dragging and self.has_moved:
                logger.info("DEBUG: Saving Undo Step: Move Loft Handle")
                try:
                    bpy.ops.ed.undo_push()
                except Exception as e:
                    logger.error(f"Failed to push undo step: {e}")
        
        self.is_dragging = False
        self.has_moved = False
