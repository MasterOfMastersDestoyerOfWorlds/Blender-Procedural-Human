import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.armor.shoulders import create_shoulders_group
from procedural_human.geo_node_groups.armor.sleeves import create_sleeves_group
from procedural_human.geo_node_groups.armor.neck import create_neck_group
from procedural_human.geo_node_groups.armor.chest import create_chest_group
from procedural_human.geo_node_groups.utilities.mirror import create_mirror_group
from procedural_human.geo_node_groups.armor.blocker import create_blocker_group
from procedural_human.geo_node_groups.armor.waist import create_waist_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_armor_suit_group():
    group_name = "Armor Suit"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")

    set_material = nodes.new("GeometryNodeSetMaterial")
    set_material.inputs[1].default_value = True

    shoulders = nodes.new("GeometryNodeGroup")
    shoulders.node_tree = create_shoulders_group()
    shoulders.inputs[0].default_value = True
    links.new(shoulders.outputs[0], join_geometry_004.inputs[0])

    sleeves = nodes.new("GeometryNodeGroup")
    sleeves.node_tree = create_sleeves_group()
    sleeves.inputs[0].default_value = True
    links.new(sleeves.outputs[0], join_geometry_004.inputs[0])

    neck = nodes.new("GeometryNodeGroup")
    neck.node_tree = create_neck_group()
    neck.inputs[0].default_value = True
    links.new(neck.outputs[0], join_geometry_004.inputs[0])

    chest = nodes.new("GeometryNodeGroup")
    chest.node_tree = create_chest_group()
    chest.inputs[0].default_value = True
    links.new(chest.outputs[0], join_geometry_004.inputs[0])

    mirror = nodes.new("GeometryNodeGroup")
    mirror.node_tree = create_mirror_group()
    links.new(mirror.outputs[0], set_material.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(realize_instances.outputs[0], mirror.inputs[0])
    links.new(join_geometry_004.outputs[0], realize_instances.inputs[0])

    set_material_001 = nodes.new("GeometryNodeSetMaterial")
    links.new(set_material.outputs[0], set_material_001.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "BOOLEAN"
    named_attribute.inputs[0].default_value = "gold"
    links.new(named_attribute.outputs[0], set_material_001.inputs[1])

    set_material_002 = nodes.new("GeometryNodeSetMaterial")
    links.new(set_material_001.outputs[0], set_material_002.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.data_type = "BOOLEAN"
    named_attribute_001.inputs[0].default_value = "ruby"
    links.new(named_attribute_001.outputs[0], set_material_002.inputs[1])

    set_material_003 = nodes.new("GeometryNodeSetMaterial")
    links.new(set_material_002.outputs[0], set_material_003.inputs[0])

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.data_type = "BOOLEAN"
    named_attribute_002.inputs[0].default_value = "saphire"
    links.new(named_attribute_002.outputs[0], set_material_003.inputs[1])

    set_material_004 = nodes.new("GeometryNodeSetMaterial")
    links.new(set_material_003.outputs[0], set_material_004.inputs[0])

    named_attribute_003 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.data_type = "BOOLEAN"
    named_attribute_003.inputs[0].default_value = "fabric"
    links.new(named_attribute_003.outputs[0], set_material_004.inputs[1])

    set_material_005 = nodes.new("GeometryNodeSetMaterial")
    links.new(set_material_004.outputs[0], set_material_005.inputs[0])

    named_attribute_004 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.data_type = "BOOLEAN"
    named_attribute_004.inputs[0].default_value = "blocker"
    links.new(named_attribute_004.outputs[0], set_material_005.inputs[1])

    blocker = nodes.new("GeometryNodeGroup")
    blocker.node_tree = create_blocker_group()
    blocker.inputs[0].default_value = True
    links.new(blocker.outputs[0], join_geometry_004.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[1].default_value = True
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))

    waist = nodes.new("GeometryNodeGroup")
    waist.node_tree = create_waist_group()
    waist.inputs[0].default_value = True
    links.new(waist.outputs[0], join_geometry_004.inputs[0])

    named_attribute_005 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_005.data_type = "BOOLEAN"
    named_attribute_005.inputs[0].default_value = "skip"
    links.new(named_attribute_005.outputs[0], mirror.inputs[1])

    set_material_006 = nodes.new("GeometryNodeSetMaterial")
    links.new(set_material_005.outputs[0], set_material_006.inputs[0])
    links.new(set_material_006.outputs[0], group_output.inputs[0])

    named_attribute_006 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_006.data_type = "BOOLEAN"
    named_attribute_006.inputs[0].default_value = "rope"
    links.new(named_attribute_006.outputs[0], set_material_006.inputs[1])

    auto_layout_nodes(group)
    return group