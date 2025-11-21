# TODO: Procedural Human Generator - Uncompleted Tasks

This document lists all tasks from `PlanOfTheWork.md` that are not yet implemented in the current codebase.

## Section 2: Anatomical Blueprint - Core Strategies

### 2.2 Curve-Based Modeling for Skeletal Structures
- [ ] Implement proper curve-based scaffolding using `Curve Line` nodes
- [ ] Add `Resample Curve` nodes with controllable resolution for vertebrae/control points
- [ ] Use `Set Position` nodes with noise/texture inputs for natural curvature
- [ ] Implement curve attributes (Radius, Tilt, Normal) for controlling final mesh shape

### 2.3 Volumetric Construction for Organic Mass
- [ ] Implement SDF emulation using `Volume Cube` nodes (Method B - preferred)
- [ ] Create smooth minimum node groups for blending multiple shapes
- [ ] Implement volumetric merging for seamless body part connections
- [ ] Add `Mesh to Volume` and `Volume to Mesh` pipeline for organic blending

### 2.4 Modular Assembly with Instancing
- [ ] Use `Instance on Points` for modular components (vertebrae, phalanges)
- [ ] Implement attribute-based control for instance rotation and scale
- [ ] Add `Realize Instances` at appropriate points in the pipeline
- [ ] Create reusable phalange/finger segment modules

## Section 3: Constructing the Core - Torso and Spine

### 3.1 Generating the Spine: The Central Curve
- [ ] Replace hardcoded spine points with procedural `Curve Line` generation
- [ ] Add `Resample Curve` with Count mode for controllable vertebrae count
- [ ] Implement `Spline Parameter` node for height-based shaping
- [ ] Use `Set Position` with mathematical functions (Sine, Noise) for natural S-curve
- [ ] Expose posture parameters (amplitude, frequency) to modifier interface

### 3.2 Creating the Rib Cage and Pelvis Forms
- [ ] Use `Endpoint Selection` node to identify spine top/bottom
- [ ] Implement `Separate Geometry` or `Switch` nodes for isolating anchor points
- [ ] Create profile curves (`Curve Circle` or custom Bezier curves)
- [ ] Use `Instance on Points` to place profile curves at rib cage and pelvis
- [ ] Expose profile scale, rotation, and curve selection as parameters

### 3.3 Lofting the Torso: From Curves to Mesh
- [ ] Implement simple lofting with `Curve to Mesh` node
- [ ] Add procedural radius control using `Set Curve Radius` before lofting
- [ ] **Advanced**: Implement bridged edge loops method for superior topology
- [ ] Ensure all profile curves have matching point counts for advanced lofting
- [ ] Create custom node group for edge loop bridging

### 3.4 Adding Parametric Detail: Shoulders, Waist, and Volume
- [ ] Implement `Float Curve` node (or `ShaderNodeMapRange` fallback) for silhouette control
- [ ] Connect `Spline Parameter` factor to Float Curve input
- [ ] Use Float Curve output to drive `Set Curve Radius` for torso shaping
- [ ] Create intuitive curve profiles for: narrow waist, broad chest, wide hips
- [ ] Expose Float Curve control points as parameters

## Section 4: Modular Appendages - Limbs, Hands, and Feet

### 4.1 Procedural Limbs: Arms and Legs
- [ ] Replace cylinder-based limbs with proper curve-based scaffolds
- [ ] Use `Curve Line` with `Resample Curve` (Count=3) for joint definition
- [ ] Implement `Set Position` to move midpoint (joint) for elbow/knee bends
- [ ] Use `Curve to Mesh` with `Curve Circle` profile for limb volume
- [ ] Implement `Spline Parameter` + `Float Curve` for muscle definition
- [ ] Add bicep/tricep bulges and forearm tapering via Float Curve
- [ ] Add thigh/calf muscle shapes for legs
- [ ] Expose joint position as controllable parameter

### 4.2 The Hand Challenge: Multi-Stage Approach
- [ ] **Stage 1**: Generate palm from `Grid` primitive with `Set Position` shaping
- [ ] **Stage 2**: Identify knuckle vertices and generate finger curve scaffolds
- [ ] **Stage 2**: Instance `Curve Line` objects onto selected palm vertices
- [ ] **Stage 3**: Create reusable phalange geometry module
- [ ] **Stage 3**: Use `Resample Curve` on finger scaffolds for phalange placement
- [ ] **Stage 3**: Instance phalange meshes using `Instance on Points`
- [ ] **Stage 4**: Use `Realize Instances` to convert instances to geometry
- [ ] **Stage 4**: Apply volumetric merging (Mesh to Volume → Volume to Mesh) for seamless blending
- [ ] **Stage 4**: Alternative: Implement SDF-based blending for superior results
- [ ] Expose finger length, rotation, and spacing as parameters

### 4.2.1 Finger Generation Enhancements
- [x] Create basic finger geometry with three segments using Geometry Nodes
- [x] Add fingernail geometry on fingertip
- [x] Organize finger code into modular structure (`procedural_human/hand/finger/`)
- [x] Refactor finger framework to support variable segment count (2-3 segments)
- [x] Implement anatomical proportions from Proportions.md for each finger type (Thumb/Index/Middle/Ring/Little)
- [x] Add curl direction parameter (X/Y/Z axes, default Y-axis)
- [x] Reposition fingernail from tip to side of Distal segment (opposite curl direction)
- [x] Scale finger geometry to exactly 1 blender unit total length
- [x] Create armature with one bone per segment, oriented along curl direction
- [x] Implement automatic weight painting for finger segments with smooth joint falloff
- [x] Setup Inverse Kinematics chain for finger with IK target at tip
- [x] Create keyframe animation with finger curl (straight to curled state)
- [x] Drive finger curl animation by translating the IK target object
- [x] Align finger segment mesh radii with both X and Y profile curves
- [x] Ensure neighboring finger segments inherit final radii for seamless joints
- [x] Provide a Blender command palette script to reset the scene and create a procedural finger
- [x] Remove radius attribute dependency - use curve geometry positions directly for thickness

### 4.3 Feet and Toes
- [ ] Create base foot mesh (main body of foot)
- [ ] Generate toe scaffolds using curve-based approach
- [ ] Instance toe segments at front of foot
- [ ] Apply volumetric merge to blend toes with foot base
- [ ] Mirror feet for left/right placement
- [ ] Add foot positioning relative to leg bottom

### 4.4 Assembling the Body: Joining the Parts
- [ ] Use `Transform Geometry` nodes for precise component positioning
- [ ] Derive anchor points from torso mesh vertices (e.g., shoulder vertices)
- [ ] Implement `Join Geometry` node to combine all components
- [ ] **Advanced**: Add global volumetric merge for watertight mesh
- [ ] **Advanced**: Create continuous, seamless character mesh (for 3D printing/simulation)

## Section 5: The Human Head

### 5.1 Base Head Sculpting with Primitives and Displacement
- [ ] Use `Subdivided Cube` with "To Sphere" operation for clean topology
- [ ] Implement layered `Noise Texture` nodes for cranium, jaw, cheekbone forms
- [ ] Create procedural masking using `Position` node + `Color Ramp`
- [ ] Use Z-axis gradients to isolate jaw area for displacement
- [ ] Apply masks to `Set Position` Selection input for targeted sculpting
- [ ] Layer multiple displacement passes for complex facial forms

### 5.2 Adding Facial Features: A Modular Approach
- [ ] Create nose geometry (simple wedge shape or custom node group)
- [ ] Create ear geometry (low-poly model or procedural generation)
- [ ] Use `Transform Geometry` nodes for precise feature positioning
- [ ] Implement `Geometry Proximity` node to find nearest head surface points
- [ ] Apply volumetric merging (Mesh to Volume → Volume to Mesh) for seamless attachment
- [ ] Alternative: Use SDF-based blending for superior nose/ear integration
- [ ] Ensure seamless transitions where features join head

### 5.3 Procedural Hair System
- [ ] Define scalp area using vertex groups on head mesh
- [ ] Use `Distribute Points on Faces` with vertex group selection mask
- [ ] Implement `Add Hair Curves` node for initial strand generation
- [ ] Add `Clump Hair Curves` node for natural hair clumping
- [ ] Add `Frizz Hair Curves` node for realistic variation
- [ ] Add `Trim Hair Curves` node for haircut shaping
- [ ] Expose hair density, length, clumping, and frizz as parameters
- [ ] Package complete hair generator as reusable node group

### 5.4 Eyes and Detailing
- [ ] Create eye sockets during base head sculpting phase
- [ ] Instance `UV Sphere` objects for eyes within sockets
- [ ] Position eyes using procedural calculations or manual placement
- [ ] Generate procedural masks for skin regions (lips, cheeks, etc.)
- [ ] Output attributes from Geometry Nodes for shader use
- [ ] Link geometric attributes to material properties in shader editor

## Section 6: Procedural Rigging

### 6.1 The Hybrid Approach: Driving Traditional Armatures
- [ ] Create custom outputs from Geometry Nodes modifier (e.g., "Bicep Flex" float)
- [ ] Implement drivers to connect node outputs to armature bone properties
- [ ] Use drivers for pose-dependent shape changes (muscle bulges)
- [ ] **Advanced**: Implement procedural foot placement using `Raycast` node
- [ ] **Advanced**: Create Empty objects bound to raycast hit positions
- [ ] **Advanced**: Connect IK bones to procedurally calculated Empty positions
- [ ] Handle dependency cycle issues between Armature and Geometry Nodes

### 6.2 The Pure Approach: Armature-Free Deformation
- [ ] Implement direct vertex manipulation using `Set Position` nodes
- [ ] Calculate vertex positions based on control object proximity/transformation
- [ ] **Advanced**: Build "node-based skeleton" using curves inside node tree
- [ ] **Advanced**: Bind character mesh to curve skeleton
- [ ] **Advanced**: Calculate vertex-to-skeleton offsets and reapply during deformation
- [ ] **Advanced**: Recreate joint rotations and IK using vector math

### 6.3 Procedural Animation: Creating Motion with Nodes
- [ ] Use `Scene Time` node to access frame number/time
- [ ] Implement breathing animation using Sine/Cosine functions
- [ ] Add idle sway animations with procedural motion
- [ ] **Advanced**: Create procedural walk cycles
- [ ] **Advanced**: Calculate foot lifting and placement based on velocity
- [ ] **Advanced**: Implement dynamic locomotion adapting to speed/direction

## General Improvements

### Code Quality & Architecture
- [ ] Refactor torso to use proper curve-based scaffolding instead of cylinder primitive
- [ ] Integrate spine curve with torso generation (currently separate)
- [ ] Convert hand generation from separate objects to volumetric merged approach
- [ ] Add proper error handling and fallbacks for all node operations
- [ ] Create reusable node groups for common operations (lofting, volumetric merge, etc.)

### UI/UX Improvements
- [x] Implement collapsible finger panel with boolean toggle
- [x] Create collapsible finger_nail sub-panel as child of finger panel (separate file)
- [x] Create collapsible finger_segment sub-panel as child of finger panel (separate file)
- [x] Add profile curve selection (X and Y) for each finger segment type
- [x] Implement real-time profile curve updates for existing fingers
- [x] Create decorator system for auto-registering panels with auto-generated bl_* attributes
- [x] Implement folder hierarchy-based parent/child panel relationships
- [x] Refactor all panels to use decorator-based registration system
- [ ] Add more parameter controls to operator properties
- [ ] Create separate panels for different body parts (torso, limbs, head, etc.)
- [ ] Add presets for common body types (athletic, slender, muscular, etc.)
- [ ] Add tooltips and help text for all parameters

### Documentation
- [ ] Document all node setups and their purposes
- [ ] Create visual diagrams of node tree structures
- [ ] Add examples for each major feature
- [ ] Document parameter ranges and their effects
- [ ] Create troubleshooting guide for common issues

### Testing & Validation
- [ ] Test all features across different Blender versions (3.0+, 4.0+)
- [ ] Validate mesh topology quality
- [ ] Test performance with high-resolution settings
- [ ] Verify watertight mesh generation for 3D printing
- [ ] Test procedural animation performance

## Priority Levels

### High Priority (Core Functionality)
- Curve-based torso scaffolding
- Proper limb joints with curve scaffolds
- Feet and toes generation
- Facial features (nose, ears, eyes)
- Volumetric merging for seamless body parts

### Medium Priority (Enhanced Features)
- Procedural hair system
- Advanced lofting with bridged edge loops
- Rib cage and pelvis profile curves
- Procedural masking for head sculpting
- Watertight mesh generation

### Low Priority (Advanced Features)
- Procedural rigging (hybrid and pure approaches)
- Procedural animation (breathing, walk cycles)
- SDF emulation for superior blending
- Advanced foot placement with raycast
- Node-based skeleton system

---

## Section 7: Advanced Finger System Features

### 7.1 Profile Curve Management
- [x] Create operator to save profile curves back to codebase
  - [x] Implement `PROCEDURAL_OT_export_profile_curve` operator
  - [x] Extract curve data from selected Blender curve object
  - [x] Generate Python dictionary code from curve data
  - [x] Validate curve format (Bezier, correct structure)
  - [x] Write formatted code to `finger_segment_profiles.py`
  - [x] Update PROFILE_DATA registry automatically
  - [x] Add UI button in finger segment panel
  - [x] Show success/error messages to user

### 7.2 Variable Profile Curve Sampling
- [ ] Add dynamic sampling to finger segment node groups
  - [ ] Add "Sample Count" input socket to segment node group (IntProperty)
  - [ ] Get curve point count programmatically
  - [ ] Set minimum samples to max(curve_point_count, user_input)
  - [ ] Update grid resolution based on sample count
  - [ ] Expose sample count in finger segment panel UI
  - [ ] Add tooltip explaining performance implications
  - [ ] Test with different sample counts (3-64)

### 7.3 Curve-Based Segment Height
- [ ] Get segment height directly from profile curve geometry
  - [ ] Calculate Z-extent (max Z - min Z) from profile curve
  - [ ] Add toggle: "Use Curve Height" vs "Manual Length"
  - [ ] Create `get_curve_height()` utility function
  - [ ] Update segment node group to support both modes
  - [ ] Add UI toggle in finger segment panel
  - [ ] Ensure backwards compatibility with manual length
  - [ ] Update existing fingers to use appropriate mode

### 7.4 Operator Decorator System
- [x] Create operator registration decorator
  - [x] Create `procedural_human/operator_decorator.py`
  - [x] Implement `@procedural_operator` decorator
  - [x] Auto-generate `bl_idname` from class name (e.g., `CreateFinger` → `mesh.procedural_create_finger`)
  - [x] Auto-set common `bl_options` (REGISTER, UNDO)
  - [x] Create operator registry list
  - [x] Implement `register_all_operators()` function
  - [x] Implement `unregister_all_operators()` function
  - [x] Update existing operators to use decorator
  - [x] Update `operators.py` to use batch registration

### 7.5 Hierarchical Finger Segment Objects
- [ ] Refactor to separate objects per segment
  - [ ] Create parent finger object (empty or low-poly placeholder)
  - [ ] Create child objects for each segment (proximal, middle, distal)
  - [ ] Set up parent-child relationships with proper transforms
  - [ ] Pass geometry between segments using Object Info nodes
  - [ ] Store segment data in parent's custom properties
  - [ ] Implement "propagate to children" for operations:
    - [ ] Realize geometry on parent → realize all children
    - [ ] Create animation on parent → animate all children
    - [ ] Delete parent → delete all children
  - [ ] Implement "modify child only" operations:
    - [ ] Edit child segment doesn't affect parent or siblings
    - [ ] Individual segment property overrides
  - [ ] Dynamic segment count based on finger properties:
    - [ ] Read segment count from parent finger data
    - [ ] Add/remove child segments automatically
    - [ ] Apply golden ratio for segment lengths
    - [ ] Update when finger type changes (thumb=2, others=3)
  - [ ] Update UI to show hierarchical structure
  - [ ] Add outliner integration for easy navigation

### 7.6 DSL for Segment and Growth Plans
- [ ] Design and implement procedural growth DSL
  - [ ] Design DSL syntax specification:
    - [ ] `SEGMENT(placement, count, ratio, behavior)` pattern
    - [ ] `SYMMETRICAL(axis, count, pattern)` for mirroring
    - [ ] `GOLDEN` ratio constant
    - [ ] `CURL`, `ZIG_ZAG` behavior patterns
    - [ ] `TIP_TAIL` placement mode
  - [ ] Create DSL parser:
    - [ ] Tokenize DSL strings
    - [ ] Build abstract syntax tree (AST)
    - [ ] Validate syntax and semantics
    - [ ] Handle nested patterns
  - [ ] Implement DSL interpreter:
    - [ ] Translate AST to Blender operations
    - [ ] Generate geometry node trees from DSL
    - [ ] Apply ratio calculations (golden ratio, fibonacci)
    - [ ] Set up symmetry and mirroring
    - [ ] Configure behavior patterns (curl direction, alternating)
  - [ ] Create DSL examples:
    - [ ] `FINGER = SEGMENT(TIP_TAIL, 3, GOLDEN, CURL)`
    - [ ] `LEGS = SYMMETRICAL(Y, 2, SEGMENT(TIP_TAIL, 3, GOLDEN, ZIG_ZAG))`
    - [ ] `ARM = SEGMENT(TIP_TAIL, 2, [2,1], CURL)`
  - [ ] Add DSL property to objects:
    - [ ] Store DSL string in custom property
    - [ ] Regenerate from DSL on demand
    - [ ] UI text field for DSL input
  - [ ] Create DSL documentation and examples

### 7.7 Joint Segments Between Segments
- [ ] Implement joint segment concept
  - [ ] Define joint segment as special segment type
  - [ ] Joint properties:
    - [ ] Overlap amount (how much it extends into neighboring segments)
    - [ ] Blend factor (smoothness of transition)
    - [ ] Joint thickness ratio
  - [ ] Create joint segment node group:
    - [ ] Takes two segment endpoints as input
    - [ ] Generates overlapping geometry
    - [ ] Smooth blending using SDF or volume merge
  - [ ] Implement joint insertion logic:
    - [ ] Insert joints between regular segments
    - [ ] Update segment list: `[seg1, joint1, seg2, joint2, seg3]`
    - [ ] Like `join()` with separator: `join(segments, joint_segment)`
  - [ ] Update finger generation to include joints:
    - [ ] Add joint insertion step after segment creation
    - [ ] Apply smooth transitions at joint locations
    - [ ] Ensure seamless mesh topology
  - [ ] Add joint customization:
    - [ ] Configurable joint profiles
    - [ ] Per-joint overlap amounts
    - [ ] Joint-specific materials (e.g., skin wrinkles)
  - [ ] UI controls for joints:
    - [ ] Toggle joints on/off
    - [ ] Adjust joint overlap
    - [ ] Preview joint locations

---

**Note**: This TODO list is based on the comprehensive plan in `PlanOfTheWork.md`. Items are organized by section to match the original document structure. Current implementation has basic functionality but lacks many of the advanced procedural techniques described in the plan.

