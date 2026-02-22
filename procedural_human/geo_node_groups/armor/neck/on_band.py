import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from mathutils import Euler, Vector
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
def create_neck_on_band_group():
    group_name = "Neck_on_band"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.inputs[1].default_value = 100000.0
    gold_on_band.inputs[2].default_value = 8.669999122619629
    gold_on_band.inputs[3].default_value = 1


    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.domain = "FACE"


    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")


    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.operation = "GREATER_THAN"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    compare_002.inputs[1].default_value = 0.8700000047683716
    compare_002.inputs[2].default_value = 0
    compare_002.inputs[3].default_value = 0
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[8].default_value = ""
    compare_002.inputs[9].default_value = ""
    compare_002.inputs[10].default_value = 0.8999999761581421
    compare_002.inputs[11].default_value = 0.08726649731397629
    compare_002.inputs[12].default_value = 0.0010000000474974513


    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.operation = "LESS_THAN"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    compare_003.inputs[1].default_value = 0.25999999046325684
    compare_003.inputs[2].default_value = 0
    compare_003.inputs[3].default_value = 0
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[8].default_value = ""
    compare_003.inputs[9].default_value = ""
    compare_003.inputs[10].default_value = 0.8999999761581421
    compare_003.inputs[11].default_value = 0.08726649731397629
    compare_003.inputs[12].default_value = 0.0010000000474974513


    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "OR"


    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.operation = "OR"


    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    compare_004.inputs[1].default_value = 0.5
    compare_004.inputs[2].default_value = 0
    compare_004.inputs[3].default_value = 0
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[8].default_value = ""
    compare_004.inputs[9].default_value = ""
    compare_004.inputs[10].default_value = 0.8999999761581421
    compare_004.inputs[11].default_value = 0.08726649731397629
    compare_004.inputs[12].default_value = 0.020999997854232788


    frame_001 = nodes.new("NodeFrame")
    frame_001.label = "On Band"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20


    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.operation = "AND"


    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.operation = "LESS_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    compare_005.inputs[1].default_value = 0.5
    compare_005.inputs[2].default_value = 0
    compare_005.inputs[3].default_value = 0
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[8].default_value = ""
    compare_005.inputs[9].default_value = ""
    compare_005.inputs[10].default_value = 0.8999999761581421
    compare_005.inputs[11].default_value = 0.08726649731397629
    compare_005.inputs[12].default_value = 0.020999997854232788


    # Parent assignments
    boolean_math.parent = frame_001
    boolean_math_001.parent = frame_001
    boolean_math_002.parent = frame_001
    compare_002.parent = frame_001
    compare_003.parent = frame_001
    compare_004.parent = frame_001
    compare_005.parent = frame_001
    gold_on_band.parent = frame_001
    separate_geometry_001.parent = frame_001
    separate_x_y_z_003.parent = frame_001

    # Internal links
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])
    links.new(separate_x_y_z_003.outputs[0], compare_002.inputs[0])
    links.new(separate_x_y_z_003.outputs[0], compare_003.inputs[0])
    links.new(compare_002.outputs[0], boolean_math.inputs[0])
    links.new(compare_003.outputs[0], boolean_math.inputs[1])
    links.new(boolean_math.outputs[0], boolean_math_001.inputs[0])
    links.new(separate_x_y_z_003.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_001.inputs[1])
    links.new(boolean_math_002.outputs[0], separate_geometry_001.inputs[1])
    links.new(boolean_math_001.outputs[0], boolean_math_002.inputs[0])
    links.new(separate_x_y_z_003.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], boolean_math_002.inputs[1])

    links.new(gold_on_band.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
