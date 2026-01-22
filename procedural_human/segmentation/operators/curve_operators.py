"""
Curve insertion operators for the segmentation workflow.
"""

import bpy
import math
from bpy.types import Operator
from bpy.props import (
    BoolProperty, 
    FloatProperty, 
    IntProperty,
    EnumProperty,
    PointerProperty,
    StringProperty,
)
from mathutils import Vector, Matrix, Euler
import numpy as np

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
        selected_curves = [obj for obj in context.selected_objects if obj.type == 'CURVE']
        
        if not selected_curves:
            self.report({'WARNING'}, "No curves selected")
            return {'CANCELLED'}
        
        try:
            if len(selected_curves) > 1:
                context.view_layer.objects.active = selected_curves[0]
                bpy.ops.object.join()
                curve_obj = context.active_object
            else:
                curve_obj = selected_curves[0]
            bpy.ops.object.select_all(action='DESELECT')
            curve_obj.select_set(True)
            context.view_layer.objects.active = curve_obj
            mesh = bpy.data.meshes.new(name=f"{curve_obj.name}_Lofted")
            mesh_obj = bpy.data.objects.new(f"{curve_obj.name}_Lofted", mesh)
            context.collection.objects.link(mesh_obj)
            modifier = mesh_obj.modifiers.new(name="LoftSpheriod", type='NODES')
            try:
                from procedural_human.geo_node_groups.loft_spheroid import create_loft_spheriod_group
                node_group = create_loft_spheriod_group()
                modifier.node_group = node_group
                curve_obj.parent = mesh_obj
                if "CurveResolution" in modifier.node_group.interface.items_tree.keys():
                    modifier["Input_2"] = self.curve_resolution
                if "Radial Resolution" in modifier.node_group.interface.items_tree.keys():
                    modifier["Input_3"] = self.radial_resolution
                
                self.report({'INFO'}, f"Created lofted object: {mesh_obj.name}")
                
            except ImportError as e:
                logger.warning(f"LoftSpheriod group not available: {e}")
                self.report({'WARNING'}, "LoftSpheriod not available, created basic mesh")
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
        selected_curves = [obj for obj in context.selected_objects if obj.type == 'CURVE']
        
        if not selected_curves:
            self.report({'WARNING'}, "No curves selected")
            return {'CANCELLED'}
        target = bpy.data.objects.get(self.target_object)
        if target is None:
            self.report({'WARNING'}, f"Target object '{self.target_object}' not found")
            return {'CANCELLED'}
        
        try:
            for curve_obj in selected_curves:
                new_curve = curve_obj.copy()
                new_curve.data = curve_obj.data.copy()
                context.collection.objects.link(new_curve)
                rotation_radians = math.radians(self.rotation_offset)
                rotation_matrix = Matrix.Rotation(rotation_radians, 4, 'Z')
                new_curve.location = rotation_matrix @ curve_obj.location
                new_curve.rotation_euler.z += rotation_radians
                new_curve.parent = target
                new_curve.name = f"{target.name}_{curve_obj.name}_rotated"
            
            self.report({'INFO'}, f"Added {len(selected_curves)} curves to {target.name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to add curves: {e}")
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
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


@procedural_operator
class SimpleRotateMeshCurveOperator(Operator):
    """
    Create a mesh by rotating the segmentation mask 90 degrees.
    Uses depth estimation to scale the rotated view (thickness).
    """
    
    bl_idname = "segmentation.simple_rotate_mesh"
    bl_label = "Simple Rotate Mesh"
    bl_description = "Create a mesh by rotating the mask 90 degrees, scaled by estimated depth"
    bl_options = {'REGISTER', 'UNDO'}
    
    simplify: BoolProperty(
        name="Simplify",
        description="Simplify curve contours",
        default=True
    )
    
    simplify_amount: FloatProperty(
        name="Simplify Amount",
        description="Higher values = more simplified (0.001 - 0.05)",
        default=0.005,
        min=0.001,
        max=0.05
    )
    
    points_per_half: IntProperty(
        name="Points per Half",
        description="Number of vertices per half-loop (excluding shared vertices)",
        default=16,
        min=4,
        max=64
    )
    
    use_depth_estimation: BoolProperty(
        name="Use Depth Estimation",
        description="Estimate object thickness from image to scale the side view",
        default=False
    )
    
    thickness_scale: FloatProperty(
        name="Thickness Scale",
        description="Manual scaling factor for the side view thickness",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    def execute(self, context):
        from procedural_human.segmentation.operators.segmentation_operators import (
            get_current_masks,
            get_active_image,
            blender_image_to_pil,
            get_enabled_mask_indices,
            get_original_image_pixels,
        )
        from procedural_human.segmentation.operators.novel_view_operators import set_contours
        from procedural_human.segmentation.mask_to_curve import find_contours, simplify_contour
        masks = get_current_masks()
        enabled_indices = get_enabled_mask_indices(context)
        image = get_active_image(context)
        
        if not masks or not enabled_indices or not image:
            self.report({'WARNING'}, "No masks or image available")
            return {'CANCELLED'}
        mask_idx = enabled_indices[0]
        mask = masks[mask_idx]
        original_pixels = get_original_image_pixels()
        if original_pixels is not None:
            from PIL import Image as PILImage
            width, height = image.size
            pixels = np.array(original_pixels).reshape((height, width, 4))
            pixels = np.flipud(pixels)
            pixels = (pixels[:, :, :3] * 255).astype(np.uint8)
            pil_image = PILImage.fromarray(pixels, mode='RGB')
        else:
            pil_image = blender_image_to_pil(image)
        mask_bottom_left = np.flipud(mask)
        front_contours = find_contours(mask_bottom_left.astype(np.uint8))
        
        if not front_contours:
            self.report({'ERROR'}, "Could not extract contour from mask")
            return {'CANCELLED'}
        front_contour = max(front_contours, key=len)
        if self.simplify:
            front_contour = simplify_contour(front_contour, epsilon=self.simplify_amount)
        scaling_factor = self.thickness_scale
        
        if self.use_depth_estimation:
            try:
                from procedural_human.depth_estimation.depth_estimator import DepthEstimator
                estimator = DepthEstimator.get_instance()
                if not estimator.is_loaded() and not estimator.is_loading():
                    self.report({'INFO'}, "Loading depth model...")
                ratio = estimator.get_thickness_ratio(pil_image, mask)
                scaling_factor *= ratio
                logger.info(f"Depth estimation ratio: {ratio:.3f}, Final scale: {scaling_factor:.3f}")
                
            except Exception as e:
                logger.warning(f"Depth estimation failed: {e}")
                self.report({'WARNING'}, f"Depth estimation failed, using manual scale. {e}")
        side_contour = front_contour.copy()
        x_center = side_contour[:, 0].mean()
        side_contour[:, 0] = (side_contour[:, 0] - x_center) * scaling_factor + x_center
        set_contours(front_contour, side_contour, None)
        bpy.ops.segmentation.create_dual_mesh_curves(
            'EXEC_DEFAULT', 
            use_convex_hull=False,  # Don't hull the side view, use the actual rotated profile
            points_per_half=self.points_per_half,
            merge_by_distance=True
        )
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "simplify")
        if self.simplify:
            layout.prop(self, "simplify_amount")
        layout.prop(self, "points_per_half")
        layout.separator()
        layout.prop(self, "use_depth_estimation")
        layout.prop(self, "thickness_scale")


