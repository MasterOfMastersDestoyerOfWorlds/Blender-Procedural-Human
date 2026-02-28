import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_attr, create_node, get_or_rebuild_node_group


@geo_node_group
def create_store_attributes_on_points_group():
    group_name = "StoreAttributesOnPoints"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")

    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    nodes = group.nodes
    links = group.links

    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    # Convert curve to points (single point per curve)
    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.mode = "COUNT"
    curve_to_points.inputs[1].default_value = 1
    curve_to_points.inputs[2].default_value = 0.1
    links.new(group_input.outputs[0], curve_to_points.inputs[0])

    # Index for sampling
    index = nodes.new("GeometryNodeInputIndex")

    # Sample and store handle_left attribute
    handle_left_attr = get_attr(group, "FLOAT_VECTOR", "handle_left")
    sample_left = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": group_input.outputs[0],
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": handle_left_attr,
        "Index": index.outputs[0]
    })

    store_left = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": curve_to_points.outputs[0],
        "Name": "handle_left",
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": sample_left.outputs[0]
    })
    store_left.inputs[1].default_value = True

    # Sample and store handle_right attribute
    handle_right_attr = get_attr(group, "FLOAT_VECTOR", "handle_right")
    sample_right = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": group_input.outputs[0],
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": handle_right_attr,
        "Index": index.outputs[0]
    })

    store_right = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": store_left.outputs[0],
        "Name": "handle_right",
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": sample_right.outputs[0]
    })
    store_right.inputs[1].default_value = True

    # Sample and store handle_start from input Value (index 1)
    sample_start = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": group_input.outputs[0],
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": group_input.outputs[1],
        "Index": index.outputs[0]
    })

    store_start = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": store_right.outputs[0],
        "Name": "handle_start",
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": sample_start.outputs[0]
    })
    store_start.inputs[1].default_value = True

    # Sample and store handle_end from input Value (index 2)
    sample_end = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": group_input.outputs[0],
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": group_input.outputs[2],
        "Index": index.outputs[0]
    })

    store_end = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": store_start.outputs[0],
        "Name": "handle_end",
        "Domain": "POINT",
        "Data Type": "FLOAT_VECTOR",
        "Value": sample_end.outputs[0]
    })
    store_end.inputs[1].default_value = True

    # Convert points to vertices
    points_to_verts = nodes.new("GeometryNodePointsToVertices")
    points_to_verts.inputs[1].default_value = True
    links.new(store_end.outputs[0], points_to_verts.inputs[0])
    links.new(points_to_verts.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
