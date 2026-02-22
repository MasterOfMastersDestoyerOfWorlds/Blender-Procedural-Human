from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.armor.neck.centre_profile import create_neck_centre_profile_group
from procedural_human.geo_node_groups.armor.neck.neck_rails import create_neck_neck_rails_group
from procedural_human.geo_node_groups.armor.neck.side_profile import create_neck_side_profile_group
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_neck_group():
    group_name = "Neck"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    nodes = group.nodes
    links = group.links

    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    centre_profile = nodes.new("GeometryNodeGroup")
    centre_profile.node_tree = create_neck_centre_profile_group()

    side_profile = nodes.new("GeometryNodeGroup")
    side_profile.node_tree = create_neck_side_profile_group()

    neck_rails = nodes.new("GeometryNodeGroup")
    neck_rails.node_tree = create_neck_neck_rails_group()

    profile_join = nodes.new("GeometryNodeJoinGeometry")
    links.new(centre_profile.outputs[0], profile_join.inputs[0])
    links.new(side_profile.outputs[0], profile_join.inputs[0])

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.node_tree = create_bi_rail_loft_group()
    bi_rail_loft.inputs[3].default_value = 0
    bi_rail_loft.inputs[4].default_value = "Resolution"
    bi_rail_loft.inputs[5].default_value = 0.009999999776482582
    bi_rail_loft.inputs[6].default_value = 0.029999999329447746
    bi_rail_loft.inputs[7].default_value = 42
    bi_rail_loft.inputs[8].default_value = 148

    links.new(neck_rails.outputs[0], bi_rail_loft.inputs[0])
    links.new(neck_rails.outputs[1], bi_rail_loft.inputs[1])
    links.new(profile_join.outputs[0], bi_rail_loft.inputs[2])
    links.new(bi_rail_loft.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group