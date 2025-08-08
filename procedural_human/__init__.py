"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes
"""

from . import operators
from . import panels
from . import menus

bl_info = {
    "name": "Procedural Human Generator",
    "author": "Procedural Human Team",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh",
    "description": "Generates complete procedural humans using Geometry Nodes",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


# Registration
def register():
    operators.register()
    panels.register()
    menus.register()


def unregister():
    menus.unregister()
    panels.unregister()
    operators.unregister()


if __name__ == "__main__":
    register()
