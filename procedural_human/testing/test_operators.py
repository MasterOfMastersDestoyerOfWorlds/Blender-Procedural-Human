"""
Test Operators for Coon/Charrot-Gregory Patch Geometry Nodes

Provides Blender operators that automate the testing workflow:
1. Setup a test scene with a cube and initialize bezier handles
2. Add the CoonNGonPatchGenerator geometry node
3. Apply the modifier and export CSV data
4. Run topology verification

Usage in Blender:
    bpy.ops.procedural.setup_coon_test()
    bpy.ops.procedural.apply_and_export()
    bpy.ops.procedural.verify_topology()
    bpy.ops.procedural.run_full_coon_test()
"""

import bpy
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty, StringProperty
from pathlib import Path

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.config import get_codebase_path

def get_tmp_dir() -> Path:
    """Get the tmp directory for test exports."""
    from procedural_human.utils.export_curve_to_csv import get_tmp_base_dir
    return get_tmp_base_dir()


def ensure_edit_mode(obj):
    """Ensure we're in edit mode for the given object."""
    bpy.context.view_layer.objects.active = obj
    if obj.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')


def ensure_object_mode(obj):
    """Ensure we're in object mode."""
    bpy.context.view_layer.objects.active = obj
    if obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


def find_geometry_node_modifier(obj, node_group_name: str):
    """Find a geometry node modifier using a specific node group."""
    for mod in obj.modifiers:
        if mod.type == 'NODES' and mod.node_group:
            if mod.node_group.name == node_group_name:
                return mod
    return None


def add_geometry_node_modifier(obj, node_group_name: str):
    """Add a geometry node modifier with the specified node group."""
    node_group = bpy.data.node_groups.get(node_group_name)
    
    if node_group is None:
        raise ValueError(f"Node group '{node_group_name}' not found. "
                        f"Make sure the addon is loaded and the geometry node is registered.")
    mod = obj.modifiers.new(name=node_group_name, type='NODES')
    mod.node_group = node_group
    
    return mod

@procedural_operator
class PROC_OT_setup_coon_test(Operator):
    """Setup a test scene for Coon/Charrot-Gregory patch testing"""
    
    bl_idname = "procedural.setup_coon_test"
    bl_label = "Setup Coon Patch Test"
    bl_options = {'REGISTER', 'UNDO'}
    
    subdivisions: IntProperty(
        name="Subdivisions",
        description="Number of subdivisions for the patch",
        default=2,
        min=1,
        max=5
    )
    
    use_existing_cube: BoolProperty(
        name="Use Existing Cube",
        description="Use the existing selected cube instead of creating a new one",
        default=True
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not self.use_existing_cube or obj is None or obj.type != 'MESH':
            bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
            obj = context.active_object
            obj.name = "CoonTestCube"
            self.report({'INFO'}, "Created new test cube")
        else:
            self.report({'INFO'}, f"Using existing object: {obj.name}")
        ensure_edit_mode(obj)
        try:
            bpy.ops.mesh.initialize_bezier_handles()
            self.report({'INFO'}, "Initialized bezier handles")
        except Exception as e:
            self.report({'WARNING'}, f"Could not initialize handles: {e}")
        ensure_object_mode(obj)
        node_group_name = "CoonNGonPatchGenerator"
        mod = find_geometry_node_modifier(obj, node_group_name)
        
        if mod is None:
            try:
                mod = add_geometry_node_modifier(obj, node_group_name)
                self.report({'INFO'}, f"Added {node_group_name} modifier")
            except ValueError as e:
                self.report({'ERROR'}, str(e))
                return {'CANCELLED'}
        else:
            self.report({'INFO'}, f"Using existing {node_group_name} modifier")
        if mod.node_group:
            for item in mod.node_group.interface.items_tree:
                if item.item_type == 'SOCKET' and item.in_out == 'INPUT':
                    if 'subdiv' in item.name.lower():
                        socket_id = item.identifier
                        mod[socket_id] = self.subdivisions
                        self.report({'INFO'}, f"Set subdivisions to {self.subdivisions}")
                        break
        context.view_layer.update()
        
        self.report({'INFO'}, "Coon patch test setup complete")
        return {'FINISHED'}


@procedural_operator
class PROC_OT_apply_and_export(Operator):
    """Apply geometry node modifier and export CSV data"""
    
    bl_idname = "procedural.apply_and_export"
    bl_label = "Apply and Export CSV"
    bl_options = {'REGISTER', 'UNDO'}
    
    apply_modifier: BoolProperty(
        name="Apply Modifier",
        description="Apply the geometry node modifier before export",
        default=True
    )
    
    export_points: BoolProperty(
        name="Export Points",
        description="Export point/vertex data to CSV",
        default=True
    )
    
    export_edges: BoolProperty(
        name="Export Edges", 
        description="Export edge data to CSV",
        default=True
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        ensure_object_mode(obj)
        if self.apply_modifier:
            mod = find_geometry_node_modifier(obj, "CoonNGonPatchGenerator")
            
            if mod:
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                    self.report({'INFO'}, "Applied CoonNGonPatchGenerator modifier")
                except Exception as e:
                    self.report({'WARNING'}, f"Could not apply modifier: {e}")
            else:
                self.report({'WARNING'}, "No CoonNGonPatchGenerator modifier found")
        from procedural_human.utils.export_curve_to_csv import (
            export_spreadsheet_data, 
            get_tmp_base_dir
        )
        
        output_dir = get_tmp_base_dir()
        exported_files = []
        
        if self.export_points:
            settings = {
                'domain': 'POINT',
                'component': 'MESH',
                'eval_state': 'EVALUATED',
            }
            try:
                csv_path, row_count, headers = export_spreadsheet_data(obj, settings, output_dir)
                self.report({'INFO'}, f"Exported {row_count} points to {csv_path.name}")
                exported_files.append("points")
            except Exception as e:
                self.report({'WARNING'}, f"Could not export points: {e}")
        
        if self.export_edges:
            settings = {
                'domain': 'EDGE',
                'component': 'MESH',
                'eval_state': 'EVALUATED',
            }
            try:
                csv_path, row_count, headers = export_spreadsheet_data(obj, settings, output_dir)
                self.report({'INFO'}, f"Exported {row_count} edges to {csv_path.name}")
                exported_files.append("edges")
            except Exception as e:
                self.report({'WARNING'}, f"Could not export edges: {e}")
        
        if exported_files:
            self.report({'INFO'}, f"Exported: {', '.join(exported_files)}")
        else:
            self.report({'WARNING'}, "No data exported")
        
        return {'FINISHED'}


@procedural_operator
class PROC_OT_verify_topology(Operator):
    """Verify topology of the generated mesh using CSV analysis"""
    
    bl_idname = "procedural.verify_topology"
    bl_label = "Verify Topology"
    bl_options = {'REGISTER'}
    
    point_csv: StringProperty(
        name="Point CSV",
        description="Path to point CSV file (leave empty for auto-detect)",
        default=""
    )
    
    edge_csv: StringProperty(
        name="Edge CSV",
        description="Path to edge CSV file (leave empty for auto-detect)",
        default=""
    )
    
    def execute(self, context):
        from procedural_human.testing.topology_checker import (
            check_all_corners,
            get_latest_csvs,
        )
        
        tmp_dir = get_tmp_dir()
        point_csv = self.point_csv
        edge_csv = self.edge_csv
        
        if not point_csv or not edge_csv:
            auto_point, auto_edge = get_latest_csvs(str(tmp_dir))
            if not point_csv:
                point_csv = auto_point
            if not edge_csv:
                edge_csv = auto_edge
        
        if not point_csv or not edge_csv:
            self.report({'ERROR'}, f"Could not find CSV files in {tmp_dir}")
            return {'CANCELLED'}
        try:
            results = check_all_corners(point_csv, edge_csv)
        except Exception as e:
            self.report({'ERROR'}, f"Topology check failed: {e}")
            return {'CANCELLED'}
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        
        if failed == 0:
            self.report({'INFO'}, f"PASS: All {passed} corners have correct topology")
        else:
            failed_corners = [r for r in results if not r.passed][:5]
            fail_msgs = [f"Point {r.corner_id}" for r in failed_corners]
            
            self.report({'WARNING'}, 
                f"FAIL: {failed}/{len(results)} corners have star patterns. "
                f"Failed: {', '.join(fail_msgs)}{'...' if failed > 5 else ''}")
        context.scene["coon_test_passed"] = passed
        context.scene["coon_test_failed"] = failed
        context.scene["coon_test_total"] = len(results)
        
        return {'FINISHED'}


@procedural_operator
class PROC_OT_run_full_coon_test(Operator):
    """Run the full Coon patch test cycle: setup, apply, export, verify"""
    
    bl_idname = "procedural.run_full_coon_test"
    bl_label = "Run Full Coon Test"
    bl_options = {'REGISTER', 'UNDO'}
    
    subdivisions: IntProperty(
        name="Subdivisions",
        description="Number of subdivisions for the patch",
        default=2,
        min=1,
        max=5
    )
    
    create_new_cube: BoolProperty(
        name="Create New Cube",
        description="Create a fresh cube for testing",
        default=True
    )
    
    subdivide_edge: BoolProperty(
        name="Subdivide Edge",
        description="Subdivide one edge to create pentagon faces",
        default=False
    )
    
    def execute(self, context):
        self.report({'INFO'}, "Setting up test...")
        result = bpy.ops.procedural.setup_coon_test(
            subdivisions=self.subdivisions,
            use_existing_cube=not self.create_new_cube
        )
        if result != {'FINISHED'}:
            return result
        if self.subdivide_edge:
            obj = context.active_object
            if obj and obj.type == 'MESH':
                ensure_edit_mode(obj)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(type='EDGE')
                bpy.ops.object.mode_set(mode='OBJECT')
                if len(obj.data.edges) > 0:
                    obj.data.edges[0].select = True
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.subdivide(number_cuts=1)
                ensure_object_mode(obj)
                bpy.ops.mesh.initialize_loft_handles()
                self.report({'INFO'}, "Subdivided edge to create pentagon faces")
        self.report({'INFO'}, "Applying modifier and exporting...")
        result = bpy.ops.procedural.apply_and_export(
            apply_modifier=True,
            export_points=True,
            export_edges=True
        )
        if result != {'FINISHED'}:
            return result
        self.report({'INFO'}, "Verifying topology...")
        result = bpy.ops.procedural.verify_topology()
        passed = context.scene.get("coon_test_passed", 0)
        failed = context.scene.get("coon_test_failed", 0)
        total = context.scene.get("coon_test_total", 0)
        
        if failed == 0:
            self.report({'INFO'}, f"TEST PASSED: All {total} corners correct")
        else:
            self.report({'ERROR'}, f"TEST FAILED: {failed}/{total} corners have star patterns")
        
        return {'FINISHED'}
