# Adding MCP Tools for the Blender Addon

This guide explains how to add new MCP (Model Context Protocol) tools for testing and debugging the Procedural Human addon.

## Architecture Overview

The MCP system has three layers:

1. **Blender Operators** (`test_operators.py`) - Execute actions inside Blender
2. **Blender Server** (`blender_server.py`) - Socket server running inside Blender that handles commands
3. **MCP Server** (`mcp_server_standalone.py`) - External MCP server that Cursor connects to

```
Cursor IDE <-> MCP Server (standalone) <-> Blender Server <-> Blender Operators
```

## Adding a New Tool

### Step 1: Add the Blender Operator (if needed)

In `procedural_human/testing/test_operators.py`:

```python
@procedural_operator
class PROC_OT_my_new_test(Operator):
    """Description of what this test does"""
    
    bl_idname = "procedural.my_new_test"
    bl_label = "My New Test"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Add properties
    my_param: IntProperty(
        name="My Param",
        default=1
    )
    
    def execute(self, context):
        # Your test logic here
        return {'FINISHED'}
```

### Step 2: Add Command Handler in Blender Server

In `procedural_human/testing/blender_server.py`:

```python
def handle_my_new_test(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle my new test command."""
    my_param = params.get("my_param", 1)
    
    try:
        result = bpy.ops.procedural.my_new_test(my_param=my_param)
        return {
            "success": result == {'FINISHED'},
            "operator_result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
```

Then register it in the `COMMAND_HANDLERS` dict:

```python
COMMAND_HANDLERS = {
    # ... existing handlers ...
    "my_new_test": handle_my_new_test,
}
```

### Step 3: Add MCP Tool in Standalone Server

In `mcp_server_standalone.py`, add TWO things:

#### 3a. Add the tool handler function:

```python
async def tool_my_new_test(my_param: int = 1) -> Dict[str, Any]:
    """Description of what this tool does (shown to Cursor AI)."""
    return await _client.send_command("my_new_test", {
        "my_param": my_param
    })
```

**Important:** The function name MUST start with `tool_` prefix.

#### 3b. Add the tool definition to the TOOLS list:

```python
TOOLS = [
    # ... existing tools ...
    {
        "name": "my_new_test",
        "description": "Description shown to Cursor AI when selecting tools.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "my_param": {"type": "integer", "description": "Parameter description", "default": 1}
            },
            "required": []  # List required parameters here
        },
        "handler": tool_my_new_test
    },
]
```

**Important:** Both the handler function AND the TOOLS entry are required!

### Step 4: Restart Services

After adding a new tool:

1. **Reload Blender addon** (F8) - picks up operator and server handler changes
2. **Restart MCP server** - picks up new tool definitions

## Tool Naming Conventions

- Function names: `tool_<action>_<target>` (e.g., `tool_run_coon_patch_test`)
- Command names: `<action>_<target>` (e.g., `run_test`)
- Operator IDs: `procedural.<action>_<target>` (e.g., `procedural.run_full_coon_test`)

## Common Patterns

### Returning Test Results

```python
# In blender_server.py handler:
return {
    "success": failed == 0,
    "passed": passed,
    "failed": failed,
    "total": total,
}
```

### Getting Data from Scene

```python
# Store results in scene for access
context.scene["my_test_result"] = some_value

# Read from handler
result = bpy.context.scene.get("my_test_result", default_value)
```

### Error Handling

Always wrap operator calls in try/except and return structured errors:

```python
try:
    result = bpy.ops.procedural.my_test()
    return {"success": True, ...}
except Exception as e:
    return {
        "success": False,
        "error": str(e),
        "traceback": traceback.format_exc()
    }
```

## Debugging Tips

1. Check Blender's system console for server logs
2. Use `tool_get_point_data(point_id)` to inspect specific vertices
3. Add debug attributes in geometry nodes and export them via CSV
