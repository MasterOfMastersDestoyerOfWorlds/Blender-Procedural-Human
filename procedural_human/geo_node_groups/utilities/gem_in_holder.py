import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes

@geo_node_group
def create_gem_in__holder_group():
    group_name = "Gem in Holder"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Gem Radius", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.009999999776482582
    socket.min_value = 0.0
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Gem Material", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "ruby"
    socket = group.interface.new_socket(name="Gem Dual Mesh", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Profile Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Profile Scale", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.004999999888241291
    socket.min_value = 0.0
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 20
    socket.min_value = 0
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 10
    socket.min_value = -10000
    socket.max_value = 10000
    socket = group.interface.new_socket(name="Wings", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Wing", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Wing Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Array Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 6
    socket.min_value = 3
    socket.max_value = 512
    socket = group.interface.new_socket(name="Strand Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 10
    socket.min_value = 0
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Split", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0020000000949949026
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 2.5099997520446777
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2440.0, -400.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (29.0, -135.79998779296875)
    group_input.bl_label = "Group Input"
    # Links for group_input

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    ico_sphere_001.label = ""
    ico_sphere_001.location = (189.0, -35.79998779296875)
    ico_sphere_001.bl_label = "Ico Sphere"
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 2
    # Links for ico_sphere_001

    dual_mesh = nodes.new("GeometryNodeDualMesh")
    dual_mesh.name = "Dual Mesh"
    dual_mesh.label = ""
    dual_mesh.location = (349.0, -35.79998779296875)
    dual_mesh.bl_label = "Dual Mesh"
    # Keep Boundaries
    dual_mesh.inputs[1].default_value = False
    # Links for dual_mesh
    links.new(ico_sphere_001.outputs[0], dual_mesh.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (1289.0, -35.79998779296875)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 24
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for curve_circle
    links.new(group_input.outputs[0], curve_circle.inputs[4])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1449.0, -35.79998779296875)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(curve_circle.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(group_input.outputs[3], curve_to_mesh_002.inputs[2])

    points = nodes.new("GeometryNodePoints")
    points.name = "Points"
    points.label = ""
    points.location = (429.0, -195.79998779296875)
    points.bl_label = "Points"
    # Radius
    points.inputs[2].default_value = 0.10000000149011612
    # Links for points
    links.new(group_input.outputs[4], points.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (269.0, -195.79998779296875)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT_VECTOR"
    # Min
    random_value.inputs[0].default_value = [-0.5, -1.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [0.5, 1.0, 0.0]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Links for random_value
    links.new(random_value.outputs[0], points.inputs[1])
    links.new(group_input.outputs[5], random_value.inputs[8])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (589.0, -195.79998779296875)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Links for points_to_curves
    links.new(points.outputs[0], points_to_curves.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.label = ""
    gradient_texture.location = (429.0, -335.79998779296875)
    gradient_texture.bl_label = "Gradient Texture"
    gradient_texture.gradient_type = "RADIAL"
    # Vector
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Links for gradient_texture
    links.new(gradient_texture.outputs[1], points_to_curves.inputs[2])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (749.0, -195.79998779296875)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = True
    # Links for set_spline_cyclic
    links.new(points_to_curves.outputs[0], set_spline_cyclic.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (909.0, -195.79998779296875)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "NURBS"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_spline_cyclic.outputs[0], set_spline_type.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (689.0, -35.79998779296875)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 0.6000000238418579))
    # Links for transform_geometry_005

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    points_to_vertices.label = ""
    points_to_vertices.location = (649.0, -215.13333129882812)
    points_to_vertices.bl_label = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True
    # Links for points_to_vertices

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.label = ""
    extrude_mesh_001.location = (1769.0, -55.133331298828125)
    extrude_mesh_001.bl_label = "Extrude Mesh"
    extrude_mesh_001.mode = "VERTICES"
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0020000000949949026
    # Individual
    extrude_mesh_001.inputs[4].default_value = True
    # Links for extrude_mesh_001

    repeat_input_001 = nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.name = "Repeat Input.001"
    repeat_input_001.label = ""
    repeat_input_001.location = (1589.0, -55.133331298828125)
    repeat_input_001.bl_label = "Repeat Input"
    # Iterations
    repeat_input_001.inputs[0].default_value = 60
    # Top
    repeat_input_001.inputs[2].default_value = True
    # Value
    repeat_input_001.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Links for repeat_input_001
    links.new(repeat_input_001.outputs[2], extrude_mesh_001.inputs[1])
    links.new(repeat_input_001.outputs[1], extrude_mesh_001.inputs[0])
    links.new(points_to_vertices.outputs[0], repeat_input_001.inputs[1])

    repeat_output_001 = nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.name = "Repeat Output.001"
    repeat_output_001.label = ""
    repeat_output_001.location = (2289.0, -55.133331298828125)
    repeat_output_001.bl_label = "Repeat Output"
    repeat_output_001.active_index = 2
    repeat_output_001.inspection_index = 0
    # Links for repeat_output_001
    links.new(extrude_mesh_001.outputs[1], repeat_output_001.inputs[1])
    links.new(extrude_mesh_001.outputs[0], repeat_output_001.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (589.0, -495.1333312988281)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    # Vector
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Scale
    noise_texture.inputs[2].default_value = 30.0
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture

    mesh_to_curve_003 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.name = "Mesh to Curve.003"
    mesh_to_curve_003.label = ""
    mesh_to_curve_003.location = (2449.0, -55.133331298828125)
    mesh_to_curve_003.bl_label = "Mesh to Curve"
    mesh_to_curve_003.mode = "EDGES"
    # Selection
    mesh_to_curve_003.inputs[1].default_value = True
    # Links for mesh_to_curve_003
    links.new(repeat_output_001.outputs[0], mesh_to_curve_003.inputs[0])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    curve_to_mesh_003.label = ""
    curve_to_mesh_003.location = (469.0, -35.80000305175781)
    curve_to_mesh_003.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = False
    # Links for curve_to_mesh_003

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.label = ""
    spline_parameter_003.location = (49.0, -515.7999877929688)
    spline_parameter_003.bl_label = "Spline Parameter"
    # Links for spline_parameter_003

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (29.0, -175.8000030517578)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(spline_parameter_003.outputs[0], float_curve.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (289.0, -175.8000030517578)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.004999999888241291
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(float_curve.outputs[0], math.inputs[0])
    links.new(math.outputs[0], curve_to_mesh_003.inputs[2])
    links.new(math.outputs[0], group_output.inputs[2])

    points_001 = nodes.new("GeometryNodePoints")
    points_001.name = "Points.001"
    points_001.label = ""
    points_001.location = (229.0, -315.1333312988281)
    points_001.bl_label = "Points"
    # Position
    points_001.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points_001.inputs[2].default_value = 0.10000000149011612
    # Links for points_001

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (229.0, -495.1333312988281)
    index.bl_label = "Index"
    # Links for index

    capture_attribute_007 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_007.name = "Capture Attribute.007"
    capture_attribute_007.label = ""
    capture_attribute_007.location = (409.0, -315.1333312988281)
    capture_attribute_007.bl_label = "Capture Attribute"
    capture_attribute_007.active_index = 0
    capture_attribute_007.domain = "POINT"
    # Links for capture_attribute_007
    links.new(capture_attribute_007.outputs[0], points_to_vertices.inputs[0])
    links.new(points_001.outputs[0], capture_attribute_007.inputs[0])
    links.new(index.outputs[0], capture_attribute_007.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (429.0, -495.1333312988281)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY_ADD"
    math_001.use_clamp = False
    # Links for math_001
    links.new(capture_attribute_007.outputs[1], math_001.inputs[0])
    links.new(math_001.outputs[0], noise_texture.inputs[1])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (28.83331298828125, -79.56706237792969)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_006
    links.new(curve_to_mesh_003.outputs[0], transform_geometry_006.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (188.83331298828125, -79.56706237792969)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(transform_geometry_006.outputs[0], flip_faces_001.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (188.83331298828125, -39.56705856323242)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(flip_faces_001.outputs[0], join_geometry_003.inputs[0])
    links.new(curve_to_mesh_003.outputs[0], join_geometry_003.inputs[0])

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    instance_on_points_003.label = ""
    instance_on_points_003.location = (329.0, -155.8000030517578)
    instance_on_points_003.bl_label = "Instance on Points"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Scale
    instance_on_points_003.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_003
    links.new(join_geometry_003.outputs[0], instance_on_points_003.inputs[2])

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (189.0, -35.79999923706055)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 9.999999747378752e-05
    # Links for curve_circle_001
    links.new(curve_circle_001.outputs[0], instance_on_points_003.inputs[0])

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.label = ""
    align_rotation_to_vector_002.location = (189.0, -435.79998779296875)
    align_rotation_to_vector_002.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_002
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points_003.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (189.0, -595.7999877929688)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_002.inputs[2])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (2860.0, 280.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    realize_instances_003.label = ""
    realize_instances_003.location = (509.0, -155.8000030517578)
    realize_instances_003.bl_label = "Realize Instances"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0
    # Links for realize_instances_003
    links.new(instance_on_points_003.outputs[0], realize_instances_003.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (509.0, -35.79998779296875)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], transform_geometry_005.inputs[0])
    links.new(dual_mesh.outputs[0], switch.inputs[2])
    links.new(ico_sphere_001.outputs[0], switch.inputs[1])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (29.0, -35.79998779296875)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], ico_sphere_001.inputs[0])
    links.new(group_input_001.outputs[2], switch.inputs[0])

    group_input_002 = nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.label = ""
    group_input_002.location = (29.0, -515.13330078125)
    group_input_002.bl_label = "Group Input"
    # Links for group_input_002
    links.new(group_input_002.outputs[8], points_001.inputs[0])
    links.new(group_input_002.outputs[9], math_001.inputs[1])
    links.new(group_input_002.outputs[10], math_001.inputs[2])

    group_input_003 = nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.label = ""
    group_input_003.location = (29.0, -95.80000305175781)
    group_input_003.bl_label = "Group Input"
    # Links for group_input_003
    links.new(group_input_003.outputs[7], curve_circle_001.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Profile"
    frame.location = (-2249.0, 615.7999877929688)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Gem"
    frame_001.location = (1151.0, 1015.7999877929688)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Strands"
    frame_002.location = (-2709.0, -124.86666870117188)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Mesh"
    frame_003.location = (211.0, -24.19999885559082)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Mirror"
    frame_004.location = (875.6666870117188, -48.33333206176758)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Radial Array"
    frame_005.location = (1271.0, -44.20000076293945)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (2020.0, 460.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (2380.0, 500.0)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(store_named_attribute.outputs[0], join_geometry_005.inputs[0])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (869.0, -35.79998779296875)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(transform_geometry_005.outputs[0], store_named_attribute_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], join_geometry_005.inputs[0])
    links.new(group_input_001.outputs[1], store_named_attribute_001.inputs[2])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (1549.0, -635.13330078125)
    mix.bl_label = "Mix"
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.0
    # B
    mix.inputs[3].default_value = 0.0
    # A
    mix.inputs[4].default_value = [1.0, 1.0, 0.0]
    # B
    mix.inputs[5].default_value = [1.0, 1.0, 1.0]
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (1589.0, -295.1333312988281)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], extrude_mesh_001.inputs[2])
    links.new(mix.outputs[1], vector_math.inputs[1])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (1189.0, -635.13330078125)
    position.bl_label = "Position"
    # Links for position

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (1189.0, -695.13330078125)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "LENGTH"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position.outputs[0], vector_math_001.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (1389.0, -635.13330078125)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Max
    map_range.inputs[2].default_value = 0.05000000074505806
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(vector_math_001.outputs[1], map_range.inputs[0])
    links.new(map_range.outputs[0], mix.inputs[0])

    group_input_004 = nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.label = ""
    group_input_004.location = (1189.0, -815.13330078125)
    group_input_004.bl_label = "Group Input"
    # Links for group_input_004
    links.new(group_input_004.outputs[0], map_range.inputs[1])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (2020.0, 160.0)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_002.inputs[3].default_value = True
    # Links for store_named_attribute_002
    links.new(realize_instances_003.outputs[0], store_named_attribute_002.inputs[0])
    links.new(store_named_attribute_002.outputs[0], join_geometry_004.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (2620.0, 360.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry
    links.new(join_geometry_005.outputs[0], transform_geometry.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_004.inputs[0])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (789.0, -495.1333312988281)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(noise_texture.outputs[1], separate_x_y_z.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (1129.0, -435.1333312988281)
    combine_x_y_z.bl_label = "Combine XYZ"
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], vector_math.inputs[0])
    links.new(separate_x_y_z.outputs[0], combine_x_y_z.inputs[0])
    links.new(separate_x_y_z.outputs[1], combine_x_y_z.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (949.0, -555.13330078125)
    math_002.bl_label = "Math"
    math_002.operation = "ABSOLUTE"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.5
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(separate_x_y_z.outputs[2], math_002.inputs[0])
    links.new(math_002.outputs[0], combine_x_y_z.inputs[2])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (1069.0, -195.79998779296875)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 12
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(resample_curve.outputs[0], curve_to_mesh_002.inputs[1])
    links.new(set_spline_type.outputs[0], resample_curve.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (2609.0, -55.133331298828125)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Length"
    # Count
    resample_curve_001.inputs[3].default_value = 10
    # Length
    resample_curve_001.inputs[4].default_value = 0.0007999999797903001
    # Links for resample_curve_001
    links.new(resample_curve_001.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(mesh_to_curve_003.outputs[0], resample_curve_001.inputs[0])
    links.new(resample_curve_001.outputs[0], group_output.inputs[4])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (3060.0, 460.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(switch_001.outputs[0], group_output.inputs[0])
    links.new(join_geometry_004.outputs[0], switch_001.inputs[2])
    links.new(join_geometry_005.outputs[0], switch_001.inputs[1])

    group_input_005 = nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.label = ""
    group_input_005.location = (3060.0, 520.0)
    group_input_005.bl_label = "Group Input"
    # Links for group_input_005
    links.new(group_input_005.outputs[6], switch_001.inputs[0])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (1769.0, -275.1333312988281)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "VECTOR"
    # True
    switch_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for switch_002
    links.new(repeat_input_001.outputs[0], switch_002.inputs[0])
    links.new(vector_math.outputs[0], switch_002.inputs[1])

    evaluate_at_index = nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index.name = "Evaluate at Index"
    evaluate_at_index.label = ""
    evaluate_at_index.location = (1929.0, -275.1333312988281)
    evaluate_at_index.bl_label = "Evaluate at Index"
    evaluate_at_index.domain = "POINT"
    evaluate_at_index.data_type = "FLOAT_VECTOR"
    # Index
    evaluate_at_index.inputs[1].default_value = 0
    # Links for evaluate_at_index
    links.new(switch_002.outputs[0], evaluate_at_index.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (2089.0, -275.1333312988281)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "ADD"
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], repeat_output_001.inputs[2])
    links.new(evaluate_at_index.outputs[0], vector_math_002.inputs[0])
    links.new(repeat_input_001.outputs[3], vector_math_002.inputs[1])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (389.0, -35.79998779296875)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(curve_to_mesh_003.outputs[0], transform_geometry_001.inputs[0])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (2469.0, -255.13333129882812)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT_VECTOR"
    attribute_statistic.domain = "POINT"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(repeat_output_001.outputs[0], attribute_statistic.inputs[0])
    links.new(repeat_output_001.outputs[2], attribute_statistic.inputs[2])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (29.0, -155.79998779296875)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector
    links.new(attribute_statistic.outputs[3], align_rotation_to_vector.inputs[2])

    invert_rotation = nodes.new("FunctionNodeInvertRotation")
    invert_rotation.name = "Invert Rotation"
    invert_rotation.label = ""
    invert_rotation.location = (229.0, -155.79998779296875)
    invert_rotation.bl_label = "Invert Rotation"
    # Links for invert_rotation
    links.new(invert_rotation.outputs[0], transform_geometry_001.inputs[3])
    links.new(align_rotation_to_vector.outputs[0], invert_rotation.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "Align to X"
    frame_006.location = (1311.0, -884.2000122070312)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (549.0, -35.79998779296875)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003
    links.new(store_named_attribute_003.outputs[0], group_output.inputs[3])
    links.new(transform_geometry_001.outputs[0], store_named_attribute_003.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (315.669921875, -66.96894073486328)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(resample_curve.outputs[0], reroute.inputs[0])
    links.new(reroute.outputs[0], group_output.inputs[1])

    auto_layout_nodes(group)
    return group
