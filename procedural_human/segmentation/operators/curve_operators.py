"""
Curve insertion operators for the segmentation workflow.
"""

import bpy
import math
from bpy.types import Operator
from bpy.props import (
    BoolProperty, 
    FloatProperty, 
    EnumProperty,
    PointerProperty,
    StringProperty,
)
from mathutils import Vector, Matrix, Euler

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


@procedural_operator
class InsertCurveAsNewObjectOperator(Operator):
    """Create a new object from selected curves with LoftSpheriod modifier"""
    
    bl_idname = "segmentation.insert_curve_new_object"
    bl_label = "Create Lofted Object"
    bl_description = "Create a new mesh object from selected curves using LoftSpheriod geometry nodes"
    bl_options = {'REGISTER', 'UNDO'}
    
    curve_resolution: bpy.props.IntProperty(
        name="Curve Resolution",
        description="Resolution along the curve",
        default=200,
        min=10,
        max=1000
    )
    
    radial_resolution: bpy.props.IntProperty(
        name="Radial Resolution",
        description="Resolution around the curve",
        default=32,
        min=4,
        max=128
    )
    
    def execute(self, context):
        # Get selected curves
        selected_curves = [obj for obj in context.selected_objects if obj.type == 'CURVE']
        
        if not selected_curves:
            self.report({'WARNING'}, "No curves selected")
            return {'CANCELLED'}
        
        try:
            # Join curves if multiple selected
            if len(selected_curves) > 1:
                # Make first curve active
                context.view_layer.objects.active = selected_curves[0]
                bpy.ops.object.join()
                curve_obj = context.active_object
            else:
                curve_obj = selected_curves[0]
            
            # Convert curve to mesh first
            bpy.ops.object.select_all(action='DESELECT')
            curve_obj.select_set(True)
            context.view_layer.objects.active = curve_obj
            
            # Create a new mesh object
            mesh = bpy.data.meshes.new(name=f"{curve_obj.name}_Lofted")
            mesh_obj = bpy.data.objects.new(f"{curve_obj.name}_Lofted", mesh)
            context.collection.objects.link(mesh_obj)
            
            # Add geometry nodes modifier
            modifier = mesh_obj.modifiers.new(name="LoftSpheriod", type='NODES')
            
            # Get or create the LoftSpheriod node group
            try:
                from procedural_human.geo_node_groups.loft_spheroid import create_loft_spheriod_group
                node_group = create_loft_spheriod_group()
                modifier.node_group = node_group
                
                # Set the curve as input geometry
                # The LoftSpheriod expects curve geometry
                # We need to copy the curve data to the mesh object
                
                # For now, we'll parent the curve to the mesh
                curve_obj.parent = mesh_obj
                
                # Set modifier inputs if they exist
                if "CurveResolution" in modifier.node_group.interface.items_tree.keys():
                    modifier["Input_2"] = self.curve_resolution
                if "Radial Resolution" in modifier.node_group.interface.items_tree.keys():
                    modifier["Input_3"] = self.radial_resolution
                
                self.report({'INFO'}, f"Created lofted object: {mesh_obj.name}")
                
            except ImportError as e:
                logger.warning(f"LoftSpheriod group not available: {e}")
                self.report({'WARNING'}, "LoftSpheriod not available, created basic mesh")
            
            # Select the new object
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            context.view_layer.objects.active = mesh_obj
            
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to create lofted object: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "curve_resolution")
        layout.prop(self, "radial_resolution")


@procedural_operator  
class InsertCurveOnExistingObjectOperator(Operator):
    """Add curves to an existing object with rotation offset"""
    
    bl_idname = "segmentation.insert_curve_existing"
    bl_label = "Add Curves to Object"
    bl_description = "Add selected curves to an existing object with rotational offset"
    bl_options = {'REGISTER', 'UNDO'}
    
    target_object: StringProperty(
        name="Target Object",
        description="Name of the object to add curves to"
    )
    
    rotation_offset: FloatProperty(
        name="Rotation Offset",
        description="Rotation offset in degrees (XY plane, Z aligned)",
        default=90.0,
        min=0.0,
        max=360.0,
        subtype='ANGLE'
    )
    
    align_to_curve: BoolProperty(
        name="Align to Existing Curve",
        description="Align new curves to intersect with an existing curve",
        default=True
    )
    
    def execute(self, context):
        # Get selected curves
        selected_curves = [obj for obj in context.selected_objects if obj.type == 'CURVE']
        
        if not selected_curves:
            self.report({'WARNING'}, "No curves selected")
            return {'CANCELLED'}
        
        # Get target object
        target = bpy.data.objects.get(self.target_object)
        if target is None:
            self.report({'WARNING'}, f"Target object '{self.target_object}' not found")
            return {'CANCELLED'}
        
        try:
            for curve_obj in selected_curves:
                # Create a copy of the curve
                new_curve = curve_obj.copy()
                new_curve.data = curve_obj.data.copy()
                context.collection.objects.link(new_curve)
                
                # Apply rotation offset (around Z axis, in XY plane)
                rotation_radians = math.radians(self.rotation_offset)
                rotation_matrix = Matrix.Rotation(rotation_radians, 4, 'Z')
                
                # Apply rotation to curve location
                new_curve.location = rotation_matrix @ curve_obj.location
                
                # Rotate the curve itself
                new_curve.rotation_euler.z += rotation_radians
                
                # Parent to target object
                new_curve.parent = target
                
                # Rename
                new_curve.name = f"{target.name}_{curve_obj.name}_rotated"
            
            self.report({'INFO'}, f"Added {len(selected_curves)} curves to {target.name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to add curves: {e}")
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        # Try to get the active object as target if it's not a curve
        if context.active_object and context.active_object.type != 'CURVE':
            self.target_object = context.active_object.name
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop_search(self, "target_object", bpy.data, "objects")
        layout.prop(self, "rotation_offset")
        layout.prop(self, "align_to_curve")


@procedural_operator
class SelectCurvesFromSegmentationOperator(Operator):
    """Select all curves created from segmentation"""
    
    bl_idname = "segmentation.select_curves"
    bl_label = "Select Segmentation Curves"
    bl_description = "Select all curve objects created from segmentation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        
        count = 0
        for obj in bpy.data.objects:
            if obj.type == 'CURVE' and obj.name.startswith("Segment"):
                obj.select_set(True)
                count += 1
        
        if count > 0:
            context.view_layer.objects.active = [
                obj for obj in context.selected_objects
            ][0]
            self.report({'INFO'}, f"Selected {count} segmentation curves")
        else:
            self.report({'INFO'}, "No segmentation curves found")
        
        return {'FINISHED'}


