# Procedural Human Generator for Blender

A comprehensive Blender add-on for creating procedural human characters using Geometry Nodes. This plugin implements the concepts outlined in the detailed plan, providing a modular approach to human character generation.

## Features

### Core Components
- **Torso Generation**: Creates anatomically proportioned torsos with customizable build and height
- **Limb System**: Generates arms and legs with muscle definition and joint articulation
- **Head Creation**: Produces stylized heads with facial feature displacement
- **Hand System**: Modular finger generation using instancing techniques
- **Spine Scaffold**: Natural S-curve spine for posture control

### Advanced Features
- **Geometry Nodes Integration**: All components use advanced Geometry Nodes setups
- **Parametric Control**: Real-time adjustment of body proportions
- **Modular Design**: Create individual components or complete humans
- **Non-Destructive Workflow**: All changes are procedural and reversible

## Installation

### Method 1: Using the Zip File (Recommended)
1. Download the `procedural_human.zip` file
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Click "Install..." and select the zip file
5. Enable the add-on by checking the box next to "Procedural Human Generator"

### Method 2: Manual Installation
1. Create a folder named `procedural_human` in your Blender addons directory
2. Copy all the plugin files into this folder
3. Open Blender
4. Go to Edit > Preferences > Add-ons
5. Enable the add-on by checking the box next to "Procedural Human Generator"

## Usage

### Creating a Complete Human

1. In the 3D Viewport, press `Shift + A`
2. Navigate to `Mesh > Procedural Human`
3. A complete human character will be generated with all components

### Creating Individual Components

1. In the 3D Viewport, press `Shift + A`
2. Navigate to `Mesh > Procedural Torso` or `Procedural Head`
3. Individual components will be created

### Adjusting Parameters

1. Select the generated object
2. In the Properties panel, find the "Procedural" tab
3. Adjust parameters like:
   - Height
   - Build (body type)
   - Head Scale
   - Arm Length
   - Leg Length

## Technical Architecture

### Node-Based Design
The plugin uses Geometry Nodes for all procedural generation:

- **Torso Nodes**: Cylinder-based with float curve shaping for natural body contours
- **Limb Nodes**: Muscle definition using height-based displacement and noise
- **Head Nodes**: Sphere-based with facial feature displacement
- **Hand Nodes**: Modular finger system using instancing

### Scaffolding Philosophy
Following the plan's "scaffolding" approach:

1. **Curve-Based Scaffolding**: Spine curves define the primary structure
2. **Volumetric Construction**: Organic mass built around the scaffold
3. **Modular Assembly**: Repeated components (fingers, vertebrae) use instancing

### Advanced Techniques

#### SDF Emulation
The advanced nodes implement Signed Distance Field techniques for smooth blending between body parts.

#### Procedural Masking
Height-based masking allows for precise control over which areas are affected by displacement.

#### Modular Finger System
Fingers are generated using:
- Distribute Points on Faces for placement
- Instance on Points for finger generation
- Realize Instances for final geometry

## File Structure

```
Blender-Procedural-Human/
├── procedural_human/              # Main addon directory
│   ├── __init__.py               # Addon entry point
│   ├── advanced_nodes.py         # Advanced Geometry Nodes functions
│   ├── operators.py              # Operator classes
│   ├── panels.py                 # UI Panel classes
│   ├── menus.py                  # Menu classes
│   └── utils.py                  # Utility functions
├── package.py                    # Packaging script
├── test_plugin.py               # Testing script
├── README.md                    # This file
├── PlanOfTheWork.md             # Detailed technical plan
└── AGENTS.md                    # Development notes
```

## Development Notes

### Key Concepts Implemented

1. **Procedural Paradigm**: Non-destructive, rule-based character creation
2. **Scaffolding Approach**: Curve-based foundation with volumetric construction
3. **Modular Design**: Reusable components for different body parts
4. **Advanced Node Techniques**: SDF blending, procedural masking, instancing

### Technical Challenges Solved

- **Dependency Cycles**: Pure Geometry Nodes approach avoids Blender's dependency issues
- **Topology Control**: Advanced node setups provide clean, quad-based meshes
- **Performance**: Efficient instancing and node optimization
- **Flexibility**: Parametric control over all aspects of the character

## Future Enhancements

### Planned Features
- **Rigging Integration**: Procedural armature generation
- **Animation Support**: Procedural walk cycles and breathing
- **Texture Generation**: Procedural skin and hair textures
- **Crowd Generation**: Random character variation system

### Advanced Node Groups
- **SMPL-X Integration**: Data-driven parametric model support
- **Motion Capture**: Integration with external motion data
- **Advanced Shading**: Procedural material generation

## Troubleshooting

### Common Issues

1. **Node Errors**: Ensure Blender version 3.0+ is used
2. **Import Errors**: Check that all files are in the correct directory structure
3. **Performance Issues**: Reduce subdivision levels in node groups
4. **Missing Features**: Advanced nodes require the `advanced_nodes.py` file
5. **Node Type Errors**: Fixed compatibility issues with Blender 4.5+ by using `GeometryNodeTree` instead of `'GEOMETRY'`
6. **Float Curve Errors**: Replaced `GeometryNodeFloatCurve` with `ShaderNodeMapRange` for better compatibility
7. **Geometry Socket Errors**: Fixed node group interface access using `node_group.interface.new_socket()` for Blender 4.5+ compatibility
8. **Node Name Changes**: Updated node names for Blender 4.5+ (`MeshUVSphere` instead of `MeshSphere`, `SetPosition` for displacement)

### Debug Mode
Enable debug mode by setting:
```python
bpy.context.scene.debug_mode = True
```

## Contributing

This plugin is designed to be extensible. Key areas for contribution:

1. **Node Group Improvements**: Enhanced Geometry Nodes setups
2. **New Body Parts**: Additional anatomical components
3. **Animation Systems**: Procedural motion generation
4. **UI Enhancements**: Better parameter controls

## License

This project is open source. See the LICENSE file for details.

## Acknowledgments

Based on the comprehensive technical framework outlined in `PlanOfTheWork.md`, implementing modern procedural character creation techniques using Blender's Geometry Nodes system.
