"""
Neck geometry node group package.

Exports create_neck_group for use by armor_suit and other modules.
Each frame and its children are defined in separate modules under this package.
"""
from procedural_human.geo_node_groups.armor.neck.main import create_neck_group

__all__ = ["create_neck_group"]
