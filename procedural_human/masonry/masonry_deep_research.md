
Procedural Generation of High-Fidelity Castle Masonry Geometry using Blender's Geometry Nodes for Normal Map Baking


I. Foundations of Procedural Masonry in Geometry Nodes (Conceptual Overview)

The task of procedurally generating castle masonry geometry requires a specialized workflow that leverages the non-destructive power of Geometry Nodes (Geo-Nodes) while satisfying the requirements of high-fidelity asset creation for rendering or game engines, specifically the need for an accurate baked normal map. The resulting asset must balance structural integrity—ensuring blocks adhere to a general pattern—with the high degree of organic irregularity observed in historical stonework.

I.A. Analytical Deconstruction of Castle Masonry Aesthetics

Visual analysis of typical castle structures, such as the provided reference image, indicates that the desired aesthetic is not clean, modern brickwork, but rather a robust, weathered style often categorized as Ashlar or Rubble-Ashlar. Key aesthetic observations dictate the procedural requirements:
Macro Structure: Blocks maintain a roughly horizontal alignment but show significant variation in individual width and height. A running bond (staggered layer) pattern is present, but it is often less regular than modern construction.
Meso Structure: Individual stones exhibit rotational misalignment and highly varied depth, protruding or receding unevenly from the wall plane. This depth variance is crucial for simulating the uneven setting of the blocks, which dramatically enhances the three-dimensional depth and realism of the eventual normal map.
Micro Structure: Edges are not sharp; they are heavily chipped, worn, and eroded, necessitating geometric removal and high-frequency displacement to simulate natural crumbling.1
The procedural system must therefore address these three layers of detail: the deterministic grid layout, the randomized transformation of blocks, and the fine-scale geometric erosion.

I.B. Initial Mesh Setup and Non-Destructive Principles

The procedural workflow commences with a base object, typically a simple, low-poly planar mesh, which represents the entire face of the wall. This base mesh will serve as the final low-poly target onto which the highly detailed geometry will be baked.
A fundamental requirement for any baking pipeline is a proper UV layout. Therefore, the base mesh must possess an established, clean, non-overlapping UV Map before the Geometry Nodes modifier is applied. This UV map defines the coordinates for the resulting texture map.3
The core advantage of using Geometry Nodes is maintaining a non-destructive workflow. The detailed, high-poly geometry is generated dynamically within the modifier stack. This allows for real-time adjustments to parameters (block size, stagger amount, level of erosion) without requiring manual re-sculpting or topological destruction. The high-poly mesh remains as instanced data until the moment geometric manipulation (like Booleans or complex displacement) or final output capture necessitates the Realize Instances node, minimizing computational overhead during early design phases.

I.C. Core Node Group Architecture Overview

To manage complexity, the Geo-Nodes setup is conceptually divided into four functional groups:
Input and Grid Generation: Defines the initial point distribution and dimensional parameters.
Instantiation and Sizing: Inserts the base cube geometry and applies the primary running bond staggering logic.
Randomization and Erosion (High-Poly Detail): Introduces per-block randomization, depth variation, and executes complex geometric operations such as diagonal cuts and edge chipping.
Output and Baking Capture: Handles the final realization of geometry and, critically, the advanced non-destructive capture of normal data for baking.

II. Generating the Structured Stone Grid (Running Bond Logic)

The creation of the staggered masonry pattern is achieved through a precise mathematical manipulation of coordinate system indices.

II.A. Creating the Base Point Distribution and Hierarchy

The most effective starting point is the Grid primitive, as it provides a structured array of points with predictable indices, critical for mathematical selection.4 The grid should be subdivided uniformly based on the desired target block dimensions (Width $\times$ Height), which are fed in as Group Input parameters.5
These grid points are then used as the input for the Instance on Points node. The geometry instanced at each point is a simple cube representing a single stone block. To ensure the necessary space for mortar gaps (which provide deep, bakeable trenches), the dimensions of the instance cube must be uniformly scaled down slightly relative to the grid spacing.

II.B. Mathematical Implementation of Staggering: Index and Modulo

The running bond pattern requires that alternating horizontal rows of blocks are offset by half the block's width. This pattern is enforced by isolating the row ID from the sequential point index and using the Math: Modulo function.6
The procedure for isolating and selecting alternating rows is detailed as follows:
Determine Points per Row ($P_{row}$): This value is calculated by dividing the total grid width by the parameter controlled Stone Width or by explicitly dividing the total number of points by the number of rows. This $P_{row}$ value is dynamically derived from the central Group Input parameters controlling the grid geometry.
Isolate the Column Index: The Index node, providing the sequential index of each point, is fed into a Math: Modulo node, using $P_{row}$ as the divisor. This operation returns the column position within each row, effectively restarting the count at zero for every new row.7
Calculate the Row Index: The result from the previous step is subtracted from the total sequential Index. This new value, after being divided by $P_{row}$, yields a stable, integer Row ID for every point in that row.
Select Alternating Rows: The Row ID is fed into a second Math: Modulo node, using 2 as the divisor. This returns 0 for even rows and 1 for odd rows. This binary output acts as a selection mask.
Apply the Offset: This selection mask (0 or 1) drives a Switch node. When the switch is active (e.g., for odd rows), a Set Position node applies a horizontal shift along the X-axis equal to half the controlled block width ($0.5 \times \text{Stone Width}$). This completes the classic running bond offset.8
The mathematical principle relies on the property of the modulo function: for a point index $I$, the row index $R$ can be determined, and the offset is applied based on whether $R$ is even or odd.

II.C. Parameterizing Block Dimensions (Height and Width Control)

Centralized control is paramount for usability. Group Input nodes are integrated at the beginning of the tree to control the $P_{row}$ calculation, the input Grid dimensions, the instance size, and the precise offset value. This ensures that a single adjustment to "Stone Width (W)" simultaneously updates the grid density, the block scale, and the required half-width translation in the Modulo logic.

II.D. Handling Non-Uniform Rectangular Blocks

Unlike highly standardized modern bricks, castle masonry blocks are rarely perfect rectangles. To achieve non-uniformity while preserving the overall structure and avoiding intersections, controlled random scaling must be applied after the primary staggering logic.9 A Random Value node connected to the instance scale allows for subtle variation in the X and Y dimensions.
It is critical that this randomization is applied in a way that the mean dimensions of the block remain consistent, preserving the structure needed for the Modulo calculation, but the individual stone dimensions vary slightly.10 This introduces the necessary visual imperfection expected in stonework without breaking the organized layout.

III. Achieving Organic Irregularity and Geometric Depth

Once the base grid is established, the blocks must be individualized to remove the machine-like uniformity inherent in procedural instancing. This involves adding unique rotation, depth, and highly detailed per-block noise.

III.A. Global Randomization: Scale, Depth (Z-Offset), and Minor Rotation

The procedural system uses Random Value nodes to introduce chaos into the structure.11
Depth Variance: A float Random Value is used to drive a Set Position node's Z-offset (depth along the wall normal). This offsets each stone instance randomly forward or backward from the wall plane. This depth variation is a high-impact detail, simulating the irregular placement of stones and ensuring that the baked normal map captures significant parallax and self-shadowing in the mortar gaps.
Scale and Rotation: Additional Random Value vectors are applied to the instance scale (further modifying dimensions) and rotation (minor rotations around the local Z-axis).5 These rotations should be small (e.g., $\pm 2^\circ$) to avoid visible intersecting geometry.

III.B. Critical Implementation: Per-Instance Noise Seeds

One of the limitations of global procedural noise is that if the object moves or is duplicated, the noise texture (which is usually based on world position) will slide across the surface, losing stability. Furthermore, if a shared noise texture is used for high-poly displacement or Boolean cutting, every single block will display the identical erosion pattern.
To ensure that the high-poly surface detail and any complex geometry modifications are unique for every single stone, the Per-Instance Noise Seed technique is employed. This relies on capturing a unique identifier for each stone instance.
The technical solution involves capturing the unique Instance Index or ID. This index is passed into the Vector input of any Noise Texture or Voronoi Texture used for subsequent displacement or Boolean masks.12 By applying a small scalar multiplication or rotation to the index before connecting it to the noise vector input, the single index value is converted into a unique 3D seed space. This method guarantees that a non-repeating noise pattern is generated across the entire wall surface, leading to greater realism in the erosion and chipping stages.

III.C. Advanced Technique: Incorporating Diagonal Cuts for Architectural Detail

Castle masonry often features non-rectangular shapes, particularly around architectural features like windows, doors, or buttresses, where stones must be cut diagonally to fit the opening.
Selection Mechanism: The target blocks for diagonal cutting must be identified. This can be achieved either by manually defining a geometric region (such as a bounding box around a planned opening) or, more procedurally, by selecting blocks based on their established row/column index IDs using comparison nodes.13
Boolean Cutter Generation: A custom cutter mesh—a simple geometric wedge or rotated prism—is created and instantiated only at the position of the selected blocks.
Execution: The core operation is the Mesh Boolean node, set to the Difference operation.15 This operation physically removes the volume of the cutter from the block instance. Since Boolean operations can only be performed on mesh geometry, the targeted instances must first pass through a Realize Instances node, temporarily converting them to mesh data.
It is important to note a critical warning regarding performance: Boolean operations, especially the Mesh Boolean node when applied to dense geometry, are computationally expensive and can be temperamental, sometimes leading to topological glitches if the meshes are non-manifold.16 Users must ensure robust geometry inputs and optimize the cutter density for stability.

IV. Detail Injection: Chipping, Erosion, and Weathering

The transformation from simple blocks to realistic masonry relies heavily on simulating natural wear and erosion, particularly along the exposed edges and faces.

IV.A. Simulating Edge Wear via Noise-Based Displacement (Initial Pass)

For subtle surface texture and minor edge breakdown, controlled displacement is highly effective. This detail is applied after the Realize Instances node to affect the actual stone mesh, but before any high-cost Boolean fracturing.
Edge Masking: To simulate mortar and natural wear, displacement must be limited to the edges of the stones. This boundary selection can be accomplished by using a proximity mask derived from the distance to the adjacent mortar geometry, or by leveraging generated attributes like the output of the Bevel node combined with the low-poly Geometry node's normal data.1
Application: A high-frequency Noise Texture is employed, ensuring it is driven by the unique per-instance seeds (as detailed in Section III.B) to guarantee non-repeating detail. This noise pattern modulates the Z-offset of vertices along the edges using a Set Position node, creating randomized chips and bumps characteristic of old, weathered stone.2 It is often necessary to use additional masking nodes to "pin" the perimeter of the block so that the displacement only occurs inward, preventing the stone from expanding beyond the defined mortar boundaries.18

IV.B. High-Fidelity Chipping using Volume Boolean Cutters (Maximum Detail)

For the most authentic, deep, and sharp fractured looks—which translate into excellent high-frequency normal map data—physical geometry removal via a Boolean operation is preferred over simple displacement.
Voronoi Cutter Generation: Realistic chipping requires an organic cutting mechanism. A highly detailed noise field, specifically a Voronoi Texture field, can be used to define the cutting shapes.19 A dense field of small, randomized points is scattered along the surface of the realized stones, and these points act as centers for the Voronoi cells. This Voronoi structure is then translated into a volumetric cutter.20
Targeted Boolean Operation: This generated volumetric noise field acts as the cutter for a final Mesh Boolean (Difference) operation, performed on the realized stone geometry. This technique yields the sharp, concave, and fractured edges observed in true ancient stonework.16

IV.C. Final Realization and Density Check

The resulting geometry, having undergone staggered placement, individual randomization, depth offset, and two passes of geometric wear (displacement and Boolean chipping), represents the final High-Poly Mesh. This geometry must be fully realized (Realize Instances) before proceeding to the baking stage. Depending on the scale and required fidelity, an additional Subdivision Surface modifier may be necessary after realization to provide sufficient vertex density, ensuring the captured normal map smoothly registers all high-frequency noise details.23

V. High-Fidelity Normal Map Baking Pipeline (Optimized for Geo-Nodes)

The procedural workflow culminates in the capture of the detailed high-poly geometric information onto the low-poly target mesh. Since the detailed geometry exists only within the Geometry Nodes modifier, an advanced baking approach is required.

V.A. Preparing the Low-Poly Target and Texture Asset

Standard baking prerequisites apply to the low-poly target:
The mesh must have clean UV coordinates.
In the Shader Editor of the low-poly material, a new Image Texture node must be added. A new image asset is created and assigned to this node.
Crucially, the Color Space of this new image texture must be explicitly set to Non-Color Data. Since normal maps are vector data representing direction rather than true color information, failure to set the color space correctly will result in inaccurate color transformation (gamma correction) and shading errors upon use.3 This image node must be the active selection when baking commences.

V.B. Standard Cycles Baking (The Conventional Path)

The conventional approach involves using Blender's native Cycles baking capability:
Set the Render Engine to Cycles.
In the Bake panel, set the Bake Type to Normal.
Enable Selected to Active (or Selected to Target in newer versions). This requires selecting the high-poly geometry first, followed by the low-poly target mesh (active selection).25
Set an appropriate Extrusion value (e.g., $0.1$ meters). Extrusion defines the distance rays are cast from the low-poly surface, ensuring they intersect and capture detail from protruding stones and the deep mortar gaps generated by the Geo-Nodes system.

V.C. Advanced Technique: Non-Destructive In-Node Normal Capture

While Section V.B is viable, it requires selecting two distinct objects and relies on the baked image asset. A more robust, fully procedural and non-destructive approach captures the normal data directly within the Geometry Nodes pipeline, ensuring the source data is precisely the calculated geometry.
This method uses the Raycast node to sample the high-poly surface normals onto the low-poly input geometry:
Raycast Capture: The low-poly input mesh (the plane with the modifier) is the source. The target geometry is the highly detailed, realized Geo-Nodes output (the dense masonry mesh). The Raycast node projects rays along the low-poly normals towards the high-poly target.
The Hit Normal output of the Raycast node captures the high-poly surface detail at the ray intersection point. This captured vector represents the surface orientation of the dense geometry.
Attribute Storage: This captured Hit Normal vector (which is currently in Object Space—aligned to the scene's coordinate system) is stored as a Vector attribute (e.g., "HighPolyNormal") on the low-poly input geometry using a Store Named Attribute node.

V.D. The Critical Step: Tangent Space Conversion

The normal vectors captured by the Raycast node are in Object Space. If this data were baked directly, the normal map would only shade correctly if the low-poly wall remained perfectly aligned with the world axes and was never rotated. For use in game engines or for re-using the asset in different orientations, Tangent Space normals are mandatory, as they define surface orientation relative to the mesh's UV coordinates and local surface.27
This conversion requires specialized vector mathematics:
Establishing the Local Frame: The low-poly mesh's local orientation frame is defined by its Normal vector (Z-axis alignment) and its Bitangent vector (Y-axis alignment relative to the UV map). These vectors are retrieved using the Geometry node.
Vector Rotation: The captured Object Space Normal vector is rotated into this local Tangent Space frame. This is accomplished using the Vector Rotate node, configured to rotate the captured normal vector around the low-poly mesh's Bitangent vector, effectively localizing the normal data.27
Color Mapping (Normalization): The resulting Tangent Space vector has components ranging from $[-1, 1]$. Since textures store color data in the $$ range, the vector must be mathematically normalized into this color range. This is achieved using the formula:

$$V_{Tangent} = (V_{Normalized} \times 0.5) + 0.5$$

This scales the vector components and shifts the resulting neutral normal (pointing straight out) to the RGB value $(0.5, 0.5, 1.0)$, or the characteristic neutral blue color.27
Final Bake Execution: The calculated, normalized Tangent Space vector is stored as a final attribute (e.g., "FinalNormal"). In the Shader Editor, an Attribute node accesses this "FinalNormal" data. By connecting this vector attribute directly to the Surface Output (or to the Color input of an Emission shader), the resulting value can be captured using the standard Cycles baking process set to Emit.28 This method captures the procedural normal map texture data as pure color output, completing the non-destructive pipeline.

VI. Summary of Customizable Parameters and Iterative Design

The power of this procedural setup lies in its flexibility, allowing artists and technical directors to rapidly iterate on the masonry design through a comprehensive set of exposed controls. The following table summarizes the essential customizable parameters integrated into the Geometry Nodes Group Input.
Table A: Procedural Control Parameters
Parameter
Geometry Node Input Type
Function and Nuance
Stone Width (W)
Float
Controls the grid unit size and base scaling. Directly drives the modulo divisor for staggering.
Stone Height (H)
Float
Controls row spacing and the Y dimension of instances.
Stagger Offset (%)
Float (0.0 - 1.0)
Defines the horizontal translation of alternating rows (e.g., 0.5 for a perfect half-brick offset).
Depth Variance (Z)
Float/Vector
Random extrusion/indentation applied per stone instance along the wall normal axis.
Erosion Seed
Integer
Unique seed input for noise textures driving chipping and surface roughness, ensuring randomness stability.
Diagonal Cut Selection
Index/Selection Mask
Used to target specific blocks or regions for the Boolean diagonal cutting operation.

The most complex procedural elements of the pipeline revolve around ensuring stability and portability. The decision to utilize the unique Instance Index to seed per-block noise textures is vital for procedural stability, preventing texture swimming and ensuring that every stone exhibits non-repeating wear and tear.12 Furthermore, the in-node capture and explicit conversion of normals into Tangent Space via vector mathematics ensures the resulting normal map is universally usable across different environments and object orientations.27
Table B: Tangent Space Normal Conversion Node Chain (Critical Baking Step)
Node
Input / Target
Function
Raycast
Target: Realized High-Poly
Captures the Object Space Normal from the detailed geometry onto the low-poly input.
Geometry Node
Read: Normal and Bitangent
Establishes the rotation frame of reference for the low-poly mesh using its local vectors.
Vector Rotate
Axis: Bitangent
Rotates the captured Object Space Normal into the local Tangent Space coordinate system.
Vector Math (Scale/Add)
Scale 0.5, Add 0.5
Normalizes the vector range from $[-1, 1]$ to the RGB color range $$ for texture storage.
Attribute Node
Read: Final $V_{Tangent}$
Transfers the calculated Tangent Space normal vector data into the Shader Editor.


Conclusion and Recommendations

The procedural generation of high-fidelity castle masonry geometry using Geometry Nodes is a rigorous process involving sophisticated grid mathematics, layered randomization, and geometrically destructive operations (Booleans) managed within a non-destructive wrapper.
The key to achieving the specified results—customizable staggered blocks with irregular and detailed surfaces—lies in the precise control over instance placement via the Modulo function, and the deployment of stable, per-instance noise seeding for organic detail.
For asset optimization and portability, the final step—the Tangent Space Normal conversion—is not optional. Using the Raycast and Vector Rotate nodes to calculate the normal map data internally and storing it as a color attribute for an Emit bake provides the highest level of control and ensures that the asset performs reliably when exported to external engines, regardless of rotation or scale. This sophisticated procedural approach transforms a simple plane into a detailed, ready-to-use game asset efficiently and non-destructively.
Works cited
Best procedural way to create chipped, worn edges? - Modeling - Blender Artists Community, accessed November 27, 2025, https://blenderartists.org/t/best-procedural-way-to-create-chipped-worn-edges/1141823
Rock Generator - Geometry Nodes (Blender Tutorial) - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=Hnm97p31R_k
Render Baking — Blender Manual, accessed November 27, 2025, https://docs.blender.org/manual/en/2.80/render/cycles/baking.html
geometry nodes - How can I make a grid with different offset with ..., accessed November 27, 2025, https://blender.stackexchange.com/questions/336625/how-can-i-make-a-grid-with-different-offset-with-geometrynodes
Customizable Brick Wall - Geometry Nodes (Blender Tutorial) - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=oE3GqhSd3NA
Using Geometry Nodes, how can I flip every other point in an array?, accessed November 27, 2025, https://blender.stackexchange.com/questions/234867/using-geometry-nodes-how-can-i-flip-every-other-point-in-an-array
Geometry nodes questions - Page 2 - Modeling - Blender Artists Community, accessed November 27, 2025, https://blenderartists.org/t/geometry-nodes-questions/1449700?page=2
Brick walls from a single curve! Geometry Nodes Blender - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=F9iaZZKCYeo
Uneven stonework with geometry nodes - possible? [closed] - Blender Stack Exchange, accessed November 27, 2025, https://blender.stackexchange.com/questions/338721/uneven-stonework-with-geometry-nodes-possible
Randomize Stacks With Geometry Nodes [Blender 4.0] - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=FSFB7t74T44
Randomize position of point distribute geometry nodes - Blender Stack Exchange, accessed November 27, 2025, https://blender.stackexchange.com/questions/243709/randomize-position-of-point-distribute-geometry-nodes
Randomize Noise Per Object (Geometry Nodes) - Blender Stack Exchange, accessed November 27, 2025, https://blender.stackexchange.com/questions/251587/randomize-noise-per-object-geometry-nodes
Blender Geometry nodes Index selection tools - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=dNHlmMcihGc
How to "grow" a selection around a index in geometry nodes? : r/blenderhelp - Reddit, accessed November 27, 2025, https://www.reddit.com/r/blenderhelp/comments/1ineknl/how_to_grow_a_selection_around_a_index_in/
How to make Boolean operations with geometry nodes in Blender part 1 - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=JwICObbT0go
Walls, walls and more walls (geonodes wall making thingy) - Page 2 - Works in Progress, accessed November 27, 2025, https://blenderartists.org/t/walls-walls-and-more-walls-geonodes-wall-making-thingy/1584273?page=2
The new geometry nodes boolean is awesome : r/blender - Reddit, accessed November 27, 2025, https://www.reddit.com/r/blender/comments/1o5xgwi/the_new_geometry_nodes_boolean_is_awesome/
How can you keep a Geometry Nodes displaced plane's edges at location 0 on the Z axis?, accessed November 27, 2025, https://blender.stackexchange.com/questions/298208/how-can-you-keep-a-geometry-nodes-displaced-planes-edges-at-location-0-on-the-z
LIVENODING Abstract Voronoi Splitter for 3D Mesh Using Geometry Nodes - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=UUEvSSXbGHQ
Geometry nodes for damage to stone - Procedural chipping - YouTube, accessed November 27, 2025, https://www.youtube.com/watch?v=lSrG6mYgk5Q
Anyone know of a good approach for voronoi edge smoothing? : r/proceduralgeneration - Reddit, accessed November 27, 2025, https://www.reddit.com/r/proceduralgeneration/comments/9ug6k1/anyone_know_of_a_good_approach_for_voronoi_edge/
Rough Cell Fracturing in Geometry Nodes - Blender Artists Community, accessed November 27, 2025, https://blenderartists.org/t/rough-cell-fracturing-in-geometry-nodes/1596074
How to bake a normal map into a mesh? I.E., create a high detail mesh from a low poly mesh and a normal/bump map? : r/3dsmax - Reddit, accessed November 27, 2025, https://www.reddit.com/r/3dsmax/comments/qr71ku/how_to_bake_a_normal_map_into_a_mesh_ie_create_a/
Baking a Normal Map: transferring details from a High Poly model to a L.P. model in Blender, accessed November 27, 2025, https://www.youtube.com/watch?v=bJdeTnbF-pA
Blender: High To Low Poly Normal BAKE - YouTube, accessed November 27, 2025, https://www.youtube.com/shorts/cissl9LKiUY
Render Baking - Blender 5.0 Manual, accessed November 27, 2025, https://docs.blender.org/manual/en/latest/render/cycles/baking.html
Normal Map Baking with Geometry Nodes, accessed November 27, 2025, https://nodesinteractive.com/normal-map-baking-with-geometry-nodes/
Texture baking from geometry nodes - Blender Artists Community, accessed November 27, 2025, https://blenderartists.org/t/texture-baking-from-geometry-nodes/1487646
