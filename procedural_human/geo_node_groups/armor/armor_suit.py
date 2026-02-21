import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
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

@geo_node_group
def create_armor_suit_group():
    group_name = "Armor Suit"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (10880.0, -1300.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (9280.0, -1300.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004

    set_material = nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    set_material.label = ""
    set_material.location = (9760.0, -1300.0)
    set_material.bl_label = "Set Material"
    # Selection
    set_material.inputs[1].default_value = True
    # Links for set_material

    shoulders = nodes.new("GeometryNodeGroup")
    shoulders.name = "Group.004"
    shoulders.label = ""
    shoulders.location = (9060.0, -1460.0)
    shoulders.node_tree = create_shoulders_group()
    shoulders.bl_label = "Group"
    # Decor
    shoulders.inputs[0].default_value = True
    # Links for shoulders
    links.new(shoulders.outputs[0], join_geometry_004.inputs[0])

    sleeves = nodes.new("GeometryNodeGroup")
    sleeves.name = "Group.005"
    sleeves.label = ""
    sleeves.location = (9060.0, -1360.0)
    sleeves.node_tree = create_sleeves_group()
    sleeves.bl_label = "Group"
    # Decor
    sleeves.inputs[0].default_value = True
    # Links for sleeves
    links.new(sleeves.outputs[0], join_geometry_004.inputs[0])

    neck = nodes.new("GeometryNodeGroup")
    neck.name = "Group.006"
    neck.label = ""
    neck.location = (9060.0, -1060.0)
    neck.node_tree = create_neck_group()
    neck.bl_label = "Group"
    # Decor
    neck.inputs[0].default_value = True
    # Links for neck
    links.new(neck.outputs[0], join_geometry_004.inputs[0])

    chest = nodes.new("GeometryNodeGroup")
    chest.name = "Group.002"
    chest.label = ""
    chest.location = (9060.0, -1160.0)
    chest.node_tree = create_chest_group()
    chest.bl_label = "Group"
    # Decor
    chest.inputs[0].default_value = True
    # Links for chest
    links.new(chest.outputs[0], join_geometry_004.inputs[0])

    mirror = nodes.new("GeometryNodeGroup")
    mirror.name = "Group"
    mirror.label = ""
    mirror.location = (9600.0, -1300.0)
    mirror.node_tree = create_mirror_group()
    mirror.bl_label = "Group"
    # Links for mirror
    links.new(mirror.outputs[0], set_material.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (9440.0, -1300.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], mirror.inputs[0])
    links.new(join_geometry_004.outputs[0], realize_instances.inputs[0])

    set_material_001 = nodes.new("GeometryNodeSetMaterial")
    set_material_001.name = "Set Material.001"
    set_material_001.label = ""
    set_material_001.location = (9920.0, -1300.0)
    set_material_001.bl_label = "Set Material"
    # Links for set_material_001
    links.new(set_material.outputs[0], set_material_001.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (9920.0, -1400.0)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Name
    named_attribute.inputs[0].default_value = "gold"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], set_material_001.inputs[1])

    set_material_002 = nodes.new("GeometryNodeSetMaterial")
    set_material_002.name = "Set Material.002"
    set_material_002.label = ""
    set_material_002.location = (10080.0, -1300.0)
    set_material_002.bl_label = "Set Material"
    # Links for set_material_002
    links.new(set_material_001.outputs[0], set_material_002.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (10080.0, -1400.0)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "BOOLEAN"
    # Name
    named_attribute_001.inputs[0].default_value = "ruby"
    # Links for named_attribute_001
    links.new(named_attribute_001.outputs[0], set_material_002.inputs[1])

    set_material_003 = nodes.new("GeometryNodeSetMaterial")
    set_material_003.name = "Set Material.003"
    set_material_003.label = ""
    set_material_003.location = (10240.0, -1300.0)
    set_material_003.bl_label = "Set Material"
    # Links for set_material_003
    links.new(set_material_002.outputs[0], set_material_003.inputs[0])

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.label = ""
    named_attribute_002.location = (10240.0, -1400.0)
    named_attribute_002.bl_label = "Named Attribute"
    named_attribute_002.data_type = "BOOLEAN"
    # Name
    named_attribute_002.inputs[0].default_value = "saphire"
    # Links for named_attribute_002
    links.new(named_attribute_002.outputs[0], set_material_003.inputs[1])

    set_material_004 = nodes.new("GeometryNodeSetMaterial")
    set_material_004.name = "Set Material.004"
    set_material_004.label = ""
    set_material_004.location = (10400.0, -1300.0)
    set_material_004.bl_label = "Set Material"
    # Links for set_material_004
    links.new(set_material_003.outputs[0], set_material_004.inputs[0])

    named_attribute_003 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.label = ""
    named_attribute_003.location = (10400.0, -1400.0)
    named_attribute_003.bl_label = "Named Attribute"
    named_attribute_003.data_type = "BOOLEAN"
    # Name
    named_attribute_003.inputs[0].default_value = "fabric"
    # Links for named_attribute_003
    links.new(named_attribute_003.outputs[0], set_material_004.inputs[1])

    set_material_005 = nodes.new("GeometryNodeSetMaterial")
    set_material_005.name = "Set Material.005"
    set_material_005.label = ""
    set_material_005.location = (10560.0, -1300.0)
    set_material_005.bl_label = "Set Material"
    # Links for set_material_005
    links.new(set_material_004.outputs[0], set_material_005.inputs[0])

    named_attribute_004 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.name = "Named Attribute.004"
    named_attribute_004.label = ""
    named_attribute_004.location = (10560.0, -1400.0)
    named_attribute_004.bl_label = "Named Attribute"
    named_attribute_004.data_type = "BOOLEAN"
    # Name
    named_attribute_004.inputs[0].default_value = "blocker"
    # Links for named_attribute_004
    links.new(named_attribute_004.outputs[0], set_material_005.inputs[1])

    blocker = nodes.new("GeometryNodeGroup")
    blocker.name = "Group.001"
    blocker.label = ""
    blocker.location = (9060.0, -1560.0)
    blocker.node_tree = create_blocker_group()
    blocker.bl_label = "Group"
    # Decor
    blocker.inputs[0].default_value = True
    # Links for blocker
    links.new(blocker.outputs[0], join_geometry_004.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (-7403.833984375, 4101.759765625)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points

    waist = nodes.new("GeometryNodeGroup")
    waist.name = "Group.003"
    waist.label = ""
    waist.location = (9060.0, -1260.0)
    waist.node_tree = create_waist_group()
    waist.bl_label = "Group"
    # Decor
    waist.inputs[0].default_value = True
    # Links for waist
    links.new(waist.outputs[0], join_geometry_004.inputs[0])

    named_attribute_005 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_005.name = "Named Attribute.005"
    named_attribute_005.label = ""
    named_attribute_005.location = (9600.0, -1400.0)
    named_attribute_005.bl_label = "Named Attribute"
    named_attribute_005.data_type = "BOOLEAN"
    # Name
    named_attribute_005.inputs[0].default_value = "skip"
    # Links for named_attribute_005
    links.new(named_attribute_005.outputs[0], mirror.inputs[1])

    set_material_006 = nodes.new("GeometryNodeSetMaterial")
    set_material_006.name = "Set Material.006"
    set_material_006.label = ""
    set_material_006.location = (10720.0, -1300.0)
    set_material_006.bl_label = "Set Material"
    # Links for set_material_006
    links.new(set_material_005.outputs[0], set_material_006.inputs[0])
    links.new(set_material_006.outputs[0], group_output.inputs[0])

    named_attribute_006 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_006.name = "Named Attribute.006"
    named_attribute_006.label = ""
    named_attribute_006.location = (10720.0, -1400.0)
    named_attribute_006.bl_label = "Named Attribute"
    named_attribute_006.data_type = "BOOLEAN"
    # Name
    named_attribute_006.inputs[0].default_value = "rope"
    # Links for named_attribute_006
    links.new(named_attribute_006.outputs[0], set_material_006.inputs[1])

    auto_layout_nodes(group)
    return group