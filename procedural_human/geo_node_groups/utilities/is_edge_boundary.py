import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group

@geo_node_group
def create_is__edge__boundary_group():
    group_name = "Is Edge Boundary"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Is Edge Boundary", in_out="OUTPUT", socket_type="NodeSocketBool")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (320.0, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"
    edge_neighbors.label = ""
    edge_neighbors.location = (-279.9999694824219, 0.0)
    edge_neighbors.bl_label = "Edge Neighbors"
    # Links for edge_neighbors

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-80.0, 0.0)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # B
    compare.inputs[3].default_value = 1
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(edge_neighbors.outputs[0], compare.inputs[2])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.label = ""
    evaluate_on_domain.location = (119.99999237060547, 0.0)
    evaluate_on_domain.bl_label = "Evaluate on Domain"
    evaluate_on_domain.domain = "EDGE"
    evaluate_on_domain.data_type = "BOOLEAN"
    # Links for evaluate_on_domain
    links.new(evaluate_on_domain.outputs[0], group_output.inputs[0])
    links.new(compare.outputs[0], evaluate_on_domain.inputs[0])

    auto_layout_nodes(group)
    return group
