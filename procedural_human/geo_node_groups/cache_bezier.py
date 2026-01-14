import bpy
from procedural_human.geo_node_groups.node_helpers import *

def get_precompute_edge_data_group():
    """Creates or retrieves a singleton Node Group that precomputes Bezier control points for all edges.
    
    The node group calculates P0, P1, P2, P3 for every edge in the 'canonical' direction
    (Vertex 1 to Vertex 2) and stores them as Named Attributes on the Edge Domain.
    It samples vertex positions, reconstructs handle vectors from scalar attributes,
    and stores the four control points as edge_cache_p0, edge_cache_p1, edge_cache_p2, edge_cache_p3.
    
    :returns: The node group for precomputing edge Bezier control points.
    """
    group_name = "Math_PrecomputeEdgeData"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    ng = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    ng.interface.new_socket("orig_geo", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Result", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    
    # Internal Logic
    in_node = ng.nodes.new("NodeGroupInput")
    out_node = ng.nodes.new("NodeGroupOutput")
    
    # 1. Get Vertex Positions
    pos_node = ng.nodes.new("GeometryNodeInputPosition")
    edge_verts = ng.nodes.new("GeometryNodeInputMeshEdgeVertices")
    
    # Sample Position of Vertex 1
    s_v1 = create_node(ng, "GeometryNodeSampleIndex", {
        "Geometry": in_node.outputs["orig_geo"], "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
        "Index": edge_verts.outputs["Vertex Index 1"]
    })
    link_or_set(ng, s_v1.inputs["Value"], pos_node.outputs[0])
    
    # Sample Position of Vertex 2
    s_v2 = create_node(ng, "GeometryNodeSampleIndex", {
        "Geometry": in_node.outputs["orig_geo"], "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
        "Index": edge_verts.outputs["Vertex Index 2"]
    })
    link_or_set(ng, s_v2.inputs["Value"], pos_node.outputs[0])
    
    P0_can = s_v1.outputs[0]
    P3_can = s_v2.outputs[0]
    
    # 2. Reconstruct Handles from Scalar Attributes (x, y, z)
    def get_handle_vec(prefix):
        x = get_attr(ng, f"{prefix}_x", "FLOAT")
        y = get_attr(ng, f"{prefix}_y", "FLOAT")
        z = get_attr(ng, f"{prefix}_z", "FLOAT")
        comb = ng.nodes.new("ShaderNodeCombineXYZ")
        ng.links.new(x, comb.inputs["X"])
        ng.links.new(y, comb.inputs["Y"])
        ng.links.new(z, comb.inputs["Z"])
        return comb.outputs[0]
    
    h_start = get_handle_vec("handle_start") # Relative to V1
    h_end = get_handle_vec("handle_end")     # Relative to V2
    
    P1_can = vec_math_op(ng, "ADD", P0_can, h_start)
    P2_can = vec_math_op(ng, "ADD", P3_can, h_end)
    
    # 3. Store these on the Edge Domain
    def store_vec(geo, name, val):
        s = create_node(ng, "GeometryNodeStoreNamedAttribute", {
            "Geometry": geo, "Name": name, "Domain": "EDGE", "Data Type": "FLOAT_VECTOR", "Value": val
        })
        return s.outputs[0]
    
    g1 = store_vec(in_node.outputs["orig_geo"], "edge_cache_p0", P0_can)
    g2 = store_vec(g1, "edge_cache_p1", P1_can)
    g3 = store_vec(g2, "edge_cache_p2", P2_can)
    g4 = store_vec(g3, "edge_cache_p3", P3_can)
    
    ng.links.new(g4, out_node.inputs["Result"])
    return ng

def precompute_edge_data_node(group, orig_geo):
    """Instantiates the precompute edge data node group to cache Bezier control points for all edges.
    
    :param group: The node group to add the node to.
    :param orig_geo: Original geometry to process (socket or geometry).
    :returns: Output socket with geometry containing cached edge control points as attributes.
    """
    ped = get_precompute_edge_data_group()
    n = group.nodes.new("GeometryNodeGroup")
    n.node_tree = ped
    
    link_or_set(group, n.inputs["orig_geo"], orig_geo)
    return n.outputs["Result"]


def get_sample_cached_bezier_group():
    """Creates or retrieves a singleton Node Group that samples precomputed Bezier control points.
    
    The node group is an optimized replacement for edge_control_points_node. It samples
    the pre-computed edge_cache_p0, edge_cache_p1, edge_cache_p2, edge_cache_p3 attributes
    and swaps them based on edge direction. If forward, returns points in canonical order.
    If backward, reverses the order (P0=cP3, P1=cP2, P2=cP1, P3=cP0).
    
    :returns: The node group for sampling cached Bezier control points.
    """
    group_name = "Math_SampleCachedBezier"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    ng = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    ng.interface.new_socket("edge_idx", in_out="INPUT", socket_type="NodeSocketInt")
    ng.interface.new_socket("is_fwd", in_out="INPUT", socket_type="NodeSocketBool")
    ng.interface.new_socket("source_geo", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("P0", in_out="OUTPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P1", in_out="OUTPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P2", in_out="OUTPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P3", in_out="OUTPUT", socket_type="NodeSocketVector")
    
    # Internal Logic
    in_node = ng.nodes.new("NodeGroupInput")
    out_node = ng.nodes.new("NodeGroupOutput")
    
    def samp(name):
        s = create_node(ng, "GeometryNodeSampleIndex", {
            "Geometry": in_node.outputs["source_geo"], "Domain": "EDGE", "Data Type": "FLOAT_VECTOR",
            "Index": in_node.outputs["edge_idx"]
        })
        # Use simple Named Attribute input for the Value
        attr = ng.nodes.new("GeometryNodeInputNamedAttribute")
        attr.data_type = "FLOAT_VECTOR"
        attr.inputs["Name"].default_value = name
        ng.links.new(attr.outputs[0], s.inputs["Value"])
        return s.outputs[0]
    
    c_p0 = samp("edge_cache_p0")
    c_p1 = samp("edge_cache_p1")
    c_p2 = samp("edge_cache_p2")
    c_p3 = samp("edge_cache_p3")
    
    # If Forward: P0=cP0, P1=cP1...
    # If Backward: P0=cP3, P1=cP2, P2=cP1, P3=cP0
    
    final_p0 = switch_vec(ng, in_node.outputs["is_fwd"], c_p3, c_p0)
    final_p1 = switch_vec(ng, in_node.outputs["is_fwd"], c_p2, c_p1)
    final_p2 = switch_vec(ng, in_node.outputs["is_fwd"], c_p1, c_p2)
    final_p3 = switch_vec(ng, in_node.outputs["is_fwd"], c_p0, c_p3)
    
    ng.links.new(final_p0, out_node.inputs["P0"])
    ng.links.new(final_p1, out_node.inputs["P1"])
    ng.links.new(final_p2, out_node.inputs["P2"])
    ng.links.new(final_p3, out_node.inputs["P3"])
    return ng

def sample_cached_bezier_node(group, edge_idx, is_fwd, source_geo):
    """Instantiates the sample cached Bezier node group to retrieve precomputed control points.
    
    :param group: The node group to add the node to.
    :param edge_idx: Edge index to sample (socket or int).
    :param is_fwd: Forward direction boolean (socket or bool). If True, returns points in canonical order; if False, reverses order.
    :param source_geo: Geometry containing the cached edge control points (socket or geometry).
    :returns: Tuple of (P0, P1, P2, P3) control point output sockets.
    """
    scb = get_sample_cached_bezier_group()
    n = group.nodes.new("GeometryNodeGroup")
    n.node_tree = scb
    
    link_or_set(group, n.inputs["edge_idx"], edge_idx)
    link_or_set(group, n.inputs["is_fwd"], is_fwd)
    link_or_set(group, n.inputs["source_geo"], source_geo)
    return n.outputs["P0"], n.outputs["P1"], n.outputs["P2"], n.outputs["P3"]