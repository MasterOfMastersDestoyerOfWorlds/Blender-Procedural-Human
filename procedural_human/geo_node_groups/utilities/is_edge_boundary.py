import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_is__edge__boundary_group():
    group_name = "Is Edge Boundary"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Is Edge Boundary", in_out="OUTPUT", socket_type="NodeSocketBool")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    compare.inputs[0].default_value = 0.0
    compare.inputs[1].default_value = 0.0
    compare.inputs[3].default_value = 1
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(edge_neighbors.outputs[0], compare.inputs[2])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.domain = "EDGE"
    evaluate_on_domain.data_type = "BOOLEAN"
    links.new(evaluate_on_domain.outputs[0], group_output.inputs[0])
    links.new(compare.outputs[0], evaluate_on_domain.inputs[0])

    auto_layout_nodes(group)
    return group
