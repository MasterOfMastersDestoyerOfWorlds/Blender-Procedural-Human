# Ixdar Procedural Geometry Nodes Implementation Plan

This document outlines the geometry node groups needed to procedurally generate the 3D models and environments for Ixdar, a volcanic island trading/survival game with colonial-era aesthetics.

## Table of Contents

1. [General-Purpose Node Groups](#general-purpose-node-groups)
2. [Terrain & Environment Node Groups](#terrain--environment-node-groups)
3. [Flora & Vegetation Node Groups](#flora--vegetation-node-groups)
4. [Fauna & Creature Node Groups](#fauna--creature-node-groups)
5. [Architecture & Building Node Groups](#architecture--building-node-groups)
   - [Detailed Building Component System](#detailed-building-component-system)
     - [Core Structure](#core-structure)
     - [Windows on Faces](#windows-on-faces)
     - [Doors](#doors)
     - [Stairs](#stairs)
     - [Railings on Edges](#railings-on-edges)
     - [Roofing & Shingles](#roofing--shingles)
     - [Trim & Architectural Detail](#trim--architectural-detail)
     - [Compound Building Generators](#compound-building-generators)
6. [Infrastructure & Road Node Groups](#infrastructure--road-node-groups)
7. [Vehicle & Transport Node Groups](#vehicle--transport-node-groups)
8. [Props & Items Node Groups](#props--items-node-groups)
9. [Character & Clothing Node Groups](#character--clothing-node-groups)
10. [VFX & Atmospheric Node Groups](#vfx--atmospheric-node-groups)
11. [Missing Assets Analysis](#missing-assets-analysis)
12. [Implementation Priority](#implementation-priority)

---

## General-Purpose Node Groups

These are foundational building blocks reused across many asset generators.

### Displacement & Weathering

| Node Group | Description | Used By |
|------------|-------------|---------|
| `worn_edges.py` | Edge wear/chipping using edge angle + noise displacement | Buildings, ships, decayed artifacts, statues |
| `rust_corrosion.py` | Procedural rust/corrosion patterns using Voronoi + noise | Decayed artifacts, metal structures, anchors |
| `moss_growth.py` | Organic moss/lichen accumulation based on upward-facing normals + moisture | Buildings, stones, deadwood, statues |
| `weathering_composite.py` | Combines wear, rust, moss based on age/exposure parameters | All outdoor assets |

### Geometric Primitives

| Node Group | Description | Used By |
|------------|-------------|---------|
| `basalt_columns.py` | Hexagonal column generator (existing plan) | Volcanic terrain, cliffs, rock formations |
| `rock_scatter.py` | Scattered rock placement with size/rotation variation | Terrain, roads, quarries |
| `plank_generator.py` | Procedural wood planks with grain, knots, warping | Ships, buildings, docks, carts |
| `rope_generator.py` | Twisted rope/cordage from curve input | Ship rigging, flags, nets |
| `chain_generator.py` | Linked chain from curve path | Anchors, drawbridges, lamps |
| `cloth_simulation_base.py` | Draping cloth with wind influence | Flags, sails, clothing, tents |

### Surface Treatments

| Node Group | Description | Used By |
|------------|-------------|---------|
| `snow_accumulation.py` | Snow buildup on upward faces + wind direction | Iceland outer layer, icebergs |
| `mud_splatter.py` | Mud/dirt accumulation on lower surfaces | Vehicles, boots, road edges |
| `ice_formation.py` | Ice/frost crystalline displacement | Icebergs, frozen terrain, cold weather effects |
| `salt_deposits.py` | White crystalline salt buildup | Coastal rocks, dried pools |

### Instancing & Scattering

| Node Group | Description | Used By |
|------------|-------------|---------|
| `terrain_scatter.py` | Point distribution with slope/elevation masking | All vegetation, rocks, debris |
| `edge_scatter.py` | Points along mesh edges for detail placement | Road edges, wall tops, cliff lines |
| `density_gradient.py` | Falloff-based instance density | Biome transitions, city outskirts |

---

## Terrain & Environment Node Groups

### Core Terrain

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `volcanic_island_terrain.py` | Multi-layer volcanic island with central well, coastal zones, elevation rings | Volcanic Island Terrain, Volcanic Biome Zones |
| `central_well.py` | Descending spiral/shaft structure for the treasure well | Central Well Structure |
| `coastal_terrain.py` | Beach/shore transitions with tide lines, erosion | Coastal Village Environment, Coastal Locations |
| `cliff_face.py` | Vertical rock faces with ledges, overhangs, caves | Island Interior Environment |
| `lava_flow_terrain.py` | Cooled lava fields with cracks, texture variation | Volcanic Biome Zones |

### Biome-Specific

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `iceland_outer_layer.py` | Sparse, windswept terrain with exposed rock, minimal vegetation | Sparse Vegetation, outer layer flora |
| `inner_biome_transition.py` | Visual distinction between biome depth layers | Biome Layer Transitions |
| `treasury_room.py` | 3D treasure vault environment with coin piles, shelves | Treasury Room Environment |

### Atmospheric

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `time_fog_volume.py` | Volumetric fog boundary visualization | Time Fog Visual Effect, Time Fog Particle Effect |
| `skybox_clouds.py` | Cloud layer generator for skybox | Skybox with Clouds |
| `ocean_surface.py` | Animated ocean with wave displacement | Main Menu Ship Scene |

---

## Flora & Vegetation Node Groups

### Trees & Large Plants

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `sparse_tree.py` | Stunted, wind-bent trees (Iceland-style birch, rowan) | Sparse Trees |
| `deadwood.py` | Large knotted dead trees, bleached driftwood | Deadwood |
| `inner_layer_tree.py` | Exotic/alien vegetation for deeper biomes | Inner Layer Flora |
| `palm_variant.py` | If tropical elements exist in deeper layers | Inner Layer Flora |

### Ground Cover

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `razor_grass.py` | Sharp, metallic-looking grass that "lights up" on touch | Razor Grass |
| `moss_patches.py` | Ground moss/lichen clusters | Sparse Vegetation |
| `tundra_grass.py` | Short, sparse grass tufts | Sparse Vegetation |
| `seaweed.py` | Coastal kelp and seaweed | Coastal Locations |

---

## Fauna & Creature Node Groups

### Domestic/Wildlife (Outer Layer)

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `sheep.py` | Base sheep mesh with wool density variation | Sheep |
| `reindeer.py` | Reindeer with antler variants | Reindeer |
| `wild_dog.py` | Feral dog variants | Wild Dogs |
| `puffin.py` | Puffin seabird model | Puffins |
| `mink.py` | Small mink/mustelid | Mink |
| `horse.py` | Draft horse variants for caravans | Horses |
| `fish.py` | Multiple fish species for fisheries | Fish |

### Creatures & Demons

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `alchemical_demon_base.py` | Base demon structure with transmutation effects | Alchemical Demon (Coastal), Alchemical Demon (Island Interior) |
| `demon_coastal_variant.py` | Sea-emerging demon with aquatic features | Alchemical Demon (Coastal) |
| `demon_interior_variant.py` | More dangerous interior demon forms | Alchemical Demon (Island Interior) |
| `tongue_whipping_deer.py` | Mutant deer with weaponized tongue | Tongue-Whipping Deer |
| `faceless_statue_creature.py` | Pale, warm, faceless humanoid statues | Faceless Warm Statues |
| `exotic_creature_base.py` | Framework for monstrous inner layer creatures | Exotic Creatures |

### Utility Animals

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `rat.py` | Scurrying rat for ship scenes | Rat |
| `bird.py` | Flying bird silhouettes | Bird |

---

## Architecture & Building Node Groups

### Colonial Era Buildings

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `timber_frame_building.py` | Half-timbered colonial structure | Housing Buildings, various buildings |
| `stone_building.py` | Stone masonry buildings | Cities |
| `thatched_roof.py` | Organic thatch roofing | Coastal Village Environment |
| `slate_roof.py` | Slate/tile roofing | Cities, nicer buildings |
| `chimney.py` | Stone chimney with smoke option | Housing Buildings |
| `window_frame.py` | Period-appropriate windows with panes | Captain's Quarters |
| `door_frame.py` | Wooden doors with hardware | All buildings |

### Specialized Structures

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `fishery_building.py` | Coastal fishing structure with drying racks, nets | Fishery Building |
| `quarry_building.py` | Stone/rock quarry infrastructure | Quarry Building |
| `horse_station.py` | Way station for horse changes | Horse Station Building |
| `toll_booth.py` | Road toll collection booth | Toll Booth |
| `warehouse.py` | Storage warehouse structure | Warehouse/Storage Building |
| `train_station.py` | Railway station building | Train Station |
| `city_station.py` | Urban caravan station | City Station Building |
| `headquarters.py` | Player HQ building variants | Headquarters Building |

### Fortifications & Infrastructure

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `city_walls.py` | Defensive stone walls | Cities |
| `watchtower.py` | Guard/lookout tower | Cities, patrol infrastructure |
| `dock_pier.py` | Wooden pier/dock structure | Coastal areas |
| `lighthouse.py` | Coastal navigation lighthouse | Coastal Locations |

### Detailed Building Component System

The following node groups form a modular building generation system. These are low-level components that combine into compound building generators.

#### Core Structure

| Node Group | Description | Inputs | Technique |
|------------|-------------|--------|-----------|
| `floor_plan_from_curve.py` | Extrudes floor polygon from closed curve | Curve, Wall Thickness, Height | Curve to Mesh → Extrude |
| `wall_extrusion.py` | Creates walls with thickness from face edges | Face, Thickness, Height | Edge selection → Extrude → Solidify |
| `multi_story_stack.py` | Stacks floor instances with floor plates | Base Geometry, Stories, Story Height | Instance on Points (Z offset) |
| `foundation.py` | Stone/concrete foundation base | Footprint, Height, Batter Angle | Extrude down with slight inward taper |

#### Windows on Faces

| Node Group | Description | Technique |
|------------|-------------|-----------|
| `window_placement.py` | Distributes window positions on wall faces | Grid distribution on face, inset from edges using face bounds |
| `window_cutout.py` | Boolean-cuts window openings into walls | Extrude Mesh (Individual) inward → Delete Faces |
| `window_frame.py` | Creates frame geometry around opening | Profile curve swept along opening edge loop |
| `window_panes.py` | Subdivides opening into glass panes | Grid within frame bounds → Mullion extrusion |
| `window_sill.py` | Projecting sill below window | Extrude bottom edge outward + down |
| `window_lintel.py` | Header/arch above window | Extrude top edge → Optional arch deformation |
| `shutters.py` | Hinged side panels | Plane instances at frame sides with rotation offset |
| `dormer_window.py` | Roof-mounted window with mini-roof | Compound: roof cutout + frame + mini gable roof |

**Window Pipeline:**
```
Wall Face → Select Regions (grid pattern) → Inset Faces → Extrude Inward
→ Delete Inner Faces (creates opening) → Profile Sweep on Edge Loop (frame)
→ Grid Subdivide Opening (panes) → Instance Mullions
```

#### Doors

| Node Group | Description | Technique |
|------------|-------------|-----------|
| `door_cutout.py` | Boolean opening for door | Same as window but floor-aligned |
| `door_frame.py` | Jamb and header trim | Profile sweep on opening edges |
| `door_panel.py` | Door leaf with panel details | Plane + Inset pattern + Extrude panels |
| `door_hardware.py` | Hinges, handle, knocker | Instance placement on door geometry |
| `doorstep.py` | Stone step at threshold | Box primitive aligned to door bottom |
| `porch.py` | Covered entry with posts and roof | Compound: posts + beam + mini roof |

#### Stairs

| Node Group | Description | Technique |
|------------|-------------|-----------|
| `stair_run.py` | Straight staircase between two heights | Instance step mesh at (i×depth, 0, i×height) |
| `stair_stringer.py` | Side support beams | Curve from start to end → Profile extrusion |
| `spiral_stair.py` | Helical staircase | Radial array with Z offset per step |
| `stair_landing.py` | Platform between runs | Box at specified height |
| `stair_nosing.py` | Rounded step edge detail | Bevel or profile on step front edge |

**Stair Calculation:**
```
Step Count = Floor(Height Difference / Step Height)
Adjusted Step Height = Height Difference / Step Count
For i in range(Step Count):
    Instance Step at position (i × Tread Depth, 0, i × Step Height)
```

#### Railings on Edges

| Node Group | Description | Technique |
|------------|-------------|-----------|
| `railing_from_edge.py` | Complete railing along selected edges | Edge Selection → Mesh to Curve → Railing assembly |
| `handrail.py` | Top rail profile sweep | Curve to Mesh with circular/rectangular profile |
| `baluster_array.py` | Vertical spindles along railing | Resample Curve (even spacing) → Instance balusters on points |
| `baluster_shape.py` | Individual baluster geometry | Lathe profile or box with chamfers |
| `newel_post.py` | Larger corner/end posts | Instance at curve endpoints + angle threshold corners |
| `bottom_rail.py` | Lower horizontal rail | Offset curve down → Profile sweep |
| `railing_panel.py` | Solid or decorative infill | Face fill between rails → Optional pattern boolean |

**Railing Pipeline:**
```
Edge Selection → Mesh to Curve → Resample Curve (baluster spacing)
→ Instance Balusters on Points → Offset Curve Up (handrail height)
→ Sweep Handrail Profile → Detect Corners (angle > threshold)
→ Instance Newel Posts at corners and endpoints
```

#### Roofing & Shingles

| Node Group | Description | Technique |
|------------|-------------|-----------|
| `roof_from_footprint.py` | Generates roof shape from floor plan | Straight skeleton algorithm or manual ridge placement |
| `gable_roof.py` | Simple A-frame roof | Extrude edge up to ridge → Fill gable ends |
| `hip_roof.py` | Four-sloped roof | Inset top face → Move up → Merge to ridge |
| `mansard_roof.py` | French-style double slope | Two-stage extrusion with angle break |
| `shingle_scatter.py` | Overlapping roof tiles | Grid on roof face → Offset alternating rows → Instance shingles |
| `shingle_tile.py` | Individual shingle/slate | Curved rectangle with thickness + edge variation |
| `thatch_generator.py` | Organic thatched roof | Curve instances (grass-like) on roof surface |
| `ridge_cap.py` | Ridge line covering | Profile sweep along roof peak edges |
| `gutter.py` | Rain gutter along eaves | U-profile sweep on lower roof edges |
| `fascia_board.py` | Trim board at roof edge | Flat profile along eave edge |

**Shingle Pattern:**
```
Roof Face → UV Project (or Position-based) → Grid Points
→ Offset Every Other Row by Half-Width (brick pattern)
→ Instance Shingle (random Z rotation ±3°, scale variation 0.95-1.05)
→ Align to Face Normal → Offset Along Normal (overlap)
```

#### Trim & Architectural Detail

| Node Group | Description | Technique |
|------------|-------------|-----------|
| `crown_molding.py` | Decorative top-of-wall trim | Profile sweep on horizontal wall-ceiling edges |
| `baseboard.py` | Bottom wall trim | Profile sweep at floor-wall intersection |
| `corner_quoin.py` | Alternating stone blocks at corners | Instance along vertical corner edges (alternating sizes) |
| `decorative_bracket.py` | Support brackets under eaves | Instance at regular intervals along eave |
| `timber_frame_pattern.py` | Half-timbered facade | Boolean subtract beam grid from wall face |
| `brick_pattern.py` | Brick coursing on walls | Offset grid instances with mortar gaps |
| `stone_wall_pattern.py` | Irregular stone masonry | Voronoi cell distribution → Extrude cells |

#### Profile Curves (Shared Resources)

| Profile | Description | Used By |
|---------|-------------|---------|
| `profile_window_frame.py` | Rectangular with chamfer/ogee | Window frames |
| `profile_door_frame.py` | Larger version with threshold detail | Door frames |
| `profile_handrail.py` | Rounded rectangle or circular | Railings |
| `profile_crown_molding.py` | Classic ogee/cove combination | Crown molding |
| `profile_baseboard.py` | Simple chamfered rectangle | Baseboards |
| `profile_gutter.py` | Half-round or K-style | Gutters |

#### Compound Building Generators

These high-level nodes combine the components above:

| Node Group | Description | Components Used |
|------------|-------------|-----------------|
| `colonial_house.py` | Complete colonial-era house | floor_plan, wall_extrusion, window_*, door_*, gable_roof, shingle_scatter, chimney |
| `timber_frame_house.py` | Half-timbered building | wall_extrusion, timber_frame_pattern, window_*, thatched_roof or slate_roof |
| `stone_cottage.py` | Thick stone walls, small windows | stone_wall_pattern, window_* (small), thatch_generator |
| `fishery_building.py` | Coastal work building | Simple walls, large doors, drying rack instances, net draping |
| `warehouse.py` | Storage building | Large footprint, minimal windows, loading dock, large doors |
| `watchtower.py` | Multi-story tower | Stacked circular/square floors, stair_spiral, railing_*, observation platform |

#### Building Generation Pipeline

```
1. Input: Footprint Curve, Building Type, Parameters (stories, style, age)

2. Foundation Layer:
   floor_plan_from_curve → foundation

3. Wall Generation:
   For each story:
     wall_extrusion → timber_frame_pattern (if applicable)
     
4. Opening Placement:
   window_placement (per wall face) → window_cutout → window_frame → window_panes
   door_cutout (ground floor) → door_frame → door_panel

5. Roof:
   roof_from_footprint (or gable/hip) → shingle_scatter → ridge_cap → gutter

6. Vertical Circulation:
   stair_run (interior/exterior) → railing_from_edge

7. Details:
   chimney, crown_molding, baseboard, corner_quoin (if stone)

8. Weathering:
   worn_edges → moss_growth → weathering_composite (based on Age parameter)

9. Output: Complete Building Geometry + Material Attributes
```

---

## Infrastructure & Road Node Groups

### Road Surfaces (Building on existing plan)

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `dirt_road.py` | Compacted dirt with ruts, puddles | Dirt Road Mesh |
| `gravel_road.py` | Gravel surface with stone scatter | Gravel Road Mesh |
| `paved_road.py` | Cobblestone/flagstone paving (see `cobble_stone_roads.md`) | Paved Road Mesh |
| `road_decay.py` | Transition states between road types | Road decay mechanics |
| `road_edge_detail.py` | Grass, stones, drainage at road edges | All road types |

### Railway

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `railway_track.py` | Steel rails on wooden ties | Railway Tracks |
| `railway_bed.py` | Gravel/ballast foundation | Railway Tracks |
| `railway_switch.py` | Track switching mechanism | Railway Tracks |

---

## Vehicle & Transport Node Groups

### Land Vehicles

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `caravan_base.py` | Basic wagon/caravan structure | Caravan Model |
| `caravan_hull_variants.py` | Different caravan hull types | Upgraded Caravan Variants |
| `cart_wheel.py` | Spoked wooden wheel with wear | Caravan Model, Transport Vehicles |
| `wagon_canopy.py` | Canvas/cloth wagon cover | Caravan Model |
| `transport_cart.py` | Material hauling cart | Transport Vehicles |
| `refrigeration_unit.py` | Cold storage equipment | Refrigeration Equipment |

### Rail Vehicles

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `train_locomotive.py` | Steam locomotive engine | Train Locomotive |
| `train_cargo_car.py` | Freight car variants | Train Cars |
| `medical_transport.py` | Specialized medical vehicle | Medical Transport Vehicle |

### Naval Vessels

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `ship_hull.py` | Wooden ship hull with planking | Ship Hull |
| `ship_mast.py` | Mast with yards, platforms | Ship Mast |
| `ship_rigging.py` | Rope network for sails | Ship Rigging |
| `ship_sail.py` | Canvas sails (furled/unfurled) | Ship Rigging |
| `captain_quarters.py` | Interior cabin with furnishings | Captain's Quarters |
| `pirate_ship.py` | Pirate vessel variant with modifications | Pirate Ship |
| `lantern.py` | Hanging ship lantern | Lantern |
| `anchor.py` | Ship anchor with chain | Ship Hull |

---

## Props & Items Node Groups

### Treasure & Currency

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `coin_stack.py` | Gold/silver coin pile with physics consideration | Coin Stack |
| `gold_spire.py` | Mysterious golden spire structures | Gold Spires |
| `mcguffin.py` | The central treasure object | McGuffin Object |
| `treasure_chest.py` | Loot container | Treasury Environment |

### Documents & Books

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `book_journal.py` | Leather-bound books/journals | Book/Journal Model |
| `scroll.py` | Rolled parchment scrolls | Various lore items |
| `newspaper.py` | Folded newspaper prop | Newspaper Layout (for 3D version) |

### Equipment & Tools

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `construction_tools.py` | Pickaxe, shovel, hammer variants | Construction Tools |
| `fishing_equipment.py` | Nets, poles, traps | Fishery Building |
| `lantern_handheld.py` | Portable lantern | Lantern |
| `barrel.py` | Wooden storage barrel | Various storage |
| `crate.py` | Wooden shipping crate | Various storage |
| `rope_coil.py` | Coiled rope | Ship accessories |

### Flags & Banners

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `flag_banner.py` | Cloth flag with faction emblems | Faction Flags/Banners |
| `flag_pole.py` | Flag mounting pole | Faction Flags/Banners |

### Artifacts & Ruins

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `decayed_artifact.py` | Rusted/rotten previous-run objects | Decayed Artifacts |
| `cliff_runes.py` | Carved rune patterns on rock | Cliff Runes (3D relief version) |
| `ancient_marker.py` | Mysterious stone markers | Inner layer exploration |

---

## Character & Clothing Node Groups

### Base Characters

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `crew_member_base.py` | Expedition member base mesh | Expedition Crew Member |
| `construction_worker.py` | Road/building worker model | Construction Workers |
| `cart_driver.py` | Caravan driver character | Cart Drivers |
| `police_guard.py` | Authority/inspection officer | Police/Guard Characters |
| `patrol_unit.py` | Road patrol character | Patrol Units |

### Clothing Systems

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `period_outfit_base.py` | Modular clothing framework | Historical Period Outfits |
| `winter_clothing.py` | Cold weather gear (furs, wool) | Historical Period Outfits |
| `colonial_uniform.py` | Faction-specific uniforms | Faction-related |
| `worker_clothing.py` | Practical labor clothing | Construction Workers, Cart Drivers |

---

## VFX & Atmospheric Node Groups

### Particle Systems (as geometry nodes)

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `gold_particle_trail.py` | Gold coins floating effect | Gold Floating Animation, Gold Collection Animation |
| `transmutation_effect.py` | Alchemical transformation particles | Transmutation VFX |
| `fog_volume.py` | Time fog particle system | Time Fog Particle Effect |
| `dust_debris.py` | Construction dust/debris | Construction Effects |
| `decay_particles.py` | Crumbling/rotting particle effect | Decay Visual Effects |

### Environmental Effects

| Node Group | Description | Source Assets |
|------------|-------------|---------------|
| `madness_distortion.py` | Visual distortion for madness effects | Progressive Madness Effects |
| `societal_breakdown.py` | Environmental degradation effect | Societal Breakdown Effects |

---

## Missing Assets Analysis

The following assets are NOT listed in `game_assets.csv` but are implied or required by the design document:

### Critical Missing 3D Models

| Asset | Reason Needed | Design Doc Reference |
|-------|---------------|----------------------|
| **Elevator/Lift System** | Transport between well layers | "elevator points being at the edges of the circle" |
| **Mining Equipment** | Resource extraction mentioned | "miners" mentioned in Shackleton-style ad |
| **Farming Equipment** | Agriculture implied | "farmers" mentioned in Shackleton-style ad |
| **Docks/Harbor** | Ships need landing infrastructure | Expeditions arrive by sea |
| **Lighthouse/Beacon** | Navigation for ships | Island approach mechanics |
| **Cemetery/Graves** | Previous expedition remains | "men go mad and start to kill and eat each other" |
| **Prison/Stocks** | Prisoners mentioned as crew source | "prisoners provided to a company to earn their freedom" |
| **Gambling House** | Gamblers as crew source | "gamblers running from debt collectors" |
| **Pub/Tavern** | Social hub, drunk crew mentioned | "drunken men singing in ship hull" |
| **Church/Chapel** | Colonial settlements typically had | Period appropriateness |
| **Windmill** | Power/grain processing | Period infrastructure |
| **Blacksmith/Forge** | Tool/equipment maintenance | Equipment production |
| **Marketplace/Trading Post** | Trade mechanics central to game | Core gameplay loop |
| **Defensive Fortifications** | Demon attacks on villages | "demons walk out of sea and attack villages" |
| **Watchtower/Lookout** | Defense and observation | Security infrastructure |
| **Bridge** | River/ravine crossing | Road network connectivity |
| **Tunnel** | Mountain passage | Road through elevation |
| **Well/Water Source** | Survival necessity | Settlement infrastructure |
| **Storage Silos** | Grain/feed storage | "fresh horses" need feed |

### Critical Missing Environment Assets

| Asset | Reason Needed | Design Doc Reference |
|-------|---------------|----------------------|
| **Village/Settlement Layout** | Procedural village generator | "coastal villages that demons attack" |
| **Trade Route Markers** | Route visualization | Core gameplay visualization |
| **Border/Boundary Markers** | Faction territory display | "different colonial companies" |
| **Camp/Expedition Base** | Temporary settlements | Expedition mechanics |
| **Ruin/Abandoned Settlement** | Previous failed expeditions | "structures and artifacts rusted and decayed" |
| **Cave System** | Island interior exploration | Deep island content |
| **Hot Spring/Geothermal** | Volcanic island features | "volcanic" nature of island |
| **Frozen Areas** | Iceland-like climate | "outer layer should be like iceland" |

### Missing Creature/Flora Assets

| Asset | Reason Needed | Design Doc Reference |
|-------|---------------|----------------------|
| **Seal/Sea Lion** | Coastal wildlife | Iceland-like ecosystem |
| **Whale** | Ocean wildlife | North Atlantic setting |
| **Arctic Fox** | Tundra wildlife | Iceland wildlife reference |
| **Berries/Edible Plants** | Survival foraging | Survival mechanics |
| **Medicinal Herbs** | Treatment mechanics | "transport them to a town where treatment is known" |
| **Mushrooms** | Foraging/alchemy | Alchemical theme |
| **Volcanic Flowers** | Unique island flora | Volcanic biome distinction |

### Missing Infrastructure Assets

| Asset | Reason Needed | Design Doc Reference |
|-------|---------------|----------------------|
| **Road Construction Site** | Building roads is core mechanic | "clearing trees and brush in front of the road head" |
| **Surveyor Equipment** | Route planning | Road efficiency calculation |
| **Milestone/Distance Marker** | Route distance tracking | "distance a horse can travel" |
| **Rest Stop/Waystation** | Between horse stations | Extended travel mechanics |
| **Smuggler's Cache** | Hidden storage for contraband | Smuggling mechanics |
| **Customs House** | Inspection point | "costly inspections of caravans" |
| **Bank/Exchange** | Financial transactions | Stock market, shares trading |
| **Insurance Office** | Risk management | Colonial company structure |
| **Colonial Office/Governor** | Administrative center | Faction HQ |

### Missing Ship/Naval Assets

| Asset | Reason Needed | Design Doc Reference |
|-------|---------------|----------------------|
| **Rowboat/Dinghy** | Ship-to-shore transport | Landing parties |
| **Fishing Boat** | Fishery operations | Fishery Building needs boats |
| **Cargo Ship** | Trade vessel | Goods transport |
| **Naval Cannon** | Ship defense | Pirate/privateer combat |
| **Figurehead** | Ship decoration | Period authenticity |
| **Ship's Bell** | Timekeeping/signals | Period authenticity |
| **Crow's Nest** | Ship observation | Navigation/spotting |

---

## Implementation Priority

### Phase 1: Core Infrastructure (Foundation)
Priority: **Critical** — Needed for basic world generation

1. `volcanic_island_terrain.py` — Main world structure
2. `basalt_columns.py` — Volcanic rock formations
3. `iceland_outer_layer.py` — Starting biome
4. `dirt_road.py` → `gravel_road.py` → `paved_road.py` — Road progression
5. `timber_frame_building.py` — Basic structures
6. `coastal_terrain.py` — Shore areas

### Phase 2: Natural Environment
Priority: **High** — Visual richness and biome distinction

1. `sparse_tree.py`, `deadwood.py` — Vegetation
2. `rock_scatter.py` — Terrain detail
3. `ocean_surface.py` — Water
4. `time_fog_volume.py` — Atmospheric boundary
5. `snow_accumulation.py` — Weather effects
6. `iceberg.py` — Ocean features (existing plan)

### Phase 3: Fauna & Characters
Priority: **High** — Gameplay entities

1. `sheep.py`, `reindeer.py`, `fish.py` — Resources
2. `horse.py` — Transport
3. `crew_member_base.py` — Player units
4. `alchemical_demon_base.py` — Antagonists
5. `rat.py`, `bird.py` — Ambient life

### Phase 4: Vehicles & Transport
Priority: **High** — Core gameplay

1. `caravan_base.py` — Primary transport
2. `cart_wheel.py` — Shared component
3. `ship_hull.py`, `ship_mast.py`, `ship_rigging.py` — Naval
4. `train_locomotive.py`, `train_cargo_car.py` — Late game

### Phase 5: Buildings & Infrastructure
Priority: **Medium** — Settlement content

**Building Component Order (dependencies flow downward):**
1. `floor_plan_from_curve.py`, `wall_extrusion.py` — Core structure
2. `window_cutout.py`, `door_cutout.py` — Openings
3. `window_frame.py`, `door_frame.py`, `window_panes.py` — Frames
4. `gable_roof.py`, `hip_roof.py` — Roof shapes
5. `shingle_scatter.py`, `shingle_tile.py` — Roof covering
6. `railing_from_edge.py`, `handrail.py`, `baluster_array.py` — Railings
7. `stair_run.py`, `stair_stringer.py` — Stairs
8. `crown_molding.py`, `baseboard.py`, `window_sill.py` — Trim details
9. Profile curves (shared by multiple components)

**Compound Buildings:**
1. `timber_frame_building.py` — Basic colonial structure
2. `fishery_building.py` — Economy
3. `warehouse.py` — Storage
4. `horse_station.py` — Transport network
5. `toll_booth.py` — Road economy
6. `headquarters.py` — Player base
7. Village generator compound nodes

### Phase 6: Props & Detail
Priority: **Medium** — Polish and immersion

1. `worn_edges.py` — Weathering (existing plan)
2. `coin_stack.py` — UI/treasury
3. `book_journal.py` — Lore items
4. `decayed_artifact.py` — Discovery content
5. `flag_banner.py` — Faction identity

### Phase 7: VFX & Atmosphere
Priority: **Lower** — Visual polish

1. `gold_particle_trail.py` — UI feedback
2. `transmutation_effect.py` — Demon attacks
3. `madness_distortion.py` — Late-game effects

---

## Technical Notes

### Node Group Patterns

Following the existing codebase patterns:

```python
@geo_node_group
def create_asset_name_group():
    group_name = "AssetName"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    # Define interface sockets
    # Build node network using node_helpers
    # auto_layout_nodes(group)
    return group
```

### Shared Parameters

Many assets should share common input parameters:
- `Seed` (Int) — Randomization control
- `Age` (Float 0-1) — Weathering/decay level
- `Scale` (Float) — Overall size multiplier
- `Detail Level` (Int) — LOD control for performance

### Material Integration

Geometry nodes should output named attributes for material assignment:
- `wear_factor` — Edge wear intensity
- `rust_factor` — Corrosion amount
- `moss_factor` — Organic growth
- `snow_factor` — Snow coverage
- `faction_id` — For faction-specific coloring

---

## Related Documents

- [Cobblestone Roads Plan](./cobble_stone_roads.md) — Detailed road paving implementation
- [Iceberg Plan](./iceberg.md) — Ice formation implementation
- [node_helpers.py](../geo_node_groups/node_helpers.py) — Utility functions for node creation
