import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_pipes_group():
    group_name = "Pipes"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Mesh", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    links.new(group_input.outputs[0], mesh_to_curve.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.inputs[2].default_value = 1.0
    curve_to_mesh_002.inputs[3].default_value = False
    links.new(mesh_to_curve.outputs[0], curve_to_mesh_002.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[0].default_value = 10
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle.inputs[4].default_value = 0.0020000000949949026
    links.new(curve_circle.outputs[0], curve_to_mesh_002.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "gold"
    store_named_attribute.inputs[3].default_value = True
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute.inputs[0])

    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "OR"
    links.new(boolean_math.outputs[0], mesh_to_curve.inputs[1])
    links.new(is_edge_boundary.outputs[0], boolean_math.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    compare.inputs[0].default_value = 0.0
    compare.inputs[1].default_value = 0.0
    compare.inputs[3].default_value = 0
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
    links.new(compare.outputs[0], boolean_math.inputs[1])

    auto_layout_nodes(group)
    return group
