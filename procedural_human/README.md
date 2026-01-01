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

### For Development (VS Code Extension - Recommended)

This addon is optimized for development with the [Blender VS Code Extension](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development).

1. **Install the Blender VS Code Extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Blender" and install the extension by Jacques Lucke

2. **Open the Addon Folder in VS Code**:
   - Open the `procedural_human` folder in VS Code

3. **Start Blender from VS Code**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Blender: Start" and select it
   - Choose your Blender executable path (first time only)

4. **The extension automatically**:
   - Creates a soft link to Blender's addon directory
   - Enables hot-reloading (reloads addon on file save)
   - Provides debugging support with breakpoints

5. **Enable the Addon**:
   - In Blender, go to Edit > Preferences > Add-ons
   - Search for "Procedural Human Generator"
   - Enable the addon

**Benefits**:
- Automatic reloading on file save (no need to restart Blender)
- Full debugging support with breakpoints
- Integrated terminal output
- No manual installation needed

### For Distribution (Zip File)

1. Run `python package.py` to create `procedural_human.zip`
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Click "Install..." and select the zip file
5. Enable the add-on

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
│   ├── operators.py              # Operator classes
│   ├── panels.py                 # UI Panel classes
│   ├── menus.py                  # Menu classes
│   └── utils.py                  # Utility functions
├── package.py                    # Packaging script (for distribution)
├── README.md                     # This file
├── PlanOfTheWork.md              # Detailed technical plan
└── AGENTS.md                     # Development notes
```

## Development

### VS Code Workflow

This addon is configured for development with the Blender VS Code Extension:

1. **Open in VS Code**: Load the `procedural_human` folder
2. **Start Blender**: Use `Ctrl+Shift+P` > "Blender: Start"
3. **Edit Code**: Make changes to any `.py` file
4. **Auto-Reload**: The extension reloads the addon automatically on save
5. **Debug**: Set breakpoints in VS Code and debug directly in Blender

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
5. **Node Type Errors**: Fixed compatibility issues with Blender 4.5+ by using `GeometryNodeTree` instead of `'GEOMETRY'`
6. **Float Curve Errors**: Replaced `GeometryNodeFloatCurve` with `ShaderNodeMapRange` for better compatibility
7. **Geometry Socket Errors**: Fixed node group interface access using `node_group.interface.new_socket()` for Blender 4.5+ compatibility
8. **Node Name Changes**: Updated node names for Blender 4.5+ (`MeshUVSphere` instead of `MeshSphere`, `SetPosition` for displacement)

### Debug Mode
Enable debug mode by setting:
```python
bpy.context.scene.debug_mode = True
```
