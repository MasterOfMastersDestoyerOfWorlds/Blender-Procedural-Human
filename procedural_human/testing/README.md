# Procedural Human Testing Module

Automated testing infrastructure for Coon/Charrot-Gregory patch geometry node validation.

## Components

### 1. Topology Checker (`topology_checker.py`)

Analyzes exported CSV data to detect "star patterns" - topology errors where corner points connect to distant points instead of adjacent grid points.

```python
# Usage (standalone, no Blender required)
from procedural_human.testing import run_quick_check

result = run_quick_check()
print(f"Passed: {result['passed']}, Failed: {result['failed']}")
```

### 2. Test Operators (`test_operators.py`)

Blender operators that automate the testing workflow:

- `bpy.ops.procedural.setup_coon_test()` - Setup test scene
- `bpy.ops.procedural.apply_and_export()` - Apply modifier, export CSVs
- `bpy.ops.procedural.verify_topology()` - Run topology check
- `bpy.ops.procedural.run_full_coon_test()` - Complete test cycle

### 3. Blender HTTP Server (`blender_server.py`)

HTTP server running inside Blender for external tool integration.
The CLI (`uv run blender-cli`) communicates with this server.

```python
# Server starts automatically when the addon loads via blender_bootstrap.py.
# Manual start from Blender Python console:
bpy.ops.procedural.start_test_server(port=9876)
```

## Verification Algorithm

For each corner point P:

1. Find all edges with P as endpoint
2. Get the other endpoint Q for each edge
3. Calculate distance |P - Q|
4. **Pass**: All Q are within `edge_length / subdivisions * 1.5`
5. **Fail (star pattern)**: Any Q is more than `edge_length * 0.8` away

## Running Tests

```bash
# Quick topology check on latest CSVs
python procedural_human/testing/topology_checker.py

# Full validation via CLI (preferred)
uv run blender-cli validate --group <GroupName>
```
