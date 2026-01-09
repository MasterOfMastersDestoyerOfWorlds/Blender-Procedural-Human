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

HTTP server running inside Blender for external tool integration:

```python
# In Blender Python console
bpy.ops.procedural.start_test_server(port=9876)

# Send commands from external process
import requests
response = requests.post("http://localhost:9876/command", json={
    "action": "run_test",
    "params": {"subdivisions": 2}
})
```

### 4. MCP Server Bridge (`mcp_server.py`)

MCP server for Claude/Cursor integration:

```bash
# Run MCP server
python -m procedural_human.testing.mcp_server

# Or test connection to Blender
python -m procedural_human.testing.mcp_server --test
```

## Setup for Claude Integration

1. **Start Blender** and load the addon

2. **Start the HTTP server** in Blender's Python console:
   ```python
   bpy.ops.procedural.start_test_server()
   ```

3. **Configure Cursor** to use the MCP server:
   - Copy `mcp_config.json` to your Cursor settings
   - Or add to `.cursor/mcp.json` in your project

4. **Use tools in conversation**:
   - Claude can now call `run_coon_patch_test`, `check_corner_topology`, etc.

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `run_coon_patch_test` | Run full test cycle |
| `get_point_data` | Query specific point attributes |
| `check_corner_topology` | Verify single corner |
| `get_csv_data` | Get latest export info |
| `verify_topology` | Check all corners |
| `setup_test` | Setup without applying |
| `apply_and_export` | Apply and export CSVs |
| `ping_blender` | Check server status |

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

# Test MCP tools (requires Blender server running)
python -m procedural_human.testing.mcp_server --test
```
