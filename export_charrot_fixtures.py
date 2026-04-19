"""Export Charrot-Gregory patch reference fixtures for the Ixdar Java port.

Run inside Blender with the procedural_human package installed:

    blender --background --python export_charrot_fixtures.py

For each test case (triangle, pentagon, hexagon, asymmetric hexagon), builds a
mesh with bezier-handled edges, runs the CoonNGonPatchGenerator geometry
node group, samples the output points at a fixed subdivision level, and writes
the input + output to a JSON file under ixdar-app/test/resources/charrot-gregory/.

Output schema (per fixture JSON):
    {
      "n": 5,
      "subdivisions": 3,
      "input_curves": [
        [[p0x, p0y, p0z], [p1x, p1y, p1z], [p2x, p2y, p2z], [p3x, p3y, p3z]],
        ...  // n curves
      ],
      "output_points": [[x, y, z], ...]
    }

The Ixdar test CharrotGregoryPatchTest can load these and compare per-point to
a tolerance of 1e-4 * mesh_extent to detect any divergence from the reference.
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path


FIXTURE_OUT_DIR = Path.home() / "Code" / "Ixdar" / "ixdar-app" / "test" / "resources" / "charrot-gregory"
SUBDIVISIONS = 3


def regular_ngon_vertices(n: int, radius: float = 1.0) -> list[tuple[float, float, float]]:
    """Vertices on the unit circle at angles (i + 0.5) * 2π/n + π — matches the
    canonical n-gon parameterization used by the Blender node group."""
    out = []
    for i in range(n):
        theta = (i + 0.5) * 2.0 * math.pi / n + math.pi
        out.append((radius * math.cos(theta), radius * math.sin(theta), 0.0))
    return out


def straight_bezier(a, b):
    """Cubic bezier from a to b with P1, P2 at 1/3, 2/3 along the chord
    (straight-line curve, no curvature)."""
    def lerp(a, b, t):
        return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    return [a, lerp(a, b, 1.0 / 3.0), lerp(a, b, 2.0 / 3.0), b]


def curved_bezier(a, b, lift):
    """Bezier from a to b with P1, P2 lifted along +z by `lift` to create a
    smooth dome."""
    def lerp(a, b, t):
        return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    p1 = lerp(a, b, 1.0 / 3.0)
    p2 = lerp(a, b, 2.0 / 3.0)
    p1 = (p1[0], p1[1], p1[2] + lift)
    p2 = (p2[0], p2[1], p2[2] + lift)
    return [a, p1, p2, b]


def build_test_case(n: int, variant: str = "flat") -> list[list]:
    """Return n boundary bezier curves (list of 4-point curves) for one test."""
    verts = regular_ngon_vertices(n)
    curves = []
    for i in range(n):
        a, b = verts[i], verts[(i + 1) % n]
        if variant == "flat":
            curves.append(straight_bezier(a, b))
        elif variant == "domed":
            curves.append(curved_bezier(a, b, 0.25))
        elif variant == "mixed":
            # Alternate edges flat and lifted to break symmetry.
            if i % 2 == 0:
                curves.append(straight_bezier(a, b))
            else:
                curves.append(curved_bezier(a, b, 0.3))
        else:
            raise ValueError(f"unknown variant {variant!r}")
    return curves


def run_node_group_in_blender(n: int, curves: list, subdivisions: int) -> list:
    """Build a Blender mesh with bezier handles matching `curves`, run
    CoonNGonPatchGenerator, return the output mesh vertex positions.

    Requires Blender with bpy available and the procedural_human package
    registered so the node group exists.
    """
    import bpy

    # Build input mesh: a single n-gon face with N vertices.
    verts = [curves[i][0] for i in range(n)]
    faces = [list(range(n))]
    mesh = bpy.data.meshes.new("charrot_fixture_input")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Store bezier handle attributes on each edge. Each edge carries
    # handle_start (vector from V1 toward P1) and handle_end (vector from V2
    # toward P2) per the Blender node-group contract.
    import array
    mesh.attributes.new("handle_start_x", "FLOAT", "EDGE")
    mesh.attributes.new("handle_start_y", "FLOAT", "EDGE")
    mesh.attributes.new("handle_start_z", "FLOAT", "EDGE")
    mesh.attributes.new("handle_end_x", "FLOAT", "EDGE")
    mesh.attributes.new("handle_end_y", "FLOAT", "EDGE")
    mesh.attributes.new("handle_end_z", "FLOAT", "EDGE")

    for ei, edge in enumerate(mesh.edges):
        v1 = curves[ei][0]
        p1 = curves[ei][1]
        p2 = curves[ei][2]
        v2 = curves[ei][3]
        hs = (p1[0] - v1[0], p1[1] - v1[1], p1[2] - v1[2])
        he = (p2[0] - v2[0], p2[1] - v2[1], p2[2] - v2[2])
        mesh.attributes["handle_start_x"].data[ei].value = hs[0]
        mesh.attributes["handle_start_y"].data[ei].value = hs[1]
        mesh.attributes["handle_start_z"].data[ei].value = hs[2]
        mesh.attributes["handle_end_x"].data[ei].value = he[0]
        mesh.attributes["handle_end_y"].data[ei].value = he[1]
        mesh.attributes["handle_end_z"].data[ei].value = he[2]

    obj = bpy.data.objects.new("charrot_fixture_input", mesh)
    bpy.context.collection.objects.link(obj)

    # Attach a geometry-nodes modifier that uses CoonNGonPatchGenerator.
    mod = obj.modifiers.new("charrot_patch", "NODES")
    group = bpy.data.node_groups.get("CoonNGonPatchGenerator")
    if group is None:
        # Try to register the procedural_human package's node groups.
        from procedural_human.geo_node_groups.charrot_gregory_patch import (
            create_charrot_gregory_group,
        )
        group = create_charrot_gregory_group()
    mod.node_group = group
    # Set Subdivisions input (input slot name varies by Blender version; we try
    # both by index and by key).
    try:
        mod["Input_2"] = subdivisions
    except Exception:
        pass

    # Evaluate the dependency graph to get the modifier output.
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    eval_mesh = eval_obj.to_mesh()

    points = [(v.co.x, v.co.y, v.co.z) for v in eval_mesh.vertices]
    eval_obj.to_mesh_clear()

    # Clean up the scene so subsequent runs start fresh.
    bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.meshes.remove(mesh, do_unlink=True)

    return points


def export_fixture(name: str, n: int, variant: str) -> None:
    curves = build_test_case(n, variant)
    try:
        points = run_node_group_in_blender(n, curves, SUBDIVISIONS)
    except ImportError:
        print(f"[{name}] Blender bpy not available — skipping output sampling. "
              f"Writing input-only fixture.")
        points = []

    payload = {
        "n": n,
        "subdivisions": SUBDIVISIONS,
        "variant": variant,
        "input_curves": [[list(p) for p in curve] for curve in curves],
        "output_points": [list(p) for p in points],
    }

    FIXTURE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIXTURE_OUT_DIR / f"{name}.json"
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"[{name}] wrote {out_path} ({n=}, {variant=}, {len(points)} points)")


def main() -> None:
    export_fixture("triangle_flat", 3, "flat")
    export_fixture("pentagon_flat", 5, "flat")
    export_fixture("pentagon_domed", 5, "domed")
    export_fixture("hexagon_mixed", 6, "mixed")


if __name__ == "__main__":
    main()
