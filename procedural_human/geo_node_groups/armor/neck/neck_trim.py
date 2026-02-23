import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from mathutils import Euler, Vector
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.utils.node_layout import auto_layout_nodes

@geo_node_group
def create_neck_trim_group():
    group_name = "NeckTrim"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Selection", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1055.0, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1065.0, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (625.0, -28.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    # Links for delete_geometry

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (465.0, -188.0)
    position_001.bl_label = "Position"
    # Links for position_001

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (465.0, -248.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_001.outputs[0], separate_x_y_z_001.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (625.0, -188.0)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.0
    # A
    compare.inputs[2].default_value = 0
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
    links.new(compare.outputs[0], delete_geometry.inputs[1])
    links.new(separate_x_y_z_001.outputs[0], compare.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (750.0, -96.0)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (265.0, -48.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(pipes.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], delete_geometry.inputs[0])
    links.new(group_input.outputs[0], join_geometry.inputs[0])

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (30.0, -36.0)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(group_input.outputs[1], separate_x_y_z_002.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (190.0, -36.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.8799999356269836
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.02099999599158764
    # Links for compare_001
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (350.0, -36.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "POINT"
    # Links for separate_geometry
    links.new(compare_001.outputs[0], separate_geometry.inputs[1])
    links.new(group_input.outputs[0], separate_geometry.inputs[0])
    links.new(separate_geometry.outputs[0], group_output.inputs[0])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (550.0, -76.0)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry_001.outputs[0], pipes.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_001.inputs[0])
    links.new(group_input.outputs[0], join_geometry_001.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Pipes"
    frame.location = (-865.0, 248.0)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    rivet = nodes.new("GeometryNodeGroup")
    rivet.name = "Rivet"
    rivet.label = ""
    rivet.location = (-695.0, -248.0)
    rivet.node_tree = create_rivet_group()
    rivet.bl_label = "Group"
    # Corners
    rivet.inputs[1].default_value = False
    # Offset
    rivet.inputs[2].default_value = -1.059999942779541
    # Spacing
    rivet.inputs[3].default_value = 0.9399999976158142
    # Links for rivet
    links.new(group_input.outputs[0], rivet.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (-515.0, -248.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], join_geometry.inputs[0])
    links.new(rivet.outputs[0], realize_instances.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (865.0, -28.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(delete_geometry.outputs[0], set_shade_smooth.inputs[0])
    links.new(set_shade_smooth.outputs[0], group_output.inputs[1])

    # Parent assignments
    pipes.parent = frame
    separate_x_y_z_002.parent = frame
    compare_001.parent = frame
    separate_geometry.parent = frame
    join_geometry_001.parent = frame

    auto_layout_nodes(group)
    return group