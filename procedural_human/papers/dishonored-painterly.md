Procedural Synthesis of Painterly Aesthetics: A Technical Framework for Emulating Arkane and Fortiche Styles in Blender
1. Introduction: The Convergence of Traditional Artistry and Real-Time Rendering
The evolution of non-photorealistic rendering (NPR) has marked a significant departure from the industry's historical pursuit of hyper-realism. While the dominant trajectory of computer graphics has been the simulation of physical light transport—manifesting in ray tracing and physically based rendering (PBR)—a parallel lineage of aesthetic development has focused on the emulation of traditional artistic media. This domain, often termed "stylized rendering, " finds its apotheosis in the visual identities of Arkane Studios’ Dishonored franchise and Fortiche Production’s animated series Arcane. Both properties reject the stochastic perfection of the camera lens in favor of the interpreted imperfection of the human hand.
For the technical artist, reproducing these styles presents a unique paradox. The original assets for both Dishonored and Arcane rely heavily on labor-intensive, hand-painted textures. In Dishonored, artists manually painted diffuse maps to mimic the impasto of oil painting. In Arcane, the pipeline involves a complex hybridization where lighting information is often "baked" or painted directly onto the assets to achieve specific dramatic moods that dynamic lighting engines cannot easily replicate. The user requirement to achieve these aesthetics without large amounts of texture painting introduces a significant technical challenge: the translation of artistic intuition into procedural algorithms.
This report outlines a comprehensive methodology for constructing a procedural shader group in Blender that synthesizes the "moving oil painting" look of Dishonored with the "hand-crafted lighting" of Arcane. By leveraging geometric data, vector manipulation, and the non-physical transformation of lighting data (Shader-to-RGB), it is possible to create a "living canvas" that reacts dynamically to the 3D environment while retaining the tactile qualities of traditional media.
1.1 Defining the Target Aesthetics
To emulate a style procedurally, one must first deconstruct its visual components into quantifiable data points.
Aesthetic ComponentDishonored (Arkane Studios)Arcane (Fortiche Production)Procedural TranslationSurface TextureVisible, thick oil paint strokes; tactile rugosity. Smooth, matte painting finish; "gritty" but integrated. Voronoi-based normal perturbation with domain warping. Edge TreatmentWorn, chipped paint revealing underlying material; angular highlights. Sharp, inked edges; rim lighting used to define silhouette. Geometry/Bevel normal comparison (Dot Product masking). Lighting ModelRealistic interaction with stylized normals (Standard shading). Hand-painted light/shadow; "Baked" look with dramatic color shifts. Shader-to-RGB quantization with warm/cool color separation. Form LanguageAngular, planar sculpting; exaggerated anatomy (Peyravernay style).2.5D integration; angular but fluid; 3D models matching 2D backgrounds. Planar modeling practices; "Scraped" normal maps. Color PaletteMuted, melancholic; warm lights vs. cool shadows. Vibrant, high contrast; neon accents; distinct atmospheric color grading. Parametric Color Ramps with HSV hue shifting inputs.
1.2 The Procedural Imperative
The traditional workflow for these styles involves unwrapping a model’s UVs and spending hours in software like Substance Painter or Photoshop, manually placing every brush stroke and edge highlight. While this yields high artistic control, it is destructive and non-scalable. If the model changes, the texture must be repainted. A procedural approach, conversely, utilizes mathematical functions in 3D space (Object Coordinates) to generate these effects. This allows the "paint" to exist as a volumetric field through which the object moves, or as a surface property that automatically adjusts to geometric deformations. The challenge lies in introducing enough "controlled chaos" to prevent the procedural algorithms from looking like sterile mathematical patterns.
2. Theoretical Framework: The Physics of "Fake" Surfaces
The core of the painterly aesthetic is the simulation of surface imperfection. In the real world, surfaces have microscopic imperfections that scatter light (roughness). In a painting, the "surface" is the paint itself—the bristles of the brush leave ridges and valleys that catch the light.
2.1 The Normal Map as a Canvas
In 3D rendering, the Normal Vector defines the orientation of a surface point relative to a light source. By manipulating this vector before the lighting calculation occurs, we can trick the render engine into shading a flat polygon as if it were a complex, rugged surface of dried paint. This is distinct from displacement mapping, which moves actual geometry. For the Dishonored look, the silhouette of the object remains angular and sharp, while the internal shading suggests a depth of texture that isn't geometrically present.
2.2 The Mathematics of Brush Strokes (Voronoi Diagrams)
The primary mathematical function used to simulate paint dabs is the Voronoi diagram. A Voronoi pattern partitions space into regions based on distance to a set of seed points.
Euclidean Distance: Produces circular, organic shapes.
Manhattan Distance: Produces blocky, rectilinear shapes.
Chebychev Distance: Produces distinct square/diagonal patterns.
For Dishonored, which features "exaggerated angular character sculpts" and textures that "mimic oil paintings" , a standard soft noise is insufficient. Paint is applied in discrete strokes. The Voronoi function, particularly when set to compute the distance to the closest feature point (F1), creates cellular structures that resemble the individual facets of a wide, flat brush.
2.3 Domain Warping and "Flow"
Real brush strokes are rarely perfect static cells; they are dragged across the canvas. To replicate this, we employ Domain Warping. Instead of sampling the Voronoi texture at coordinate $\vec{p}$, we sample it at $\vec{p} + f(\vec{p})$, where $f(\vec{p})$ is a low-frequency noise function.
This distorts the coordinate system itself. When a Voronoi texture is mapped onto these distorted coordinates, the cells stretch and twist, simulating the wet-on-wet dragging of paint. This introduces the necessary organic irregularity to break the "CG look."
3. Geometric Prerequisites: Modeling for the Shader
A procedural shader does not exist in a vacuum; it relies on the underlying geometry to provide data for its calculations. The distinct look of Dishonored and Arcane is as much about the modeling as the texturing.
3.1 Planar Sculpting and Angularity
The concept art of Cedric Peyravernay, central to the Dishonored aesthetic, emphasizes angularity. Faces are not smooth ovals but collections of distinct planes. When modeling for this shader, one must avoid the "subdivision surface" smoothness typical of Pixar-style animation.
The "Scrape" Technique: Artists should use the Scrape and Flatten brushes in sculpting to create hard edges between muscle groups and facial features.
Implication for Shading: The procedural shader relies on these hard geometric transitions to trigger edge highlights (via the Bevel/Dot Product method) and to break up the Voronoi pattern. A perfectly smooth sphere will look like a procedural marble; a sphere with planar facets will look like a painted object.
3.2 Coordinate Systems and UVs
While the goal is to avoid texture painting, proper texture coordinates remain essential.
Object Coordinates: For static objects or rigid bodies (weapons, buildings), Object Coordinates are superior. They allow the noise texture to be consistent in world scale—a brush stroke on a wall will be the same size as a brush stroke on a door.
UV Coordinates: For deforming characters, Object Coordinates fail because the texture will "swim" through the character as they move (the "shower door effect"). For characters, the shader must use UV coordinates. However, unlike traditional texturing, the UVs do not need to be efficiently packed or non-overlapping in the same strict sense. The primary requirement is that they are low-distortion so the procedural noise maps correctly to the surface.
4. The Surface Texture Engine: Procedural Brush Strokes
This section details the construction of the "Paint Surface" component of the shader group. This component's responsibility is to generate a Normal Map that creates the tactile feel of oil paint.
4.1 Base Noise Architecture
The texture is generated by layering multiple frequencies of noise.
Macro-Texture (The Canvas): A high-scale, low-intensity noise texture simulates the grain of the canvas or the underlying material.
Meso-Texture (The Strokes): A Voronoi texture simulates the individual dabs of paint.
Micro-Texture (The Bristles): A stretched, high-frequency noise creates the streaks within the strokes.
4.2 Creating the "Stroke" Look (Node Setup)
The core mechanism uses a Voronoi Texture driven by Distorted Vectors.
Step 1: Coordinate Distortion
Input: Texture Coordinate (Object or UV).
Modifier: Add a Noise Texture node. Scale: ~5.0.
Mix: Use a Mix Color node (Linear Light). Input A: Original Coordinates. Input B: Noise Texture Color. Factor: 0.1 - 0.2.
Result: This creates a coordinate vector that "wobbles."
Step 2: Voronoi Application
Node: Voronoi Texture.
Input: The distorted vector from Step 1.
Settings: 4D (for seed variation), Smooth F1, Euclidean.
Scale: This is a critical artistic parameter exposed to the user. A lower scale implies a larger brush; a higher scale implies fine detail work.
Step 3: Normal Map Generation
Conversion: The Voronoi texture outputs a Distance or Position value. This scalar data is fed into a Bump Node.
Strength: Kept low (0.1 - 0.3). We want to suggest surface texture, not create a topographic map.
Output: The Normal output of the Bump Node is plugged into the shader's Normal input.
4.3 Directional Flow and Anisotropy
To satisfy the Arcane requirement of directional strokes that follow the form (e.g., strokes wrapping around an arm), isotropic noise is insufficient.
Tangent Vectors: We utilize the Tangent node in the shader editor. This provides a vector direction that runs along the surface of the mesh (u/v direction).
Vector Math: By taking the Cross Product of the Surface Normal and the Tangent, we get a consistent directional vector.
Stretching: We separate the XYZ components of our mapping vector. We multiply the X component (parallel to flow) by a small factor (e.g., 0.1) and the Y component (perpendicular) by a large factor (e.g., 5.0).
Result: When applied to a Noise Texture, this stretches the noise into long streaks that follow the model's UV flow or topology, effectively mimicking brush strokes dragged along the surface form.
5. The Edge Wear Engine: Procedural Weathering
One of the defining features of the Dishonored art style is the "worn edge" look—paint chipped away on corners to reveal the metal or wood underneath. Manually painting these masks is tedious. We can generate them mathematically using the geometry of the mesh itself.
5.1 The Bevel / Dot Product Method
This is the industry-standard procedural technique for edge detection in Blender.
Theory:
The Geometry node provides the true normal vector ($\vec{N}_{geo}$) for every shading point. On a sharp corner of a low-poly mesh, this normal changes abruptly from one face to the next. The Bevel node, however, calculates a smoothed "fake" normal ($\vec{N}_{bevel}$) that rounds off that corner.
On a flat face, $\vec{N}_{geo} \approx \vec{N}_{bevel}$.
On a sharp edge, $\vec{N}_{geo} \neq \vec{N}_{bevel}$.
Implementation:
Nodes: Geometry Node (Normal output) and Bevel Node (Normal output).
Operation: Vector Math Node set to Dot Product.
$$D = \vec{N}_{geo} \cdot \vec{N}_{bevel}$$
Analysis:
If vectors are identical, $D = 1$.
As vectors diverge (at edges), $D < 1$.
Processing: Feed the result into a Map Range node.
Input Min/Max: 0.9 to 1.0 (isolating only the areas where they match closely).
Output Min/Max: 1.0 to 0.0 (inverting so edges become white).
Artifact Control: The Color Ramp can be used to sharpen this mask, creating the "chipped" look rather than a soft gradient.
5.2 Curvature and Pointiness (Cycles vs. Eevee)
The Pointiness attribute (Geometry Node) is another method but relies heavily on mesh topology density. The Bevel method is topology-agnostic regarding density but computationally heavier.
Optimization Note: The Bevel node is computationally expensive in Cycles. For Eevee (real-time rendering), it often requires baking. However, recent updates to Blender's Eevee Next engine have improved support for curvature detection. If real-time performance is critical (e.g., game assets), this edge mask should be baked into a texture. For the "Shader Group" requested, including a switch to toggle Edge Wear off for performance is a recommended best practice.
6. The Lighting Engine: Non-Photorealistic Color Response
This section addresses the crucial difference between Dishonored (realistic light on stylized texture) and Arcane (stylized light on stylized texture). The user wants a system that can do both or blend between them.
6.1 The Shader-to-RGB Workflow
The secret to the Arcane look in Blender is the Shader to RGB node. This node intercepts the calculated lighting data (diffuse and specular) before it is output to the screen, converting it into raw color data that can be manipulated.
The Pipeline:
Principled BSDF (or Diffuse BSDF): Calculate the physical interaction of light with the surface (including the normal map from Section 4).
Shader to RGB: Convert this light interaction into a gradient (Black = Shadow, White = Light).
Color Ramp: Map this gradient to a specific color palette.
6.2 Managing Color Bands (The "Paint" Palette)
Instead of a smooth fade from light to dark, painterly styles often group values.
Constant Interpolation: Creates hard edges (cel shading).
B-Spline Interpolation: Creates incredibly smooth, non-linear gradients that mimic soft airbrushing.
For the "Dishonored" feel, which is not strictly cel-shaded, using Linear or Ease interpolation is best. We define three zones:
The Shadow: Usually cool and desaturated (e.g., slate blue).
The Midtone: The local color of the object (e.g., olive green for a uniform).
The Highlight: A warm, desaturated peak (e.g., pale yellow).
6.3 Warm/Cool Shading Logic (The Peyravernay Effect)
A key characteristic of Cedric Peyravernay’s art (and Arcane) is the temperature shift between light and shadow. A red jacket doesn't just get "darker red" in shadow; it shifts towards purple or blue.
Procedural Implementation:
Inside the node group, we do not just expose a single "Base Color." We expose:
Lit Color
Shadow Color
Shift Factor
We use the Shader-to-RGB output as a mask.
$$\text{Final Color} = \text{Mix}(\text{Shadow Color}, \text{Lit Color}, \text{Light Factor})$$

This allows the user to define that a "Red" material is actually Red in the light and Blue in the shadow, mimicking the rich color theory of the source material without hand-painting the gradients.
6.4 Rim Lighting (Fresnel)
Arcane characters often have a strong "rim light" that separates them from the background, even if no light source justifies it.
Fresnel Node: Calculates the angle between the view vector and the surface normal. High values occur at the grazing angles (edges of the silhouette).
Layering: We add (Screen or Add mode) this Fresnel mask on top of our Base Color. This mimics the "backlighting" technique used in 2.5D animation to pop characters from the background.
7. Compositing: The Final Polish
The shader operates on the surface, but the "painterly feel" often requires full-frame processing to unify the image. The Dishonored and Arcane look is finalized in the post-processing stage.
7.1 The Kuwahara Filter
The Kuwahara filter is a non-linear smoothing filter that preserves edges while flattening internal areas. It is the digital equivalent of a painter simplifying a complex scene into broad strokes.
Mechanism: For every pixel, it calculates the mean and variance of color in four sub-quadrants. It then chooses the mean color of the quadrant with the lowest variance (the most uniform area).
Effect: High-frequency noise (like the Voronoi bump map) is smoothed out into "pools" of color, but the distinct edges of objects (and the sharp shadows created by the planar geometry) are preserved.
Blender Implementation: The Kuwahara node (introduced in Blender 4.0) should be added in the Compositor.
Size: Controls the abstraction level. A size of 2-5 pixels retains detail; 10+ becomes abstract art.
Anisotropy: Use the anisotropic version to allow the filter to follow the flow of the image features, reinforcing the directional strokes set up in the shader.
7.2 Chromatic Aberration and Grain
Dishonored has a gritty, steampunk aesthetic. Arcane has a cinematic, filmic quality. Both benefit from lens imperfections.
Lens Distortion: Adding a tiny amount of Dispersion (0.01 - 0.03) separates the RGB channels at the edges of the frame. This mimics a physical lens and breaks the "perfect CG" look.
Film Grain: Overlaying a subtle grain texture helps to dither the smooth gradients created by the Shader-to-RGB node, preventing color banding and adding texture to the darks, similar to the canvas grain in Dishonored.
8. Implementation Strategy: The "Arkane" Node Group
To satisfy the user's request for a "Shader Group, " we must package these techniques into a reusable tool. Below is the specification for the master node group interface.
8.1 Group Interface Parameters
Input ParameterDescriptionInternal MappingMain AlbedoThe base color of the object. Feeds into the Lit Color slot. Shadow TintColor to tint the shadows (usually Blue/Purple). Mixed with Albedo for Shadow Color slot. Paint RoughnessHow "wet" or "dry" the paint looks. Controls Specular Roughness. Brush ScaleSize of the procedural strokes. Controls Voronoi Texture Scale. Stroke IntensityDepth of the normal map bump. Controls Bump Node Strength. Edge WearAmount of damage on corners. Controls Map Range max/min for Edge Mask. Wear ColorColor of the material under the paint. Mix Color B slot (driven by Edge Mask). Lighting StyleSlider: 0 = Realistic (Dishonored), 1 = Stylized (Arcane). Mixes between BSDF output and Shader-to-RGB output.
8.2 Building the Group (Step-by-Step)
Texture Coordinate Block: Create the Object Coordinate -> Noise Distortion setup.
Normal Block: Create the Voronoi setup. Mix with a secondary "Canvas Grain" noise. Feed to Bump Node.
Edge Block: Setup Geometry Normal / Bevel Normal dot product. Feed into a Color Ramp for tuning.
Shading Block:
Path A (Realism): Principled BSDF using the Normal Block and Edge Block for Albedo/Roughness.
Path B (Stylized): Shader-to-RGB setup using the output of Path A's BSDF. Feed into Color Ramp (Lit/Shadow mixing).
Output Mix: Mix Path A and Path B based on the "Lighting Style" slider.
9. Conclusion
The "Dishonored" and "Arcane" aesthetics, while rooted in the manual labor of traditional illustration, can be effectively synthesized using modern procedural pipelines. By understanding the mathematical basis of these styles—the planar geometry, the faceted normals of the Voronoi diagram, the edge-isolating power of the Dot Product, and the non-physical quantization of light via Shader-to-RGB—artists can create a flexible "smart material" that emulates the hand-crafted look without the bottleneck of hand-painting.
This report demonstrates that the "painterly feel" is not a singular effect but a composite of surface imperfection, geometric simplification, and stylized light response. The proposed Node Group architecture encapsulates these pillars, providing a powerful tool for indie developers and technical artists to achieve AAA-quality stylized visuals with a fraction of the manual overhead.
9.1 Future Outlook: Real-Time vs. Offline
As Blender’s Eevee engine evolves (Eevee Next), features like Ray Tracing and screen-space global illumination are bridging the gap between real-time rendering and the high-fidelity light transport of Cycles. This suggests that the hybrid workflow—using procedural shaders for the "look" but real-time engines for the "feedback"—will become the standard for stylized productions. The procedural shader described herein is future-proof, relying on fundamental vector math that transcends specific render engine versions.
