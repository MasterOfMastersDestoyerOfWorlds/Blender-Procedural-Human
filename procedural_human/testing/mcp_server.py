"""
MCP Server Bridge for Blender Testing

An MCP (Model Context Protocol) server that exposes Blender testing tools to Claude.
This server communicates with the Blender HTTP server to execute commands.

Setup:
    1. Start Blender and run: bpy.ops.procedural.start_test_server()
    2. Run this MCP server: python -m procedural_human.testing.mcp_server
    3. Configure Cursor to use this MCP server

MCP Tools Exposed:
    - run_coon_patch_test: Run full test cycle
    - get_point_data: Query point attributes
    - get_edge_data: Query edge connectivity
    - check_corner_topology: Verify specific corner
    - get_latest_csv: Read recent export data
"""

import json
import sys
import asyncio
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path
try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False
    import urllib.request
    import urllib.error
DEFAULT_BLENDER_URL = "http://localhost:9876"

class BlenderClient:
    """Client for communicating with the Blender HTTP server."""
    
    def __init__(self, base_url: str = DEFAULT_BLENDER_URL):
        self.base_url = base_url.rstrip("/")
    
    def _send_command_sync(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command synchronously using urllib."""
        url = f"{self.base_url}/command"
        data = json.dumps({
            "action": action,
            "params": params or {}
        }).encode()
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode())
        except urllib.error.URLError as e:
            return {"success": False, "error": f"Connection failed: {e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def send_command(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to the Blender server."""
        if HAS_HTTPX:
            async with httpx.AsyncClient(timeout=60.0) as client:
                try:
                    response = await client.post(
                        f"{self.base_url}/command",
                        json={"action": action, "params": params or {}}
                    )
                    return response.json()
                except httpx.ConnectError:
                    return {"success": False, "error": "Cannot connect to Blender server. Is it running?"}
                except Exception as e:
                    return {"success": False, "error": str(e)}
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, self._send_command_sync, action, params
            )
    
    async def check_health(self) -> bool:
        """Check if Blender server is running."""
        if HAS_HTTPX:
            async with httpx.AsyncClient(timeout=5.0) as client:
                try:
                    response = await client.get(f"{self.base_url}/health")
                    return response.status_code == 200
                except:
                    return False
        else:
            try:
                req = urllib.request.Request(f"{self.base_url}/health")
                with urllib.request.urlopen(req, timeout=5) as response:
                    return response.status == 200
            except:
                return False
_client: Optional[BlenderClient] = None


def get_client() -> BlenderClient:
    """Get the Blender client instance."""
    global _client
    if _client is None:
        _client = BlenderClient()
    return _client

@dataclass
class MCPTool:
    """Definition of an MCP tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: callable


async def tool_run_coon_patch_test(
    subdivisions: int = 2,
    create_new_cube: bool = True,
    subdivide_edge: bool = False
) -> Dict[str, Any]:
    """
    Run the full Coon/Charrot-Gregory patch test cycle.
    
    This will:
    1. Create or use a cube mesh
    2. Initialize bezier handles
    3. Optionally subdivide an edge to create pentagon faces
    4. Add the CoonNGonPatchGenerator geometry node
    5. Apply the modifier
    6. Export point and edge data to CSV
    7. Verify topology for star patterns
    
    Args:
        subdivisions: Number of subdivisions (1-5, default 2)
        create_new_cube: Whether to create a fresh cube (default True)
        subdivide_edge: Whether to subdivide an edge to create pentagon faces (default False)
    
    Returns:
        Test results including pass/fail status and details
    """
    client = get_client()
    return await client.send_command("run_test", {
        "subdivisions": subdivisions,
        "create_new_cube": create_new_cube,
        "subdivide_edge": subdivide_edge
    })


async def tool_run_pentagon_test(
    subdivisions: int = 2
) -> Dict[str, Any]:
    """
    Run Coon patch test with pentagon faces (5-sided N-gons).
    
    Creates a cube with one edge subdivided, resulting in two pentagon faces.
    This tests N-gon support beyond simple quads.
    
    Args:
        subdivisions: Number of subdivisions (1-5, default 2)
    
    Returns:
        Test results including pass/fail status and details
    """
    client = get_client()
    return await client.send_command("run_test", {
        "subdivisions": subdivisions,
        "create_new_cube": True,
        "subdivide_edge": True
    })


async def tool_get_point_data(point_id: int) -> Dict[str, Any]:
    """
    Get detailed data for a specific point/vertex.
    
    Args:
        point_id: The ID of the point to query (0-based index)
    
    Returns:
        Point data including position, face index, domain position, etc.
    """
    client = get_client()
    return await client.send_command("get_point_data", {"point_id": point_id})


async def tool_check_corner_topology(
    corner_id: int,
    subdivisions: int = 2,
    edge_length: float = 2.0
) -> Dict[str, Any]:
    """
    Check if a corner point has correct topology (no star pattern).
    
    A star pattern occurs when a corner point connects to distant points
    on the opposite side of the face instead of adjacent grid points.
    
    Args:
        corner_id: The ID of the corner point to check
        subdivisions: Number of subdivisions used (for distance calculation)
        edge_length: Expected edge length of original mesh (default 2.0 for unit cube)
    
    Returns:
        Check results including pass/fail, connected points, and distances
    """
    client = get_client()
    return await client.send_command("check_corner", {
        "corner_id": corner_id,
        "subdivisions": subdivisions,
        "edge_length": edge_length
    })


async def tool_get_csv_data(
    include_points: bool = False,
    include_edges: bool = False
) -> Dict[str, Any]:
    """
    Get information about the latest CSV exports.
    
    Args:
        include_points: Include point data in response (can be large)
        include_edges: Include edge data in response (can be large)
    
    Returns:
        CSV file paths and optionally the data
    """
    client = get_client()
    return await client.send_command("get_csv_data", {
        "include_points": include_points,
        "include_edges": include_edges
    })


async def tool_verify_topology() -> Dict[str, Any]:
    """
    Verify topology of all corners in the generated mesh.
    
    This checks all corner points for star patterns and returns
    a summary of pass/fail results.
    
    Returns:
        Verification results for all corners
    """
    client = get_client()
    return await client.send_command("verify_topology", {})


async def tool_setup_test(
    subdivisions: int = 2,
    use_existing_cube: bool = True
) -> Dict[str, Any]:
    """
    Setup a test scene without applying the modifier.
    
    This creates/selects a cube, initializes handles, and adds
    the geometry node modifier.
    
    Args:
        subdivisions: Number of subdivisions to set
        use_existing_cube: Use existing selection instead of creating new
    
    Returns:
        Setup status
    """
    client = get_client()
    return await client.send_command("setup_test", {
        "subdivisions": subdivisions,
        "use_existing_cube": use_existing_cube
    })


async def tool_apply_and_export(
    apply_modifier: bool = True,
    export_points: bool = True,
    export_edges: bool = True
) -> Dict[str, Any]:
    """
    Apply the geometry node modifier and export CSV data.
    
    Args:
        apply_modifier: Whether to apply the modifier
        export_points: Export point/vertex data
        export_edges: Export edge data
    
    Returns:
        Export status
    """
    client = get_client()
    return await client.send_command("apply_export", {
        "apply_modifier": apply_modifier,
        "export_points": export_points,
        "export_edges": export_edges
    })


async def tool_ping() -> Dict[str, Any]:
    """
    Check if the Blender server is running and responding.
    
    Returns:
        Connection status
    """
    client = get_client()
    healthy = await client.check_health()
    if healthy:
        return {"success": True, "message": "Blender server is running"}
    else:
        return {
            "success": False,
            "error": "Cannot connect to Blender server. "
                    "Make sure Blender is running and execute: "
                    "bpy.ops.procedural.start_test_server()"
        }
MCP_TOOLS = [
    MCPTool(
        name="run_coon_patch_test",
        description="Run the full Coon/Charrot-Gregory patch test cycle",
        input_schema={
            "type": "object",
            "properties": {
                "subdivisions": {
                    "type": "integer",
                    "description": "Number of subdivisions (1-5)",
                    "default": 2
                },
                "create_new_cube": {
                    "type": "boolean",
                    "description": "Create a fresh cube for testing",
                    "default": True
                }
            }
        },
        handler=tool_run_coon_patch_test
    ),
    MCPTool(
        name="get_point_data",
        description="Get detailed data for a specific mesh point/vertex",
        input_schema={
            "type": "object",
            "properties": {
                "point_id": {
                    "type": "integer",
                    "description": "The point ID to query (0-based)"
                }
            },
            "required": ["point_id"]
        },
        handler=tool_get_point_data
    ),
    MCPTool(
        name="check_corner_topology",
        description="Check if a corner point has correct topology (no star pattern)",
        input_schema={
            "type": "object",
            "properties": {
                "corner_id": {
                    "type": "integer",
                    "description": "The corner point ID to check"
                },
                "subdivisions": {
                    "type": "integer",
                    "description": "Number of subdivisions used",
                    "default": 2
                },
                "edge_length": {
                    "type": "number",
                    "description": "Expected edge length of original mesh",
                    "default": 2.0
                }
            },
            "required": ["corner_id"]
        },
        handler=tool_check_corner_topology
    ),
    MCPTool(
        name="get_csv_data",
        description="Get information about the latest CSV exports",
        input_schema={
            "type": "object",
            "properties": {
                "include_points": {
                    "type": "boolean",
                    "description": "Include point data in response",
                    "default": False
                },
                "include_edges": {
                    "type": "boolean",
                    "description": "Include edge data in response",
                    "default": False
                }
            }
        },
        handler=tool_get_csv_data
    ),
    MCPTool(
        name="verify_topology",
        description="Verify topology of all corners in the generated mesh",
        input_schema={"type": "object", "properties": {}},
        handler=tool_verify_topology
    ),
    MCPTool(
        name="setup_test",
        description="Setup a test scene with cube and geometry node",
        input_schema={
            "type": "object",
            "properties": {
                "subdivisions": {
                    "type": "integer",
                    "description": "Number of subdivisions",
                    "default": 2
                },
                "use_existing_cube": {
                    "type": "boolean",
                    "description": "Use existing cube selection",
                    "default": True
                }
            }
        },
        handler=tool_setup_test
    ),
    MCPTool(
        name="apply_and_export",
        description="Apply geometry node modifier and export CSV data",
        input_schema={
            "type": "object",
            "properties": {
                "apply_modifier": {
                    "type": "boolean",
                    "description": "Apply the modifier",
                    "default": True
                },
                "export_points": {
                    "type": "boolean",
                    "description": "Export point data",
                    "default": True
                },
                "export_edges": {
                    "type": "boolean",
                    "description": "Export edge data",
                    "default": True
                }
            }
        },
        handler=tool_apply_and_export
    ),
    MCPTool(
        name="ping_blender",
        description="Check if the Blender server is running",
        input_schema={"type": "object", "properties": {}},
        handler=tool_ping
    ),
]

class MCPServer:
    """Simple MCP server implementation using stdio transport."""
    
    def __init__(self):
        self.tools = {t.name: t for t in MCP_TOOLS}
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "blender-coon-patch-tester",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": t.name,
                            "description": t.description,
                            "inputSchema": t.input_schema
                        }
                        for t in MCP_TOOLS
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
            
            tool = self.tools[tool_name]
            
            try:
                result = await tool.handler(**tool_args)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2, default=str)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32000,
                        "message": str(e)
                    }
                }
        
        elif method == "notifications/initialized":
            return None
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }
    
    async def run_stdio(self):
        """Run the server using stdio transport."""
        print("Blender Coon Patch Tester MCP Server", file=sys.stderr)
        print("Waiting for requests on stdin...", file=sys.stderr)
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    continue
                response = await self.handle_request(request)
                if response is not None:
                    print(json.dumps(response), flush=True)
                    
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)


async def main():
    """Main entry point for the MCP server."""
    server = MCPServer()
    await server.run_stdio()

async def test_tools():
    """Test the tools outside of MCP context."""
    print("Testing Blender connection...")
    result = await tool_ping()
    print(f"Ping: {result}")
    
    if not result.get("success"):
        print("\nBlender server not running. Start it with:")
        print("  bpy.ops.procedural.start_test_server()")
        return
    print("\nRunning Coon patch test...")
    result = await tool_run_coon_patch_test(subdivisions=2, create_new_cube=True)
    print(f"Test result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Blender Coon Patch Tester MCP Server")
    parser.add_argument("--test", action="store_true", help="Run standalone test")
    parser.add_argument("--blender-url", default=DEFAULT_BLENDER_URL, 
                       help="Blender server URL")
    
    args = parser.parse_args()
    _client = BlenderClient(args.blender_url)
    
    if args.test:
        asyncio.run(test_tools())
    else:
        asyncio.run(main())
