"""
Utility functions for Procedural Human Generator
"""

import bpy
from mathutils import Vector

def get_property_value(prop_name, default):
    """Get actual value from Blender property"""
    try:
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        pass 
    except Exception:
        return default


def get_property_value(obj, prop_name, default):
    """Get actual value from Blender property"""
    try:
        val = getattr(obj, prop_name, default)
        
        if hasattr(val, '_default'):
            return val._default
        elif hasattr(val, 'default'):
            return val.default
        elif str(type(val)) == "<class 'bpy.props._PropertyDeferred'>":
            return default
        else:
            
            if isinstance(default, (int, float)):
                return float(val)
            else:
                return str(val)
    except Exception:
        return default


def get_numeric_value(value, default):
    """Extract numeric value from Blender property or return as-is if already numeric"""
    try:
        if hasattr(value, "_default"):
            return value._default
        elif hasattr(value, "default"):
            return value.default
        elif str(type(value)) == "<class 'bpy.props._PropertyDeferred'>":
            return default
        else:
            return float(value)
    except Exception:
        return default


def setup_node_group_interface(node_group):
    """Helper function to setup node group interface with geometry sockets"""
    
    existing_sockets = [socket.name for socket in node_group.interface.items_tree]
    
    
    if "Geometry" not in existing_sockets:
        try:
            node_group.interface.new_socket(
                name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
            )
        except Exception as e:
            print(f"Warning: Could not create input Geometry socket: {e}")
    
    
    existing_sockets = [socket.name for socket in node_group.interface.items_tree]
    if "Geometry" not in existing_sockets or existing_sockets.count("Geometry") < 2:
        try:
            node_group.interface.new_socket(
                name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
            )
        except Exception as e:
            print(f"Warning: Could not create output Geometry socket: {e}")

def create_geometry_nodes_modifier(obj, name):
    """Add Geometry Nodes modifier to object"""
    modifier = obj.modifiers.new(name, "NODES")
    node_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    modifier.node_group = node_group
    return modifier, node_group


def setup_basic_nodes(node_group):
    """Setup basic input/output nodes"""
    
    if "Geometry" not in [socket.name for socket in node_group.interface.items_tree]:
        node_group.interface.new_socket(
            name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        node_group.interface.new_socket(
            name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

    
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    
    input_node.location = (-600, 0)
    output_node.location = (600, 0)

    return input_node, output_node

