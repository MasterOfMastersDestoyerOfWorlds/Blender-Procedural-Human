"""
Procedural Human Testing Module

Provides automated testing infrastructure for geometry node validation,
including CSV-based topology verification and MCP integration.
"""

from .topology_checker import (
    TopologyCheckResult,
    check_corner_topology,
    check_all_corners,
    load_point_csv,
    load_edge_csv,
    find_corner_points,
    analyze_star_pattern,
    run_quick_check,
    get_latest_csvs,
)

# Note: test_operators are auto-registered via @procedural_operator decorator
# They will be available when loaded in Blender

__all__ = [
    # Topology checker
    "TopologyCheckResult",
    "check_corner_topology",
    "check_all_corners",
    "load_point_csv",
    "load_edge_csv",
    "find_corner_points",
    "analyze_star_pattern",
    "run_quick_check",
    "get_latest_csvs",
]
