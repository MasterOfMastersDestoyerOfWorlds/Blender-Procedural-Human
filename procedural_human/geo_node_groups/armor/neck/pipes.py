import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group
from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold__decorations_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_neck_pipes_group():
    group_name = "Neck_pipes"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    pipes = nodes.new("GeometryNodeGroup")
    pipes.node_tree = create_pipes_group()


    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")


    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[1].default_value = 0.8799999356269836
    compare_001.inputs[2].default_value = 0
    compare_001.inputs[3].default_value = 0
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[8].default_value = ""
    compare_001.inputs[9].default_value = ""
    compare_001.inputs[10].default_value = 0.8999999761581421
    compare_001.inputs[11].default_value = 0.08726649731397629
    compare_001.inputs[12].default_value = 0.02099999599158764


    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "POINT"


    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")


    frame = nodes.new("NodeFrame")
    frame.label = "Pipes"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20


    # Parent assignments
    compare_001.parent = frame
    join_geometry_001.parent = frame
    pipes.parent = frame
    separate_geometry.parent = frame
    separate_x_y_z_002.parent = frame

    # Internal links
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])
    links.new(compare_001.outputs[0], separate_geometry.inputs[1])
    links.new(join_geometry_001.outputs[0], pipes.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_001.inputs[0])

    links.new(pipes.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
