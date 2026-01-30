"""
Basalt Columns Test Module

Provides operators and utilities for testing the BasaltColumns geometry node group
with visual validation against reference images.

Usage in Blender:
    bpy.ops.procedural.test_basalt_columns()
    bpy.ops.procedural.setup_basalt_scene()
"""

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty, StringProperty
from procedural_human.decorators.operator_decorator import procedural_operator
from datetime import datetime
import os


@procedural_operator
class PROC_OT_setup_basalt_scene(Operator):
    """Setup a test scene with basalt columns, camera, and lighting"""
    
    bl_idname = "procedural.setup_basalt_scene"
    bl_label = "Setup Basalt Test Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    size_x: FloatProperty(
        name="Size X",
        description="Width of the basalt field",
        default=10.0,
        min=1.0,
        max=100.0
    )
    
    size_y: FloatProperty(
        name="Size Y",
        description="Depth of the basalt field",
        default=10.0,
        min=1.0,
        max=100.0
    )
    
    resolution: IntProperty(
        name="Resolution",
        description="Grid resolution (more = smaller columns)",
        default=20,
        min=5,
        max=100
    )
    
    min_height: FloatProperty(
        name="Min Height",
        description="Minimum column height",
        default=0.5,
        min=0.0
    )
    
    max_height: FloatProperty(
        name="Max Height",
        description="Maximum column height",
        default=3.0,
        min=0.1
    )
    
    clear_scene: BoolProperty(
        name="Clear Scene",
        description="Remove existing objects before creating",
        default=False
    )
    
    def execute(self, context):
        # Optionally clear scene
        if self.clear_scene:
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
        
        # Create base plane for basalt
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
        obj = context.active_object
        obj.name = "BasaltColumns"
        
        # Add geometry nodes modifier
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        
        # Get or create the basalt columns node group
        from procedural_human.geo_node_groups.terrain.basalt_columns import create_basalt_columns_group
        node_group = create_basalt_columns_group()
        mod.node_group = node_group
        
        # Set parameters via modifier inputs
        # The input names in the modifier use the socket identifiers
        for item in mod.node_group.interface.items_tree:
            if item.item_type == 'SOCKET' and item.in_out == 'INPUT':
                socket_id = item.identifier
                if "Size X" in item.name and socket_id in mod:
                    mod[socket_id] = self.size_x
                elif "Size Y" in item.name and socket_id in mod:
                    mod[socket_id] = self.size_y
                elif "Resolution" in item.name and socket_id in mod:
                    mod[socket_id] = self.resolution
                elif "Min Height" in item.name and socket_id in mod:
                    mod[socket_id] = self.min_height
                elif "Max Height" in item.name and socket_id in mod:
                    mod[socket_id] = self.max_height
        
        # Setup camera
        cam_data = bpy.data.cameras.new("BasaltCamera")
        cam_data.lens = 35
        cam = bpy.data.objects.new("BasaltCamera", cam_data)
        context.collection.objects.link(cam)
        
        # Position camera for isometric-like view
        cam.location = (self.size_x * 1.5, -self.size_y * 1.5, self.max_height * 3)
        cam.rotation_euler = (1.1, 0, 0.8)
        context.scene.camera = cam
        
        # Setup sun light
        light_data = bpy.data.lights.new("BasaltSun", type='SUN')
        light_data.energy = 3
        light_data.color = (1.0, 0.95, 0.9)  # Slightly warm
        light = bpy.data.objects.new("BasaltSun", light_data)
        context.collection.objects.link(light)
        light.rotation_euler = (0.8, 0.2, 0.5)
        
        # Setup world background
        if context.scene.world is None:
            context.scene.world = bpy.data.worlds.new("BasaltWorld")
        context.scene.world.use_nodes = True
        bg_node = context.scene.world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs["Color"].default_value = (0.6, 0.7, 0.8, 1.0)  # Sky blue
        
        self.report({'INFO'}, f"Created basalt test scene with {self.resolution}x{self.resolution} grid")
        return {'FINISHED'}


@procedural_operator
class PROC_OT_test_basalt_columns(Operator):
    """Test basalt columns generation and render for validation"""
    
    bl_idname = "procedural.test_basalt_columns"
    bl_label = "Test Basalt Columns"
    bl_options = {'REGISTER'}
    
    resolution: IntProperty(
        name="Resolution",
        default=20,
        min=5,
        max=50
    )
    
    render_resolution_x: IntProperty(
        name="Render Width",
        default=800,
        min=100,
        max=4096
    )
    
    render_resolution_y: IntProperty(
        name="Render Height",
        default=600,
        min=100,
        max=4096
    )
    
    def execute(self, context):
        from procedural_human.config import get_codebase_path
        
        # Setup scene
        bpy.ops.procedural.setup_basalt_scene(
            resolution=self.resolution,
            clear_scene=True
        )
        
        # Get mesh metrics
        obj = context.active_object
        if obj and obj.type == 'MESH':
            # Apply modifier to get real mesh data
            depsgraph = context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(depsgraph)
            mesh = obj_eval.to_mesh()
            
            # Count face sides
            face_sides = {}
            for poly in mesh.polygons:
                sides = len(poly.vertices)
                face_sides[sides] = face_sides.get(sides, 0) + 1
            
            obj_eval.to_mesh_clear()
            
            # Store metrics in scene for later retrieval
            context.scene["basalt_test_vertex_count"] = len(mesh.vertices)
            context.scene["basalt_test_face_count"] = len(mesh.polygons)
            context.scene["basalt_test_hexagon_count"] = face_sides.get(6, 0)
            context.scene["basalt_test_face_sides"] = str(face_sides)
            
            hexagon_ratio = face_sides.get(6, 0) / max(len(mesh.polygons), 1)
            self.report({'INFO'}, f"Hexagon ratio: {hexagon_ratio:.1%}")
        
        # Render
        codebase = get_codebase_path()
        tmp_dir = str(codebase / "tmp") if codebase else ""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        render_path = os.path.join(tmp_dir, f"basalt_test_{timestamp}.png")
        
        context.scene.render.resolution_x = self.render_resolution_x
        context.scene.render.resolution_y = self.render_resolution_y
        context.scene.render.filepath = render_path
        context.scene.render.image_settings.file_format = 'PNG'
        
        bpy.ops.render.render(write_still=True)
        
        context.scene["basalt_test_render_path"] = render_path
        
        self.report({'INFO'}, f"Rendered to: {render_path}")
        return {'FINISHED'}


@procedural_operator
class PROC_OT_validate_basalt_metrics(Operator):
    """Validate basalt column geometry metrics"""
    
    bl_idname = "procedural.validate_basalt_metrics"
    bl_label = "Validate Basalt Metrics"
    bl_options = {'REGISTER'}
    
    min_hexagon_ratio: FloatProperty(
        name="Min Hexagon Ratio",
        description="Minimum acceptable ratio of hexagonal faces",
        default=0.7,
        min=0.0,
        max=1.0
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        # Get evaluated mesh
        depsgraph = context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh = obj_eval.to_mesh()
        
        # Count face sides
        face_sides = {}
        for poly in mesh.polygons:
            sides = len(poly.vertices)
            face_sides[sides] = face_sides.get(sides, 0) + 1
        
        total_faces = len(mesh.polygons)
        hexagon_count = face_sides.get(6, 0)
        hexagon_ratio = hexagon_count / max(total_faces, 1)
        
        obj_eval.to_mesh_clear()
        
        # Check all faces have positive area
        valid_faces = True
        for poly in mesh.polygons:
            if poly.area <= 0:
                valid_faces = False
                break
        
        # Validation results
        passed = True
        messages = []
        
        if hexagon_ratio < self.min_hexagon_ratio:
            passed = False
            messages.append(f"FAIL: Hexagon ratio {hexagon_ratio:.1%} < {self.min_hexagon_ratio:.1%}")
        else:
            messages.append(f"PASS: Hexagon ratio {hexagon_ratio:.1%}")
        
        if not valid_faces:
            passed = False
            messages.append("FAIL: Some faces have zero area")
        else:
            messages.append("PASS: All faces have positive area")
        
        # Report
        for msg in messages:
            self.report({'INFO' if 'PASS' in msg else 'WARNING'}, msg)
        
        context.scene["basalt_validation_passed"] = passed
        context.scene["basalt_validation_hexagon_ratio"] = hexagon_ratio
        
        return {'FINISHED'} if passed else {'CANCELLED'}
