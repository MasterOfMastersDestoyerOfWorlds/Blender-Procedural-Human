import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group

@geo_node_group
def create_pipes_group():
    group_name = "Pipes"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Mesh", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (520.0, 60.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-200.0, 80.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (40.0, 60.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Links for mesh_to_curve
    links.new(group_input.outputs[0], mesh_to_curve.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Group.003"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (-380.0, -140.0)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (200.0, 60.0)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_002.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(mesh_to_curve.outputs[0], curve_to_mesh_002.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (200.0, -80.0)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 10
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.0020000000949949026
    # Links for curve_circle
    links.new(curve_circle.outputs[0], curve_to_mesh_002.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (360.0, 60.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute.inputs[0])

    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"
    edge_neighbors.label = ""
    edge_neighbors.location = (-380.0, -240.0)
    edge_neighbors.bl_label = "Edge Neighbors"
    # Links for edge_neighbors

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (-200.0, -100.0)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(boolean_math.outputs[0], mesh_to_curve.inputs[1])
    links.new(is_edge_boundary.outputs[0], boolean_math.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-200.0, -240.0)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # B
    compare.inputs[3].default_value = 0
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
    links.new(compare.outputs[0], boolean_math.inputs[1])

    auto_layout_nodes(group)
    return group
