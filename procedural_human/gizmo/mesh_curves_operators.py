
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

import time
import numpy as np

from procedural_human.gizmo.mesh_curves_gizmo import *
ATTR_HANDLE_LEFT = "handle_left"
ATTR_HANDLE_RIGHT = "handle_right"
QUARTER_CIRCLE_RATIO = 0.5523  # 4 * (sqrt(2) - 1) / 3



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
    other_dirs = []
    for other_edge in vert.link_edges:
        if other_edge != edge:
            other_vert = other_edge.other_vert(vert)
            other_dir = (other_vert.co - vert.co).normalized()
            other_dirs.append(other_dir)
    
    if other_dirs:
        avg_dir = Vector((0, 0, 0))
        for d in other_dirs:
            avg_dir += d
        avg_dir /= len(other_dirs)
        
        if avg_dir.length > 0.0001:
            return -avg_dir.normalized() * handle_len  # NEGATE to point outward
    edge_vec = edge.other_vert(vert).co - vert.co
    edge_dir = edge_vec.normalized()
    outward = vert.co - mesh_center
    if outward.length < 0.0001:
        outward = Vector((0, 0, 1))
    else:
        outward.normalize()
    outward_perp = outward - edge_dir * outward.dot(edge_dir)
    if outward_perp.length > 0.0001:
        return outward_perp.normalized() * handle_len
    if vert.normal.length > 0:
        return vert.normal.normalized() * handle_len
    
    return Vector((0, 0, 1)) * handle_len

def ensure_edge_layers(bm):
    """
    Ensure BMesh has the required float layers for per-edge handle data.
    Each edge has 2 handles: start (at verts[0]) and end (at verts[1]).
    
    Args:
        bm: The BMesh object
        
    Returns:
        Tuple of (start_x, start_y, start_z, end_x, end_y, end_z) layer references
    """
    start_x = bm.edges.layers.float.get(LAYER_HANDLE_START_X)
    if start_x is None:
        start_x = bm.edges.layers.float.new(LAYER_HANDLE_START_X)
    
    start_y = bm.edges.layers.float.get(LAYER_HANDLE_START_Y)
    if start_y is None:
        start_y = bm.edges.layers.float.new(LAYER_HANDLE_START_Y)
    
    start_z = bm.edges.layers.float.get(LAYER_HANDLE_START_Z)
    if start_z is None:
        start_z = bm.edges.layers.float.new(LAYER_HANDLE_START_Z)
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
            set_edge_handles(edge, layers, Vector((0, 0, 0)), Vector((0, 0, 0)))
            continue
        handle_len = edge_len * QUARTER_CIRCLE_RATIO
        start_handle = _calculate_handle_for_vertex(edge, v0, mesh_center, handle_len)
        end_handle = _calculate_handle_for_vertex(edge, v1, mesh_center, handle_len)
        
        set_edge_handles(edge, layers, start_handle, end_handle)
    for vert in bm.verts:
        make_handles_coplanar_at_vertex(vert, layers)


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
    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(mesh)
        calculate_auto_handles_bmesh(bm)
        bmesh.update_edit_mesh(mesh)
        return
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
        if context.mode != 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='EDIT')
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
        try:
            bm = bmesh.from_edit_mesh(obj.data)
            return has_edge_handle_layers(bm)
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
            return has_edge_handle_layers(bm)
        except Exception:
            return False
    
    def execute(self, context):
        obj = context.object
        mesh = obj.data
        
        bm = bmesh.from_edit_mesh(mesh)
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
