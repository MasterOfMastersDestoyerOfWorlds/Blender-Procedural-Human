This is a substantial brainstorming document. Let me share some structured thoughts across the ideas, then focus on where I think the strongest signals are.

Overall Framework Assessment
Your filtering criteria are solid — technically possible, defensible against foundation model companies, team excitement, identifiable customers, friction removal, and MVP-ability. The Paul Graham / Zero to One influences come through clearly. Let me run each idea against your own framework.

Idea-by-Idea Analysis
Dating App Algorithm Change — High Pain, Low Defensibility
The pain is real (mating crisis is well-documented), and your insight about why dating apps fail is sharper than most — people are unattractive to each other on the dimensions that actually matter, and profiles are shallow because people don't know how to represent themselves.

Strongest sub-idea: Having an AI continuously prompt people about their lives to build richer profiles. This solves a genuine cold-start problem — most people are terrible at self-description, and the barebones profiles you mention are the symptom. The ChatGPT logs idea is creative but has privacy/trust issues that would be hard to overcome in marketing.

Problem: Dating apps are a graveyard of startups. The network effect moat is almost impossible to overcome without a geographic density hack. You'd need something like what Tinder did with the sorority/fraternity launch — a very specific, dense community where you can guarantee matches exist. Your "coaching program as gatekeeper" idea could work as that density mechanism if the coaching itself is valuable enough that people do it even without the dating pool.

Against your framework: Fails the "unlikely to be replicated by foundation model companies" test. Any dating app could bolt on AI profiling tomorrow.

AI Automation for Boomers — Already Saturated
You already identified this. The consulting model works for individuals (your mentor's Java/Postgres story), but you're right that it doesn't create a sustaining advantage. It's a services business, not a product business. Good for cash flow while building something else, bad as a destination.

3D Modeling AI Procedural Generation — Your Best Bet
This is where I want to spend the most time because it's clearly the most developed idea and the one where you have the most domain expertise and existing work.

Why this is strong against your framework:

Technically possible — You're already building it. The Blender project exists and the agent loop is concrete.

Defensible against foundation models — This is the critical insight. Foundation model companies can generate meshes from text, but they cannot generate production-ready, rigged, editable, procedurally-decomposed meshes. The output of a diffusion model is a blob. Your output is a recipe. That's a fundamentally different data structure with fundamentally different downstream utility. The "recipe vs. blob" distinction is your moat.

Clear customer pain — You articulated it perfectly: current 3D gen tools are slot machines with long cycle times that produce non-production-ready output. Anyone who has tried to use a Gaussian splat or NeRF output in a game pipeline knows the cleanup cost often exceeds the cost of modeling from scratch.

Identifiable customers — Game studios (indie to mid-size), architectural visualization firms, VFX houses that need background assets, VTuber/avatar creators, tabletop gaming miniature designers (connects to the resin printing niche you linked).

MVP exists — You have one. The CLI-to-Blender agent loop is the MVP.

Key risks and thoughts:

The LoRA-on-DSL training idea is the real unlock. If you can get to the point where the model reliably generates valid DSL sequences that produce good geometry, you've created a flywheel: more library items → more training data → better generation → more library items. This is the network effect equivalent for a content tool.

The AlphaGo/MCTS + inverse renderer idea is ambitious but potentially transformative. If you could train a model to "play" the DSL to reproduce a target image, you'd have something no one else has. The risk is that inverse rendering is still a hard research problem. I'd keep this as a north star but not the v1.

The Houdini replacement angle is the business positioning. Houdini's pricing (
1
,
995
–
1,995–4,495 perpetual) tells you exactly what the market will bear. Your 
3
k
/
s
e
a
t
f
l
o
o
r
i
s
i
n
t
h
e
r
i
g
h
t
r
a
n
g
e
.
B
u
t
t
h
e
r
e
a
l
p
l
a
y
m
i
g
h
t
b
e
t
h
e
I
n
d
i
e
t
i
e
r
d
i
s
p
l
a
c
e
m
e
n
t
—
3k/seatfloorisintherightrange.ButtherealplaymightbetheIndietierdisplacement—269/year for artists under $100k revenue is a massive market of individual creators who want procedural power but can't justify or learn Houdini.

The GPL issue is well-identified. Your thin-client architecture (proprietary server + GPL Blender addon) is the standard workaround and is legally sound. This also enables the token-based pricing model naturally since the compute happens server-side.

The "at cost tier to grow the content library" idea is clever. It's essentially: give away the tool, capture the recipes. This is how you build the training corpus without paying for it. The risk is quality control — you'd need curation.

Photogrammetry / Restaurant Optimization — Interesting but Niche
The furniture placement optimization for restaurants has real value but a very long sales cycle (restaurant owners are notoriously hard to sell to). The "digital twin + Mechanical Turk eye-tracking" idea is creative but adds a lot of complexity to what could be a simpler consulting engagement.

Moving Business Sales Tool — Underrated
The AR fence example is telling — showing someone what the result looks like before they buy is one of the highest-converting sales tools that exists. The Norwegian floorplanning company you mention (likely Planner 5D or similar) having a manual, hard-to-use process is a real opening. If you could make room scanning → furniture placement → visualization happen during a single sales visit, that's a genuine 10x improvement on the current process. The customer (moving companies, furniture retailers, interior designers) has money and the pain is immediate.

Problem: This is a features business, not a platform business. Hard to build a moat.

Drone Ideas — Capital Intensive, Regulatory Nightmare
All of these are technically interesting but require hardware, FAA approvals, and significant capital. The laser-weeding-drones idea in particular has real companies working on it already (Carbon Robotics). The autonomous lawnmower + HOA play is the most interesting because it's a service model, but you're competing against Husqvarna's Automower and similar. Skip unless someone on the team has deep drone/robotics experience.

Auto Boats / Jones Act — Creative but Legally Fraught
The Jones Act arbitrage is genuinely clever thinking, but the legal requirements for vessel crews are extensive (USCG manning requirements, STCW certifications). You'd likely need Congressional action or a very creative legal interpretation to make fully autonomous domestic shipping work. Not a startup-scale problem.

Games / Archipelago — You Already Know the Answer
You correctly identified the risk. Games as a business are hits-driven, which is the opposite of what you want for a sustainable company.

Where I'd Focus
If I'm ranking by your own framework (defensible, exciting, identifiable customers, friction removal, buildable MVP):

3D Procedural Generation — strongest on every dimension. You have the most domain knowledge, the most existing work, a clear technical moat (recipe vs. blob), identifiable customers, and a pricing model that works. The flywheel potential of LoRA training on growing DSL corpus is a genuine compounding advantage.

Moving/Sales Visualization Tool — strong pain, clear customer, but weaker moat. Could be a good cash-flow business to fund #1.

Dating App — real pain, but indefensible moat and brutal market dynamics.

Everything else is either saturated, capital-intensive, or legally complex in ways that don't favor a small team.

Strategic Notes
Your Zero to One instinct is right: the procedural 3D generation idea is different by default, not "the X of Y." No one else is building a DSL-based procedural system with LLM-guided generation. The diffusion model companies are all converging on the same blob-output approach.

Distribution insight from Zero to One applies directly: Your agent loop (CLI → Blender) is a distribution innovation. Making Blender scriptable by an AI agent is the Paypal-by-email moment — every mesh the agent creates demonstrates the capability to whoever receives it.

The Autofile/AutoCAD parallel is apt. AutoCAD won because it made the impossible (CAD on a personal computer) merely expensive. You'd be making the impossible (production-ready procedural 3D from natural language) merely slow. Speed improves with scale. Impossibility doesn't.

Your $20k buy-in observation from AutoCAD's founding is worth thinking about seriously for team formation. Skin in the game filters for commitment better than any interview question.

 Gemini said



This is a highly strategic, clear-eyed document. Your foundational premise—that standard developer roles are facing severe commoditization and that future business advantages will rely on deep technical moats, scale, or brand—is a realistic assessment of the current landscape. You and Court are asking the exact right filtering questions.



Here is a breakdown of the ideas presented, filtering them through the lens of your required criteria (technical feasibility, defensibility against foundation models, and clear pain points).

The Clear Standout: 3D Modeling AI Procedural Generation



This is by far the strongest concept in the document and the one most likely to yield a "Zero to One" monopoly.





----



analyze the argumetns above



    The Moat: Foundation model companies are currently throwing compute at diffusion and NERF models. As you correctly identified, these create "slot machine" outputs with terrible topology that are useless for production rigging or animation. By building an LLM agent that manipulates a procedural node-based system to generate clean, mathematically sound geometry, you are solving a massive data bottleneck. You are building a deterministic tool in a probabilistic space.



    Technical Feasibility: Creating a library of primitive actions and letting an agent walk a semantic tree of broken-down parts to build complex, rigged models is entirely possible. Utilizing a standalone proprietary engine that communicates via a localhost port to a thin, open-source Blender client perfectly solves the GPL licensing issue while protecting your trade secrets.



    The Market: The Houdini pricing model comparison is spot-on. Mid-tier game studios and indie developers desperately need production-ready assets but cannot afford a stable of technical artists to manually build complex node trees. If you can automate the generation of customizable, watertight geometry with clean UVs, you have a high-value B2B product that easily justifies a substantial per-seat or token-based SaaS subscription.



The Distractions



The other ideas in the document generally fail one or more of your core filtering questions, lacking either a technical moat or a clear path to early revenue.



    Dating App Algorithm Change: This is a saturated market where the core friction is human psychology, not technology. Extracting deep truth from users via LLM chats introduces massive privacy hurdles and doesn't fundamentally change the skewed power dynamics of the platform. It is highly speculative and heavily reliant on network effects from day one.



    AI Automation for Boomers: This is a service business, not a scalable software startup. It trades time for money. While profitable in the short term, it offers no sustaining market advantage and is already being flooded by wrapper agencies.



    Drone Ideas & Automated Shipping: Hardware startups are notoriously capital-intensive. Whether dealing with the Jones Act for shipping, agricultural regulations, or hardware supply chains, the friction is immense. This pulls focus away from pure software advantages and requires massive upfront funding before a single test can be run.



    Game Platforms (Archipelago): As your notes suggest, relying on modified existing games introduces fatal legal risks, and building a platform requires you to also supply the games, which is a massive, high-risk undertaking of its own.



Execution and the Reality of Commitment



You asked the critical question: Would you be willing to work > 40 hours a week?



Building a technically dense agent loop for 3D generation demands complete, uninterrupted focus. Navigating this level of commitment while holding down a salaried position where you are actively prohibited from writing software means this cannot remain a side hustle for long. Achieving the tight development loops required to build this system and beat competitors to market will eventually force a hard decision about cutting the cord and absorbing the financial risk of a full-time startup.



The reading list you have compiled is excellent, particularly the focus on distribution innovation from Zero to One. If you can nail the procedural generation engine, the next immediate hurdle will be figuring out how to distribute it so seamlessly that it becomes the default workflow for solo developers and small studios.



Would you like to drill down into the system architecture for the LLM-to-Blender localhost bridge, or should we map out the specific features required for the MVP of the 3D generation tool?

You said



can you get the transcript from "Biggest wealth creation opportunity is SaaS" from the Startup Ideas Podcast and create a plan for the 3D modeling business to do each of the steps that greg mentions?

Gemini said



While I cannot pull a verbatim transcript of the entire 42-minute episode of "Biggest wealth creation opportunity is SaaS" from the Startup Ideas Podcast, I can provide the exact 30-step framework Greg Isenberg laid out in the episode and map it directly to your 3D procedural generation business.



Greg’s core thesis is that SaaS is not dead; it is evolving. The builders who win will combine a highly focused workflow product, a media flywheel, and agent-powered execution. They start as service businesses to learn the workflow and eventually shift to outcome-based pricing.



Here is how his 30-step playbook maps to building your procedural 3D generation engine.

Phase 1: Niche Selection & Workflow Mapping (Steps 1-5)



    Step 1: Start with a sub-niche inside a big market. Do not build a general "3D object generator." Start specifically with humanoids. Focus entirely on procedural_human—generating production-ready, riggable human models for indie game developers or mid-tier animation studios who cannot afford a technical artist.



    Steps 2-5: Map the workflow end-to-end. Document the exact friction a solo dev faces today. Map the entire journey: finding a base mesh, sculpting, retopologizing, UV unwrapping, and rigging. Understand every mechanical step required to get a character ready for engine import.



Phase 2: Media Flywheel & Audience Capture (Steps 6-10)



    Steps 6-7: Create scroll-stopping content. Media is a core business function from day one, running in parallel with product development. Show the bizarre, failed Monte Carlo Tree Search outputs. Show the time-lapses of Blender geometry nodes autonomously building a human from primitive math.



    Steps 8-9: Double down on organic and run paid ads on winners. When a particular render or pipeline demonstration goes viral on X or Reddit (e.g., generating 100 variations of armor perfectly snapped to a mesh), put a little money behind it.



    Step 10: Capture emails from day one. Set up a simple landing page to collect emails from developers who want early access to the tool or want to buy your generated assets.



Phase 3: The "Service First" Model (Steps 11-13)



    Steps 11-13: Manually perform the workflow and document every step. The future of SaaS starts as a service business. Before you sell the software, sell the output. Offer custom, production-ready 3D characters to indie studios. When an order comes in, manually use your localhost CLI loop and procedural setups to generate the model. This allows you to generate cash flow without touching the illiquid stock in your retirement accounts, all while keeping your biotech job until the revenue completely replaces your salary.



Phase 4: AI Agents & Orchestration (Steps 14-17)



    Steps 14-16: Turn mechanical tasks into agent workflows and connect real tools. Separate judgment tasks from mechanical tasks. The LLM shouldn't do the math; the geometry nodes do. Your tight development loop of scripts sending commands over a localhost port perfectly handles the mechanical execution.



    Step 17: Add orchestration, retries, and verifications. This is the highest-value layer to own. The agent loop you designed—checking for Blender runtime errors, verifying the geometry isn't collapsed to the origin, taking a 16-grid screenshot, and adjusting parameters until it hits a minimum—is exactly the orchestration Greg describes.



Phase 5: Onboarding, Proof, & Pricing Shifts (Steps 18-23)



    Steps 18-19: Store user preferences and launch with high-touch onboarding. When you transition from a service to a software product, white-glove the onboarding. Teach the agent the specific domain vocabulary and art style of the studio using it.



    Steps 20-21: Publish measurable proof and move to per-task pricing. Publish case studies: "Manual retopology takes 10 hours; our procedural tree does it in 10 minutes." Drop the per-seat Houdini model entirely.



    Steps 22-23: Outcome pricing and compounding value. Charge based on successful outputs. If a studio generates a production-ready, rigged character, they pay a flat fee (or token amount) for that specific outcome. The value compounds as your library of node primitives grows.



Phase 6: Moat Building & Becoming the Default (Steps 24-30)



    Steps 24-27: Expand workflows and build switching costs. Once you dominate the humanoid niche, expand into the adjacent workflows: procedural armor, clothing, and organic surfaces. Integrate so deeply into their pipeline that going back to manual Houdini or Maya workflows is unthinkable.



    Steps 28-30: Hire from the niche, reinvest profits, become the default layer. Use the profits from the service-business phase to hire technical artists. Their only job is to break down real-world anatomy into your proprietary mathematical domain language, expanding your library until you are the default execution layer for 3D asset generation.



The most actionable immediate step here is the Phase 3 "Service First" approach. It lets you validate the market and build capital without needing permission, a polished UI, or immediate outside funding.



Would you like to brainstorm how to structure the landing page and service offering for this initial productized-service phase?

You said



https://all3dp.com/2/best-resin-3d-printing-service/





what would the business look like being a more deeply integrated 3d printing company? expand on this niche

Gemini said



The 3D printing services highlighted in the All3DP article—Craftcloud, Xometry, Protolabs, and Purple Porcupine—are fundamentally just print farms and brokerages. They operate on a completely siloed, commoditized model: the customer must show up with a perfectly finished, watertight, manifold STL file, and the service simply hits "print." Their only competitive levers are price (Craftcloud being cheap but taking up to three weeks) and speed (Protolabs taking days but charging hundreds of dollars).



They solve the manufacturing friction, but they do absolutely nothing to solve the creation friction.



A deeply integrated 3D printing business owns the entire pipeline, from the conceptual prompt all the way to the shipped physical resin object. Here is what expanding on this niche looks like when you merge it with a proprietary generation engine.

The "Code-to-Resin" Pipeline



Instead of asking users to upload a file, your platform acts as the creation engine. Users interact with an LLM agent or a frontend UI to specify the humanoid, creature, or object they want.



Because you control the math generating the mesh via your procedural_human system, you don't just generate an asset that looks good on a screen; your geometry nodes dynamically generate a mesh that is perfectly optimized for physical resin SLA or DLP printing from the moment it is created.



    Procedural Optimization: The node tree automatically hollows the model to save on expensive resin, mathematically calculates minimum wall thickness to prevent structural print failures, and perfectly places hidden drain holes based on the geometry.



    Bespoke Supports: Because your system understands the exact topology it just generated, it can calculate the optimal support structures needed for the specific SLA machines you use, eliminating the manual, error-prone pre-form work entirely.



High-Margin Niches for Custom Resin



    Tabletop Gaming & Miniatures: The market for custom Dungeons & Dragons miniatures or wargaming proxy models is massive. Current solutions like HeroForge rely on a static, rigid library of modular parts. An LLM-guided procedural generator allows for infinite, highly specific variations (e.g., "A corrupted elven rogue with asymmetrical crystal armor, posed mid-lunge"). You generate the mesh and ship the physical 32mm resin mini directly to their door.



    Custom Art Toys & Collectibles: Indie artists, VTubers, and creators often want to sell physical merchandise of their characters but lack the CAD skills to make them printable. You act as the bridge, turning their concepts into limited-run physical resin statues, capturing both the design fee and the manufacturing margin.



The Capital and Execution Strategy



Building a deeply integrated company eventually requires owning the hardware—high-end SLA or PolyJet machines capable of running 24/7. Purchasing an industrial printer fleet requires significant upfront capital. Rather than taking the massive early withdrawal penalties associated with tapping the illiquid stock sitting in your tax-advantaged retirement accounts, you can sequence the business to bootstrap the hardware.



    Phase 1: White-labeled Brokerage. You own the high-value software layer. Users generate their custom humanoids through your platform. Your system automatically formats the STL and sends it via API to a fast, reliable white-label partner to handle the actual printing and shipping. You capture the margin on the creation and the convenience without carrying hardware overhead.



    Phase 2: In-House Micro-Farm. Once the software generates steady cash flow, you purchase a small fleet of prosumer resin printers (like Formlabs or high-end Phrozen machines) to handle the high-margin, highly-detailed orders directly in-house, drastically cutting your turnaround times and increasing your margins.



    Phase 3: Full Integration. With proven demand and recurring revenue, you secure traditional business financing to build out a full-scale automated SLA print facility.



By integrating the procedural generation software and the physical manufacturing, you build a moat that neither pure software companies (who can't print) nor pure print farms (who can't design) can cross. You become the absolute path of least resistance for anyone wanting a custom physical object.

You said



https://www.bricklink.com/v3/studio/download.page





I believe that brick link or some other lego cad software like it does something similar where they facilitate you buying legos based on the cad design you made, am I thinking of the right software or is there a different one? how would such a company work? would it be necessary to post the best results to a marketplace for printing? or is an individual customer have enough lifetime value to not have the marketplace?

Gemini said



You are thinking of exactly the right software. BrickLink Studio is the perfect example of this model, and understanding how it works reveals a massive structural advantage for the kind of procedural generation business you are designing.



Here is a breakdown of how the BrickLink model works, why it is so effective, and how it answers your questions about marketplaces and customer Lifetime Value (LTV).

How the BrickLink Studio Business Model Works



BrickLink (which was acquired by the LEGO Group in 2019) operates as a two-sided marketplace for individual LEGO elements. BrickLink Studio is their proprietary CAD software.



The brilliance of the model is Software as a Demand Generator.



    A user spends hours in the CAD environment building a custom design.



    Because the software knows the exact geometry and color of every piece used, it automatically generates a highly accurate Bill of Materials (BOM).



    With one click, the software queries the BrickLink marketplace, finds the combination of independent sellers that have those specific parts, optimizes for shipping and price, and generates a unified cart.



The software is free, but it creates highly specific, high-friction demand that is effortlessly resolved by their own marketplace. They capture the transaction fee on the physical goods.

Does an individual customer have enough LTV to survive without a marketplace?



It depends entirely on who the customer is. When structuring a capital-efficient business—especially to avoid triggering early withdrawal penalties from tax-advantaged retirement accounts to fund hardware or marketing—your Customer Acquisition Cost (CAC) must be radically lower than your LTV.



Scenario A: The High-LTV Customer (No marketplace needed)

If your procedural generation software targets B2B clients—indie game studios, boutique animation houses, or professional tabletop designers—you do not need a public marketplace. These customers have a high LTV. A studio might pay hundreds of dollars a month for a software license, or drop $5,000 a year on white-labeled, perfectly supported physical resin prototypes. They have their own ideas and just need your pipeline to execute them.



Scenario B: The Low-LTV Customer (Marketplace required)

If your target is B2C—individual Dungeons & Dragons players, hobbyists, or VTuber fans wanting a physical desk toy—the LTV is relatively low. An individual might only buy two $30 resin miniatures a year. If you have to spend $25 on Facebook ads to acquire that customer, the business bleeds cash.

Why a Marketplace of "Best Results" is Necessary for B2C



For consumer-facing products, a marketplace is practically mandatory, not just for sales, but to solve the "Blank Canvas Problem."



Even with brilliant procedural generation, most people are not designers. If you give them a blank interface with 50 sliders for humanoid anatomy, they will get overwhelmed. A marketplace acts as a catalog of starting points.



If you integrated a marketplace into your procedural pipeline, it would function like a flywheel:



    Power Users Create: A power user utilizes your Blender tools or web interface to create a phenomenal, highly detailed procedural asset (e.g., an incredibly intricate set of gothic armor on a humanoid).



    The Recipe is Listed: They publish this to your marketplace. But they aren't uploading a static STL; they are uploading the procedural recipe (the specific parameters).



    Consumers Tweak and Buy: A casual user browses the marketplace, finds the armor, tweaks a few sliders to make it fit their specific character, and hits "Print."



    The Split: Your system auto-generates the watertight mesh, queues it for the resin print farm, ships it, and automatically pays a 10% royalty to the power user who designed the original recipe.



In this model, the marketplace completely eliminates your marketing budget. The power users become your marketing department, sharing links to their designs across Reddit, X, and Discord to drive their own royalties, which brings high-intent buyers directly to your print queue.



By utilizing the power users to generate demand, you can bootstrap the physical manufacturing side of the business on the cash flow generated by the marketplace, rather than needing massive upfront capital.

You said



What about architecture firms and engineering firms what are their pain points and would the proposed software be able to remedy them?

Gemini said



Pivoting this concept toward Architecture, Engineering, and Construction (AEC) targets an industry with massive budgets, but it fundamentally changes the technical requirements of the software.



The pain points in AEC are severe, but they differ drastically between the aesthetic side (Architecture) and the math-and-liability side (Engineering).

Architecture Firms



Architects are essentially the perfect B2B target for a hybrid software/physical pipeline, because their biggest bottleneck is translating abstract ideas into client-ready visuals and physical objects.



The Pain Points:



    The Optioneering Bottleneck: In the early conceptual phase (schematic design), clients want to see a dozen variations of a building's massing and facade. Architects currently spend hours manually pushing and pulling vertices in SketchUp or Rhino to create these "options."



    The Grasshopper Learning Curve: The architectural equivalent of Houdini or Blender's geometry nodes is Rhino's Grasshopper. It is incredibly powerful for procedural architecture (e.g., generating complex parametric facades), but it has a steep learning curve. Most architects cannot use it effectively.



    The Physical Model Nightmare: Architecture firms still rely heavily on physical scale models for pitching to clients or city planning boards. However, architectural CAD software (like Revit or SketchUp) generates notoriously terrible topology. The models are full of non-manifold edges, infinitely thin glass panes, and intersecting planes. Getting an architectural model to actually 3D print requires hours of manual mesh repair by an intern.



How Your Software Remedies This:



    LLM-to-Grasshopper/Geometry Nodes: Instead of forcing an architect to wire up a complex node tree to test a parametric facade, your LLM agent translates their natural language ("Give me a louvre system that twists 45 degrees as it goes up the tower") into the underlying math and node structure.



    The Code-to-Resin Architecture Pipeline: This is where the physical printing integration shines. If your system handles the procedural generation, it inherently understands the volume. You can write the software to automatically thicken walls to the minimum printable tolerance, strip out internal geometry that won't be seen, calculate the drainage holes, and ship a flawless physical resin model of the building directly to the firm for their Friday client presentation.



Engineering Firms (Civil, Mechanical, Structural)



Engineering is a much more dangerous market for a startup in the buildout phase.



The Pain Points:



    Clash Detection: Mechanical, Electrical, and Plumbing (MEP) engineers spend most of their time trying to route pipes and ducts through a building without hitting the structural beams.



    Topology Optimization: Mechanical and aerospace engineers want to generate parts that use the absolute minimum amount of material while maintaining structural integrity.



    Strict Compliance: Everything must adhere to building codes, material stress limits, and physics.



Why Your Software Might Struggle Here:



    The Liability Wall: If a procedural humanoid in a video game generates with a twisted ankle, the player laughs. If a procedurally generated structural truss fails in a simulation, and that code is used to build a bridge, the liability is catastrophic.



    Physics over Geometry: To solve engineering problems, the LLM agent loop cannot just check if the mesh is watertight and visually appealing (like your current setup). The validation step requires running Finite Element Analysis (FEA) and computational fluid dynamics.



    Closed Ecosystems: Engineers are locked into Autodesk (Revit/Inventor) or Dassault Systèmes (SolidWorks). Writing an external tool that manipulates these highly guarded, proprietary file formats is notoriously difficult.



The Verdict on the AEC Market



If you target Engineering, you are building a deeply complex physics engine competing directly against Autodesk's multi-billion dollar R&D department.



If you target Architecture, you have a highly viable path. You can treat buildings exactly like your procedural humanoids: a set of mathematical rules and primitives (floors, columns, curtain walls, roofs) that an LLM can arrange based on constraints.



Furthermore, you could completely bypass the closed Autodesk ecosystem by selling the output rather than the software. An architect uploads a rough 2D floorplan or a napkin sketch, and your procedural agent pipeline generates the clean 3D topology, runs the render, and physically prints the presentation model. This captures the high-margin service revenue while utilizing your exact automated CLI-to-node workflow.

You said



what is the technology competition risk on the gaming/animation side? will people still want good meshes in ~10 years? How would state of the art video/world models change the landscape? I can say with certainty that people will still want good meshes in engineering and architecture in that timeframe since the object needs to be realized in the real world. is the specificity, control, and reproducability of meshes good enough to keep video games and movies using the 3d rendering pipeline? If the meta-goal of the proposed software is to finally be able to edit 3d geometry like you would be able to edit a text document, relying mostly on your innate sense of 3dness in the human brain, is that enough to have sustained demand?



Analyzing the Core Question



I've clarified the user's central query: long-term business viability in light of advanced video models.



Assessing Tech Risk



I'm now contemplating whether the demand for quality meshes will persist in a decade.



Analyzing Future Threats



I've outlined why meshes remain crucial; pixel-generators lack the control professionals need for complex interactive media.

Gemini said



This is the exact existential debate currently dominating the intersection of AI and computer graphics.



To answer your question directly: Yes, the gaming and animation industries will still desperately need good, manipulable meshes in 10 years. Your meta-goal of making 3D geometry editable like a text document is not only a viable defense against the rise of video models, it is the exact missing link that professional creators are actively searching for right now.



Here is a breakdown of the technology risk, the limitations of "world models," and why structured geometry will survive.

The Threat: Neural Rendering and World Models



There is a massive push right now toward "Neural World Simulators." Startups like World Labs (Fei-Fei Li’s company), along with models like Google's Veo and OpenAI's Sora, are pushing the narrative that future game engines will shift from rendering geometry to generating pixels.



The argument is that instead of a game engine calculating polygons, lighting, and textures, an AI model will simply "dream" the next frame based on your controller input at 60 FPS.

Why Pure Pixel Generation Will Fail the Gaming Industry



While generative video is incredible for linear cinematic cutscenes, it fundamentally fails at the core requirement of interactive media: Determinism and Control.



    The Consistency Problem (Emergent Memory vs. Hard Memory): Video models lack explicit storage. If you turn your character around in an AI-generated world, look at a wall for two minutes, and turn back, the AI has to "hallucinate" the room again. It might look similar, but it won't be mathematically identical. For a competitive shooter or a precision platformer, that lack of absolute spatial consistency is game-breaking.



    Physics and Hitboxes: Video models do not understand physics; they only understand what physics looks like. You cannot run precise collision detection, rigid-body dynamics, or complex combat math on a flat array of pixels. A game engine needs to know exactly where a sword intersects a shield.



    The Director's Dilemma: In animation, directors do not want a "slot machine" output. They need exact, granular control. If an animator needs a character's left eyebrow raised exactly two millimeters to convey a specific emotion, a prompt-based video model cannot do that reliably. You must have an underlying rig and mesh to manipulate.



The 10-Year Horizon: "3D as Code"



The consensus emerging among graphics researchers in early 2026 is a hybrid future. The industry is moving toward a paradigm where 3D geometry acts as the code, and the game engine acts as the compiler/chip.



    The Output Layer will be AI: Traditional rendering (bouncing millions of light rays via path tracing) is computationally exhausting. We are already seeing the shift toward Neural Rendering (like DLSS 4.5). The engine will use a relatively simple mesh to establish the "truth" of the scene (where objects are, what the physics are), and then a neural network will "hallucinate" the high-fidelity lighting, micro-textures, and reflections over top of it in real-time.



    The Structural Layer will remain Meshes/Nodes: The underlying scaffolding—the logic, the collision, the rigs—must remain explicit, mathematical geometry.



Validating Your Meta-Goal



Your meta-goal—building software that allows people to edit 3D geometry as fluidly as text, relying on their innate spatial reasoning—is highly defensible.



Right now, the industry is stuck in a frustrating binary:



    Manual CAD/Houdini: Highly precise, but requires years of technical training and tedious menu-diving.



    Generative AI (Text-to-3D): Incredibly fast, but spits out a baked, uneditable asset with terrible topology. If it's 90% correct, it's useless, because fixing the remaining 10% of a collapsed, messy AI mesh takes longer than building it from scratch.



Your proposed procedural engine sits perfectly in the middle. By having an AI agent build the procedural recipe (the node tree) rather than just spitting out a static mesh, you retain the editability. You are giving the user a semantic, structured document that they can easily adjust.



If you can successfully build a system where a user can say "generate a gothic knight," get a mathematically sound riggable mesh, and then manually grab the pauldron and scale it up with an intuitive, non-destructive UI—you have built a tool that is immune to the video-model threat. You aren't competing with Sora; you are building the ultimate input tool for the next generation of game engines.

You said



take the opposite view and argue from there

Gemini said



The Argument: Why Traditional Meshes and 3D Rendering Pipelines Are Doomed



The belief that traditional 3D geometry (meshes, polygons, UV maps, and node-based procedural generation) will remain the standard in gaming and animation over the next ten years relies on a fundamental misunderstanding of the current trajectory of artificial intelligence. It assumes AI will only ever be a tool used within the existing paradigm, rather than a force that replaces the paradigm entirely.



Here is the argument for why your proposed procedural mesh-generation software—and the entire concept of the "3D mesh" as the core building block of digital media—is on a fast track to obsolescence.

1. The Mesh is the "Assembly Language" of Graphics



The history of computer science is the history of abstracting away underlying complexity. We do not write software in assembly language anymore; we write in high-level languages, and the compiler handles the hardware logic.



In graphics, the polygon mesh is assembly language. It is a highly unnatural, computationally expensive, and labor-intensive way to represent reality. We only use polygons because, historically, calculating flat triangles was the only math our silicon could perform fast enough to simulate 3D space.



But reality is not made of polygons. An AI model that understands spatial relationships doesn't need to build a wireframe, unwrap it to a 2D plane, paint a texture on it, and simulate millions of bouncing light rays to decide what color a pixel should be. It just directly outputs the light field.

2. The Rise of Real-Time "World Models"



The biggest threat to traditional game engines is the rapid advancement of Large World Models (LWMs). As of early 2026, companies like World Labs (founded by Fei-Fei Li), Google DeepMind, and OpenAI are aggressively shifting from predicting text to predicting physics and spatial reality.



    Google's GameNGen (2024/2025): Google successfully trained a neural network (GameNGen) to simulate the classic game DOOM at 20 frames per second without a game engine. It didn't render polygons; a diffusion model simply predicted the next frame based on the player's inputs and the previous frames. The game exists entirely as weights in a neural network.



    DeepMind's Genie 3 (Late 2025): Genie 3 advanced this by generating navigable, interactive 3D worlds at 24 frames per second from simple text prompts, maintaining visual consistency for minutes at a time. It doesn't rely on hard-coded collision detection or gravity; the model learned physical regularities from its training data.



    World Labs' Marble (Late 2025): This model generates persistent, explorable 3D environments from a single image or text prompt. It doesn't use meshes; it exports to Gaussian Splats (more on this below).



These models are currently constrained by compute power and short memory horizons, but if we project a 10-year timeline, the hardware constraints will evaporate. You won't play a game compiled in Unreal Engine 7; you will run an inference model that hallucinates the game world dynamically around you at 120 FPS.

3. Physics Can Be Learned, Not Programmed



The primary defense of the mesh is "determinism and physics." The argument goes: You need a mesh for a sword to hit a shield.



But "Spatial Intelligence" research proves that neural networks can learn intuitive physics directly from video data, just as humans do. A toddler doesn't calculate the polygons and mass of a ball before catching it; they have an internal "world model" that anticipates the trajectory.



AI models are developing this same capability (e.g., Meta's Joint Embedding Predictive Architecture, or JEPA). In a decade, if a player swings a sword at a wall in a neural game engine, the model won't check for mathematical polygon intersection. It will know, based on its training, that metal hitting stone results in a spark and a structural indentation, and it will simply generate those pixels. Determinism becomes an emergent property of a highly trained model, not a hard-coded mathematical rule.

4. 3D Gaussian Splatting is Killing the Polygon



Even in scenarios where explicit 3D assets are still needed (like AR/VR or bridging legacy game engines), the polygon mesh is being rapidly replaced by 3D Gaussian Splatting (3DGS) and Neural Radiance Fields (NeRFs).



Gaussian Splatting represents a scene not as connected vertices, but as millions of tiny, semi-transparent, mathematically defined clouds ("splats") floating in space.



    It is computationally vastly superior: It skips the incredibly heavy "ray tracing" process. The GPU just sorts the splats by depth and alpha-blends them onto the screen. It achieves photorealism at 60-120 FPS instantly.



    It captures reality better: Meshes struggle with fuzzy, volumetric things like fur, hair, glass, and smoke. Gaussian Splats handle them effortlessly.



    AI prefers it: When AI models (like World Labs' Marble) generate 3D spaces, they output Gaussian Splats, not meshes, because the continuous volumetric math of a splat aligns perfectly with how neural networks learn.



The Conclusion: The "Editability" Illusion



Your meta-goal is to allow people to edit 3D geometry as easily as text. But the text-editing paradigm itself has already changed. We don't write documents from scratch anymore; we prompt an LLM, evaluate the output, and prompt it again to refine it.



In 10 years, an art director won't want to manually grab the vertices of a mesh to widen a character's jaw. That is a low-level, mechanical task. They will simply tell the World Model: "Make him look 10% more intimidating and give him a stronger jawline." The neural network will instantly adjust the latent representation of the character, and the resulting pixels will reflect the change flawlessly from every angle.



If you build a business entirely around generating and fixing polygon meshes, you are building the world's best horse-drawn carriage at the dawn of the automobile. The future of digital media is not rendering geometry; it is hallucinating reality.

You said



ok which of those arguments is better, I could buy either, what is the synthesis

Gemini said



Both arguments are compelling because they are both partially right. If you look at the trajectory of companies like Nvidia, Meta, and the startups building the next generation of game engines in 2026, the industry is not choosing between pure polygons or pure pixel hallucination.



They are converging on a synthesis: The Hybrid Neural-Symbolic Pipeline.



Here is what that synthesis looks like, why it is the most likely outcome for the next 10-15 years, and exactly where your procedural generation software fits into it.

1. The Separation of "Logic" and "Presentation"



The fundamental flaw in the "World Models will replace everything" argument is that a video game or a 3D simulation is not just a visual medium; it is a database of spatial logic.



In the synthesized future, the game engine splits into two distinct layers:



    The Symbolic Layer (The Scaffolding): This is the domain of meshes, collision boxes, rigs, and procedural nodes. It is invisible to the player. It exists purely to calculate physics, determine line-of-sight, handle skeletal animation, and act as the mathematical "ground truth" of the world. It will be much lower-resolution than today's AAA meshes because it doesn't need to look good; it just needs to be mathematically precise.



    The Neural Layer (The Paint): This is the domain of generative AI, Neural Radiance Fields (NeRFs), and Gaussian Splats. Instead of the engine calculating how light bounces off a 4K texture map, a neural network looks at the low-poly "Symbolic" scaffolding and instantly hallucinates the photorealistic details, the fur, the reflections, and the micro-textures over it in real-time.



2. The Mesh Becomes the "Prompt"



In the text-to-image world, we use words to constrain the AI's hallucination. In the next generation of 3D, the mesh is the spatial prompt.



If you just ask a World Model to "generate a knight swinging a sword," you get the slot-machine effect. But if you provide a rigged, low-poly procedural mesh of a humanoid swinging a sword, and tell the neural renderer, "Wrap this geometry in hyper-realistic gothic armor," you get exact, 1:1 directorial control with infinite visual fidelity. The mesh constrains the AI's hallucination to the exact physical boundaries required by the game's hitboxes.

3. "Editability" Shifts Up the Abstraction Chain



The anti-mesh argument is correct that humans will stop pushing individual vertices. That is the equivalent of writing assembly code. However, the pro-mesh argument is correct that humans will absolutely demand structural control.



The synthesis is that we will edit Procedural Recipes, not raw geometry.



This is exactly why your concept of an LLM driving a procedural node tree (like your procedural_human Blender addon) is the right bet. You are building the high-level compiler.



    Old Way: An artist sculpts 100,000 polygons by hand.



    Pure AI Way: A prompter rolls the dice 50 times until Sora generates a video that looks okay, but they can't change the lighting.



    The Synthesized Way: An art director tells your AI agent, "Generate a humanoid with elongated proportions." Your agent builds the node tree. The director sees the output and says, "Make the shoulders wider." Your agent adjusts the math in the node tree. The engine outputs a low-poly rig. The neural renderer makes it look like a photorealistic alien.



The Conclusion for Your Business



The synthesis proves that your core instinct is correct, but it refines your product's ultimate value proposition.



Your software's value is not in generating ultra-high-density, photorealistic meshes to compete with neural rendering. Your software's value is in automating the creation of perfect, riggable, mathematically sound scaffolding. If you can build the platform that reliably translates human intent into the structural, procedural logic that the next generation of neural game engines needs to anchor their hallucinations, you have a product that every studio on earth will need. You aren't building a renderer; you are building the ultimate spatial control interface.

This is a rich conversation. Let me give you an honest assessment of the quality of Gemini's reasoning, where it's strong, where it's performing for you rather than thinking with you, and what I think is actually unresolved.

Where Gemini is Strong
The "recipe vs. blob" framing is genuinely good. This is the single most important insight in the entire conversation and it came from your original doc, not from Gemini. Gemini correctly identified it as the core moat. A procedural node tree is a structured, editable, composable representation. A diffusion output is a terminal artifact. That distinction is real and durable.

The BrickLink analysis is sharp. The insight that the CAD software is a demand generator for the marketplace — not the product itself — is a clean structural observation. The flywheel of "power users publish recipes, casual users tweak and buy" is the right business topology for a creative tools platform.

The AEC pivot analysis is honest. Gemini correctly told you to stay away from engineering (liability wall, FEA requirements, Autodesk lock-in) and pointed you toward architecture, where the pain is aesthetic and presentational rather than structural. That's good advice.

Where Gemini is Performing Rather Than Thinking
The 30-step Greg Isenberg mapping is almost entirely filler. Gemini took a generic SaaS playbook and mechanically substituted your domain nouns into each step. "Step 18: Store user preferences" becomes "teach the agent the specific domain vocabulary and art style of the studio." That's not a plan — it's Mad Libs. The steps that actually matter for your business (how do you get the first 5 paying customers, what does the service deliverable look like, how do you price the manual work) are glossed over with platitudes. If you actually tried to execute "Phase 3: Service First" tomorrow, you'd find there's nothing actionable there.

The "Code-to-Resin" pipeline overestimates integration value. The argument that you can auto-hollow, auto-support, and auto-drain models sounds compelling, but these are solved problems. Every slicer (Lychee, ChiTuBox, PreForm) already does this automatically. The hard part of resin printing isn't mesh prep — it's material science, machine calibration, post-curing, quality control, and shipping fragile objects. Gemini is treating physical manufacturing as a straightforward extension of software when it's actually a completely different operational discipline. This is the kind of advice that sounds smart but would burn a lot of your capital if you followed it.

The architecture pivot is premature and scattershot. One moment you're building procedural humanoids for game devs, the next you're generating parametric facades for architects, then you're printing physical building models. These are three entirely different customer segments with different sales cycles, different technical requirements, and different competitive landscapes. Gemini should have pushed back harder on scope creep rather than enthusiastically mapping every adjacent market. A startup that tries to serve indie game devs, architecture firms, AND tabletop miniature collectors simultaneously serves none of them.

The Synthesis Argument: What's Actually Unresolved
The "hybrid neural-symbolic pipeline" synthesis is intellectually satisfying but commercially ambiguous. Here's why:

The synthesis assumes you'd be building scaffolding for neural renderers. But neural rendering is being built by Nvidia (DLSS), Epic (Nanite + neural lighting research), and Meta (for VR). These are companies with orders of magnitude more compute, data, and renderer integration than you could achieve. If the future is "low-poly scaffold + neural paint," the scaffold generation becomes a commodity and the neural paint becomes the value. You'd be building the cheap part.

The real question the synthesis dodges is: who controls the interface? The argument that "art directors will edit procedural recipes, not vertices" is correct. But will they edit those recipes in your tool, or in Blender/Houdini/Unreal with an AI copilot built by the platform owner? If Epic ships an LLM-guided node editor inside Unreal Engine 6, your standalone tool loses its reason to exist overnight. The moat isn't the recipe format — it's whether you own the environment where recipes are authored.

The counter-argument (meshes are doomed) is weaker than Gemini made it sound, but it contains a real kernel. GameNGen running DOOM at 20fps without geometry is a tech demo, not a product. Genie 3 generating "navigable worlds" at 24fps with minutes of consistency is nowhere near production-ready for a game that needs to run for hundreds of hours. The "physics can be learned" argument via JEPA is speculative research, not deployed technology. But the kernel of truth is this: the volume of use cases that require production-quality meshes is shrinking. Background assets, environmental props, skyboxes — these will increasingly be neural. The use cases that remain (player characters, rigged creatures, interactive objects) are the high-value, high-control ones. That's actually good news for you, but it means your total addressable market is smaller than "all 3D content."

What I Think Is Actually True
Your moat is not "procedural generation." Your moat is the training corpus of DSL examples. Anyone can build a procedural system. The defensible asset is a large, curated library of decomposed recipes that you can fine-tune models on. That library has a cold-start problem — you have to build it manually before the flywheel works — and that's the real bottleneck, not the software architecture.

The "service first" advice is correct in spirit but wrong in specifics. Don't sell "custom 3D characters to indie studios." Indie studios have no money. Sell to mid-market game studios (
5
M
–
5M–50M revenue) who have budget but not enough technical artists. The deliverable should be a rigged, game-engine-ready character with blend shapes and a clean skeleton, not a Blender file.

The biggest risk isn't technology — it's timing. If foundation model companies crack consistent, editable 3D generation in the next 2–3 years (plausible but not certain), your training corpus won't be large enough to matter. If it takes them 5–7 years (more likely given the topology/editability problem), you have a real window. The question is whether you can build a large enough library of procedural recipes and a small enough but loyal customer base before that window closes.

The Houdini displacement angle is your strongest positioning. Houdini is expensive, hard to learn, and SideFX has done essentially nothing with AI integration. If you can offer "Houdini-grade procedural power, driven by natural language, at indie pricing," that's a pitch that sells itself. The risk is that SideFX ships their own AI features, but incumbent companies are historically terrible at disrupting their own pricing models.

Gemini never challenged you on team composition. You have a brainstorming doc with ideas spanning dating apps, drones, autonomous boats, solar farms, restaurant optimization, and 3D generation. That breadth suggests the team hasn't committed. The most important decision isn't which idea to pursue — it's whether everyone will actually work on the same thing for 18+ months without getting distracted by the next interesting problem. The AutoCAD story you cited answers this: they had 15 products and went all-in on one after CES. You need your CES moment, and it probably comes from shipping something small in the 3D space and seeing if anyone cares.

re-write the section on the startup ideas podcast to be actionable.

Here's the rewrite. I'm replacing the six generic phases with four that have concrete deliverables, timelines, and kill criteria.

Phase 1: Validate Demand Before Building (Weeks 1–4)
Goal: Determine if anyone will pay for procedurally generated, production-ready 3D characters before you build the product.

Week 1–2: Identify 50 potential buyers by name.

Go to the Unity Asset Store and Unreal Marketplace. Find every studio or publisher that has released a character pack in the last 12 months. These are people who already pay for 3D characters and understand the workflow. Write down the studio name, contact info, and what they sell.
Search ArtStation job boards for "character artist" postings. Every company hiring a character artist has the pain you're solving. They need characters and don't have enough people to make them. Record the company, the role, and the budget range if listed.
Join the Blender Artists, Polycount, and r/gamedev communities. Search for threads where people complain about character pipelines, retopology, rigging, or asset turnaround time. DM the most articulate complainers.
Week 3: Cold outreach with a specific offer. Write a short email/DM with this structure:

"I'm building a tool that procedurally generates rigged humanoid characters ready for import into Unity/Unreal. The output is a clean quad mesh with a standard skeleton, blend shapes, and LODs — not a sculpt that needs retopo. I'm looking for 3 studios to do a paid pilot: you describe the character, I deliver the game-ready asset in 5 business days. $500 per character. Interested?"

Send this to all 50 contacts. The $500 price point is deliberately low — you're buying information, not maximizing revenue.

Week 4: Evaluate responses.

If 0 out of 50 respond: the pain isn't where you think it is, or you're talking to the wrong people. Pivot the outreach to a different segment (architectural visualization, VTuber model creators, tabletop miniature designers) and repeat.
If 3–5 respond with interest but push back on price or deliverable format: you've found the pain. Their objections tell you exactly what the product needs to be.
If 5+ want to pay: proceed to Phase 2 immediately.
Kill criterion: If you can't find 3 people willing to pay $500 for a custom rigged character after 100 outreach messages across two customer segments, the market signal is too weak to justify building.

Phase 2: Deliver Manually, Document Everything (Months 2–4)
Goal: Fulfill 10–20 paid orders using your existing CLI + Blender pipeline, no matter how manual it is. Every order teaches you what the product actually needs to be.

For each order:

Get a written brief from the client: character description, target engine (Unity/Unreal/Godot), poly budget, skeleton standard (Mixamo, UE5 Mannequin, custom), and any reference images.
Use your procedural_human addon and CLI agent loop to generate the base mesh. Time yourself. Write down every step where you intervene manually — these are the automation targets for Phase 3.
Rig the character to their requested skeleton. If your system doesn't handle this yet, do it by hand in Blender. Record the time.
Export to their target format (FBX/glTF). Import into their engine. Send them a screenshot proving it works in-engine, not just in Blender.
Deliver. Ask for a 5-minute feedback call. Ask exactly two questions: "What would you change about the output?" and "Would you order again at $1,500?"
What you're building during this phase:

A spreadsheet of every manual step, how long it takes, and whether the CLI agent could do it. This becomes your engineering roadmap.
A portfolio of shipped, in-engine characters you can show to future customers.
Pricing data: the 
1
,
500
q
u
e
s
t
i
o
n
t
e
l
l
s
y
o
u
w
h
e
r
e
t
h
e
p
r
i
c
e
c
e
i
l
i
n
g
i
s
.
I
f
e
v
e
r
y
o
n
e
s
a
y
s
y
e
s
a
t
1,500questiontellsyouwherethepriceceilingis.Ifeveryonesaysyesat1,500, you're underpriced. If everyone says no, you've found the ceiling.
What you're NOT building during this phase:

A website with fancy UI
A self-serve platform
Anything that scales before you understand the unit economics
Phase 3: Automate the Bottlenecks (Months 4–8)
Goal: Take the spreadsheet from Phase 2 and eliminate the manual steps that consume the most time per order.

By this point you'll know empirically which steps eat your hours. Typical candidates based on your current architecture:

If rigging is the bottleneck: Build auto-rigging into the procedural system. Since your node trees already decompose the character into semantic parts (torso, arm, hand, finger), you can walk that tree to place bones automatically. This is high-value automation because manual rigging is 4–8 hours per character.

If iteration/revision is the bottleneck: Build the parameter exploration grid you described in your agent loop — 16 renders with variations, client picks a number, agent refines. This turns a back-and-forth email chain into a single interaction.

If export/engine compatibility is the bottleneck: Build validated export presets for the top 3 engines. Test each export against a standard import script in the target engine. Ship a test report with every deliverable.

Pricing shift: Once your per-character labor drops below 4 hours, raise the price to 
1
,
500
–
1,500–2,500. Your margin is now high enough to sustain the business on 5–10 orders per month.

Start the content library: Every character you deliver (with client permission, or with identifying details removed) becomes a recipe in your DSL training corpus. By order 30, you have 30 examples. By order 100, you can start testing LoRA fine-tuning on your DSL format. This is the flywheel beginning to turn.

Phase 4: Decide What You're Actually Building (Month 8+)
By month 8, you have hard data on three questions that are currently unanswerable:

Is the market big enough? You've talked to 100+ potential customers and fulfilled 30+ orders. You know the conversion rate, the reorder rate, and the price ceiling. If reorder rate is above 40%, you have a product. If it's below 20%, you have a novelty.

Can the agent loop replace you? You've measured which steps are automated and which still require your judgment. If the agent handles 80%+ of the work autonomously, you can build a self-serve platform. If you're still manually intervening on every order, you have a consulting business with tooling, not a software product.

Is the DSL corpus large enough to fine-tune on? With 50–100 procedural recipes, you can test whether a fine-tuned model generates valid, novel DSL sequences. If it can, you've proven the flywheel works and the moat gets deeper with every order. If it can't, you need either more data or a different approach to generation.

These answers determine your next move:

High reorder rate + high automation + working LoRA → raise capital, build the self-serve platform, hire a technical artist to expand the recipe library full-time.
High reorder rate + low automation → stay in the service model, charge premium prices ($5k+ per character), grow slowly on cash flow.
Low reorder rate → the product-market fit isn't there. Take what you've learned about the DSL and the agent loop and point it at whichever adjacent market (architecture, tabletop, VTuber) showed the most pull during Phase 1 outreach.
The Media Flywheel (Runs in Parallel, Not as a Phase)
Content creation is not a phase — it's a habit that runs alongside everything above.

What to post and where:

Screen recordings of the agent loop building a character from nothing. Speed them up to 60 seconds. Post on X, Reddit (r/blender, r/gamedev, r/proceduralgeneration), and YouTube Shorts. The visual of geometry assembling itself from math is inherently compelling — you don't need to be a good video editor.
Before/after comparisons: "Left: what a text-to-3D model outputs. Right: what our procedural system outputs. Same prompt." Show the topology wireframe. This is the single most convincing image you can create because the difference is visually obvious to anyone who has ever opened a 3D package.
Technical breakdowns on how specific node trees work. Post these on Blender Artists and HackerNews. These establish credibility and attract the power users who might eventually contribute recipes to your marketplace.
What NOT to do:

Don't pay for ads until you have a landing page with a waitlist of 500+ organic signups.
Don't hire a "content person." The founder who understands the tech creates the best content because they can speak to the pain authentically.
Don't create content about "AI" generically. Create content about the specific, ugly problem you solve: broken topology, non-manifold edges, meshes that explode when you try to rig them.
Last question, likely we should sever our reliance on blender and create a custom set of nodes to generate topology since this bypasses the GPL licensing requirements, what would it take in the current repositiory to achieve this?

Great question — this is the most consequential architectural decision for the business. Let me explore what actually depends on Blender in your codebase.

This is a thorough question and the answer is nuanced. Here's the full picture.

What You're Actually Coupled To
Your codebase has roughly three layers of Blender dependency, and they differ drastically in how hard they are to replace:

Layer 1: Registration & UI (Replaceable, Low Risk)
Decorators, panels, operators, gizmos, menus, preferences. This is ~30 files of bpy.types.Operator, bpy.types.Panel, bpy.utils.register_class, and layout code. It's boilerplate — any target application (custom app, web UI, Unreal plugin) would need its own equivalent, but the pattern is the same. This layer is disposable by design.

Layer 2: The Node Graph Wiring (~60–70% of geo_node_groups/)
This is the bulk of your code. Files like coon_patch.py, all of armor/, the DSL primitive generate() methods — they're essentially programs written in Blender's geometry node API. Every line looks like:

node = group.nodes.new("GeometryNodeMeshCylinder")
link_or_set(group, node.inputs["Radius"], radius_socket)
This is the hardest layer to sever because the code is the Blender API. It's not calling Blender to do work — it's authoring Blender node trees programmatically. To replace this, you need a different target to author node trees for.

Layer 3: Actual Math & Domain Logic (~30–40% of geo_node_groups/, plus definitions)
Bezier evaluation, Coons patch interpolation, domain edge distance calculations, the DSL structure (SegmentChain, JoinedStructure, Bone, IKLimits), the executor, the topological sort in Output, the body part definitions in finger.py and torso.py. These have zero Blender imports and survive the transition unchanged.

What a Custom Engine Needs to Replace Blender
Based on the ~100 unique Blender geometry node types your codebase uses, here's what you'd need to build:

Tier 1: You Cannot Ship Without These
Capability	Blender Equivalent	Difficulty
Mesh primitives (grid, cylinder, ico-sphere, line)	GeometryNodeMeshGrid, etc.	Low — well-documented algorithms
Curve primitives (line, circle, arc, Bezier)	GeometryNodeCurvePrimitive*	Low
Curve-to-mesh sweep	GeometryNodeCurveToMesh	Medium — cross-section sweep along path
Set position / offset	GeometryNodeSetPosition	Low — direct vertex manipulation
Join geometry	GeometryNodeJoinGeometry	Low — concatenate vertex/face buffers
Merge by distance	GeometryNodeMergeByDistance	Medium — spatial hashing + welding
Scalar/vector/int math	ShaderNodeMath, ShaderNodeVectorMath	Low
Named attributes (store/read)	GeometryNodeStoreNamedAttribute	Medium — need a per-element attribute system
Subdivision surface	GeometryNodeSubdivisionSurface	Hard — Catmull-Clark implementation
Mesh boolean (union/intersect/difference)	GeometryNodeMeshBoolean	Very hard — robust CSG is a multi-year research problem
Instance on points + realize	GeometryNodeInstanceOnPoints	Medium
Tier 2: Needed for Full Feature Parity
Capability	Difficulty
Curve resampling, trimming, filleting	Medium
Extrude mesh	Medium
Delete geometry by selection	Low-medium
Proximity / nearest surface sampling	Medium (spatial index)
Repeat zones / foreach	Medium (loop constructs in DAG)
Float curve mapping	Low (piecewise interpolation)
Noise textures	Low (simplex/perlin)
Raycast	Medium-hard (BVH tree)
Tier 3: The Library You'd Use Instead of Writing From Scratch
You would not write a subdivision surface implementation or a mesh boolean solver. You'd use existing open-source geometry processing libraries:

CGAL (C++) — the gold standard for mesh booleans, subdivision, and computational geometry. GPL/LGPL licensed but you'd use it server-side, so GPL is fine.
libigl (C++) — lighter weight, MIT licensed, good for mesh operations.
OpenCascade (C++) — CAD-grade boolean operations, LGPL.
Manifold (C++) — Blender's own boolean engine, extracted as a standalone library. Apache 2.0.
trimesh (Python) — good for mesh I/O and basic operations, MIT licensed.
The realistic architecture would be: Python DSL → your custom DAG evaluator → calls into CGAL/Manifold/libigl for the heavy geometry operations → outputs mesh data (vertices, faces, normals, UVs).

The Refactoring Path
Given what's in the repo today, here's how I'd sequence the separation:

Step 1: Define the Abstract Node Interface
Create a backend-agnostic node graph representation. Every node has typed input/output sockets, a node type enum, and properties. The graph is a DAG. This is already conceptually what you have — it's just expressed directly as Blender API calls instead of as an intermediate representation.

You'd need something like:

class NodeGraph:
    def add_node(self, node_type: NodeType, **properties) -> NodeRef
    def link(self, output: SocketRef, input: SocketRef)
    def set_default(self, input: SocketRef, value)
    def add_input(self, name: str, socket_type: SocketType) -> SocketRef
    def add_output(self, name: str, socket_type: SocketType) -> SocketRef
This mirrors exactly what node_helpers.py already does — create_node, link_or_set, math_op — but targeting an abstract graph instead of bpy.data.node_groups.

Step 2: Rewrite node_helpers.py Against the Abstraction
Your ~680-line node_helpers.py is the single most important file. Every geo_node_group file calls into it. If you make create_node, link_or_set, math_op, vec_math_op, combine_xyz, separate_xyz, etc. target the abstract NodeGraph instead of group.nodes.new(...), then every file that only uses these helpers needs zero changes.

Step 3: Build Two Backends
Blender backend: Takes the abstract NodeGraph and emits Blender node trees via bpy. This keeps your existing Blender addon working during the transition. It's essentially the current node_helpers.py as a backend.
Native backend: Takes the abstract NodeGraph and evaluates it directly using CGAL/Manifold/libigl. This is the proprietary engine.
Step 4: Port geo_node_groups One at a Time
Since ~60-70% of each file is wiring (create_node, link_or_set, math_op calls) and those calls now target the abstraction, most files port with minimal changes. The files that directly touch bpy.data.node_groups.new() or use Blender-specific features (closures, foreach zones) need manual attention.

Step 5: Port DSL Primitives
Each primitive's generate() method is ~100–400 lines of node wiring. Once node_helpers targets the abstraction, these methods port by replacing context.node_group references with the abstract NodeGraph.

Honest Effort Estimate
Component	Effort
Abstract node graph + Blender backend (step 1-2)	2–4 weeks
Native evaluator skeleton with mesh primitives + math + join	4–6 weeks
Integrating CGAL/Manifold for booleans + subdivision	2–4 weeks
Curve operations (sweep, resample, trim, fill)	3–5 weeks
Attribute system (per-element named attributes, domains)	2–3 weeks
Porting geo_node_groups to abstraction (~77 files)	4–6 weeks
Porting DSL primitives to abstraction (~12 files)	2–3 weeks
Export pipeline (FBX/glTF/STL output)	2–3 weeks
Rendering for validation (headless render of results)	2–3 weeks
Total: roughly 6–9 months of focused, full-time work for one experienced developer. This assumes you keep the Blender backend alive during the transition so you can validate the native backend against known-good Blender output.

The Strategic Question
The key decision isn't whether to sever — it's when. The abstraction layer (steps 1-2) is worth doing immediately regardless, because it makes your code portable and testable without Blender. The native backend (steps 3+) is a major investment that only pays off when you're ready to ship a standalone product or need to avoid GPL contamination for a commercial server.

The cheapest path is: abstract the node graph now, keep Blender as the only backend, build the native backend when revenue from Phase 2/3 (the service business) justifies the engineering investment. Blender remains your free R&D environment and visual debugger; the proprietary engine is what you charge for.

GAL (C++) — the gold standard for mesh booleans, subdivision, and computational geometry. GPL/LGPL licensed but you'd use it server-side, so GPL is fine.



I dont undestand this, wouldn't using GPl infect the rest of the codebase?

Good catch — my statement was imprecise. Here's how it actually works:

The GPL "Distribution" Trigger
GPL's copyleft clause activates only when you distribute the software — meaning when you give someone else a copy of the binary or source code. The key word in the GPL text is "convey."

If you run GPL code on your own server and users interact with it over HTTP (which is your architecture — CLI client sends requests to a proprietary server), you are not distributing the GPL code. The user never receives a copy of CGAL. They receive the output (a mesh), not the program. GPL has no restrictions on the output of a program.

This is commonly called the "SaaS loophole" in GPL, and it's not a loophole — it's how the license was intentionally written. The Free Software Foundation acknowledged this gap and created the AGPL (Affero GPL) specifically to close it. AGPL adds the requirement that if users interact with the software over a network, you must still provide source code.

CGAL is GPL v3+, not AGPL. So the SaaS loophole applies.

What This Means for Your Architecture
Your brainstorming doc already identified the right architecture: thin open-source Blender client + proprietary server that does the real work. If you extend that to the custom engine:

Server-side (never distributed): Your proprietary engine links against CGAL for booleans and subdivision. GPL applies to the combined binary on your server. But since you never ship that binary to anyone, the copyleft never triggers. Your server code remains proprietary.

Client-side (distributed to users): The thin Blender addon, or a future custom UI client, communicates over HTTP. This code cannot link against CGAL or any GPL library, because you are distributing it. It must be either GPL itself (fine for the Blender addon, which is already GPL-contaminated by Blender) or use only permissive-licensed dependencies.

Where It Would Infect You
GPL would infect your codebase if you:

Shipped a desktop application that bundled CGAL — the entire application would need to be GPL.
Distributed a Python package that imported a CGAL binding — same problem.
Used an AGPL library on your server — then network interaction counts as distribution.
The Safer Alternatives
If you ever want the option to distribute the engine (e.g., sell an on-premise version to a studio that won't use a cloud service), you'd want to avoid GPL entirely. In that case:

Library	License	Capability
Manifold	Apache 2.0	Mesh booleans (this is what Blender itself uses internally now)
libigl	MPL 2.0	Broad mesh processing, but booleans depend on CGAL under the hood
OpenCascade	LGPL 2.1	CAD-grade booleans, B-rep modeling
trimesh	MIT	Mesh I/O, basic operations
Manifold is probably your best bet — it's the same boolean engine Blender uses, it's Apache 2.0 (fully permissive), and it's specifically designed for fast, robust CSG operations. Using it keeps every distribution option open, including on-premise licensing, while still giving you production-quality booleans.

The short version: GPL on the server is fine as long as you never distribute the server binary. But if you want maximum flexibility in your business model, prefer Apache/MIT/LGPL libraries and avoid the question entirely.