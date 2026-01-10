#!/usr/bin/env python
"""
Standalone MCP Server for Blender Testing

This script runs OUTSIDE of Blender and communicates with the Blender HTTP server.
It doesn't import any Blender-specific modules.

Usage:
    python mcp_server_standalone.py
    python mcp_server_standalone.py --test
"""

import json
import sys
import asyncio
import urllib.request
import urllib.error
from typing import Any, Dict, Optional
from dataclasses import dataclass


# Blender server URL
BLENDER_URL = "http://localhost:9876"


# ============================================================================
# BLENDER CLIENT
# ============================================================================

class BlenderClient:
    """Client for communicating with the Blender HTTP server."""
    
    def __init__(self, base_url: str = BLENDER_URL):
        self.base_url = base_url.rstrip("/")
    
    def send_command_sync(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command synchronously."""
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
            return {"success": False, "error": f"Connection failed: {e}. Is Blender running with the test server?"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def send_command(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.send_command_sync, action, params)
    
    def check_health_sync(self) -> bool:
        """Check if Blender server is running."""
        try:
            req = urllib.request.Request(f"{self.base_url}/health")
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except:
            return False
    
    async def check_health(self) -> bool:
        """Check health asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.check_health_sync)


# Global client
_client = BlenderClient()


# ============================================================================
# MCP TOOL HANDLERS
# ============================================================================

async def tool_run_coon_patch_test(subdivisions: int = 2, create_new_cube: bool = True, subdivide_edge: bool = False) -> Dict[str, Any]:
    """Run the full Coon/Charrot-Gregory patch test cycle."""
    return await _client.send_command("run_test", {
        "subdivisions": subdivisions,
        "create_new_cube": create_new_cube,
        "subdivide_edge": subdivide_edge
    })


async def tool_run_pentagon_test(subdivisions: int = 2) -> Dict[str, Any]:
    """Run Coon patch test with pentagon faces (5-sided N-gons)."""
    return await _client.send_command("run_test", {
        "subdivisions": subdivisions,
        "create_new_cube": True,
        "subdivide_edge": True
    })


async def tool_get_point_data(point_id: int) -> Dict[str, Any]:
    """Get detailed data for a specific point/vertex."""
    return await _client.send_command("get_point_data", {"point_id": point_id})


async def tool_check_corner_topology(corner_id: int, subdivisions: int = 2, edge_length: float = 2.0) -> Dict[str, Any]:
    """Check if a corner point has correct topology (no star pattern)."""
    return await _client.send_command("check_corner", {
        "corner_id": corner_id,
        "subdivisions": subdivisions,
        "edge_length": edge_length
    })


async def tool_get_csv_data(include_points: bool = False, include_edges: bool = False) -> Dict[str, Any]:
    """Get information about the latest CSV exports."""
    return await _client.send_command("get_csv_data", {
        "include_points": include_points,
        "include_edges": include_edges
    })


async def tool_verify_topology() -> Dict[str, Any]:
    """Verify topology of all corners in the generated mesh."""
    return await _client.send_command("verify_topology", {})


async def tool_setup_test(subdivisions: int = 2, use_existing_cube: bool = True) -> Dict[str, Any]:
    """Setup a test scene with cube and geometry node."""
    return await _client.send_command("setup_test", {
        "subdivisions": subdivisions,
        "use_existing_cube": use_existing_cube
    })


async def tool_apply_and_export(apply_modifier: bool = True, export_points: bool = True, export_edges: bool = True) -> Dict[str, Any]:
    """Apply geometry node modifier and export CSV data."""
    return await _client.send_command("apply_export", {
        "apply_modifier": apply_modifier,
        "export_points": export_points,
        "export_edges": export_edges
    })


async def tool_ping() -> Dict[str, Any]:
    """Check if the Blender server is running."""
    healthy = await _client.check_health()
    if healthy:
        return {"success": True, "message": "Blender server is running"}
    return {
        "success": False,
        "error": "Cannot connect to Blender server. Make sure Blender is running with the addon loaded."
    }


# Tool definitions for MCP
TOOLS = [
    {
        "name": "run_coon_patch_test",
        "description": "Run the full Coon/Charrot-Gregory patch test cycle. Returns pass/fail and topology analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subdivisions": {"type": "integer", "description": "Number of subdivisions (1-5)", "default": 2},
                "create_new_cube": {"type": "boolean", "description": "Create a fresh cube", "default": True},
                "subdivide_edge": {"type": "boolean", "description": "Subdivide one edge to create pentagon faces", "default": False}
            }
        },
        "handler": tool_run_coon_patch_test
    },
    {
        "name": "run_pentagon_test",
        "description": "Run Coon patch test with pentagon faces (5-sided N-gons). Creates a cube with one edge subdivided.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subdivisions": {"type": "integer", "description": "Number of subdivisions (1-5)", "default": 2}
            }
        },
        "handler": tool_run_pentagon_test
    },
    {
        "name": "get_point_data",
        "description": "Get detailed data for a specific mesh point/vertex including position, face, domain coords.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "point_id": {"type": "integer", "description": "Point ID (0-based)"}
            },
            "required": ["point_id"]
        },
        "handler": tool_get_point_data
    },
    {
        "name": "check_corner_topology",
        "description": "Check if a corner point has correct topology (no star pattern).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "corner_id": {"type": "integer", "description": "Corner point ID"},
                "subdivisions": {"type": "integer", "default": 2},
                "edge_length": {"type": "number", "default": 2.0}
            },
            "required": ["corner_id"]
        },
        "handler": tool_check_corner_topology
    },
    {
        "name": "get_csv_data",
        "description": "Get information about the latest CSV exports from Blender.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "include_points": {"type": "boolean", "default": False},
                "include_edges": {"type": "boolean", "default": False}
            }
        },
        "handler": tool_get_csv_data
    },
    {
        "name": "verify_topology",
        "description": "Verify topology of all corners - checks for star patterns.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_verify_topology
    },
    {
        "name": "setup_test",
        "description": "Setup test scene with cube and geometry node (without applying).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subdivisions": {"type": "integer", "default": 2},
                "use_existing_cube": {"type": "boolean", "default": True}
            }
        },
        "handler": tool_setup_test
    },
    {
        "name": "apply_and_export",
        "description": "Apply the geometry node modifier and export CSV data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "apply_modifier": {"type": "boolean", "default": True},
                "export_points": {"type": "boolean", "default": True},
                "export_edges": {"type": "boolean", "default": True}
            }
        },
        "handler": tool_apply_and_export
    },
    {
        "name": "ping_blender",
        "description": "Check if Blender server is running and responding.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_ping
    },
]

TOOL_MAP = {t["name"]: t["handler"] for t in TOOLS}


# ============================================================================
# MCP SERVER
# ============================================================================

class MCPServer:
    """MCP server using stdio transport."""
    
    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
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
                    "capabilities": {"tools": {}},
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
                        {"name": t["name"], "description": t["description"], "inputSchema": t["inputSchema"]}
                        for t in TOOLS
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name not in TOOL_MAP:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                }
            
            try:
                result = await TOOL_MAP[tool_name](**tool_args)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32000, "message": str(e)}
                }
        
        elif method == "notifications/initialized":
            return None
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Unknown method: {method}"}
        }
    
    async def run(self):
        """Run the MCP server on stdio."""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                request = json.loads(line)
                response = await self.handle_request(request)
                
                if response:
                    print(json.dumps(response), flush=True)
                    
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "error": {"code": -32000, "message": str(e)}
                }), flush=True)


# ============================================================================
# MAIN
# ============================================================================

async def test_connection():
    """Test the Blender connection."""
    print("Testing Blender connection...", file=sys.stderr)
    result = await tool_ping()
    print(f"Ping result: {json.dumps(result, indent=2)}", file=sys.stderr)
    
    if result.get("success"):
        print("\nRunning test...", file=sys.stderr)
        result = await tool_run_coon_patch_test(subdivisions=2)
        print(f"Test result: {json.dumps(result, indent=2)}", file=sys.stderr)


if __name__ == "__main__":
    if "--test" in sys.argv:
        asyncio.run(test_connection())
    else:
        server = MCPServer()
        asyncio.run(server.run())
