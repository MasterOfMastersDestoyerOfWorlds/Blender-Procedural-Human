"""
Topology Checker for Coon/Charrot-Gregory Patch Geometry Nodes

Analyzes exported CSV data to detect "star patterns" and other topology errors
in the generated mesh. A star pattern occurs when corner points connect to
distant points on the opposite side of the face instead of adjacent grid points.

Usage:
    from procedural_human.testing import check_corner_topology, check_all_corners
    result = check_corner_topology(
        point_csv="path/to/points.csv",
        edge_csv="path/to/edges.csv",
        corner_point_id=13
    )
    print(result.passed, result.message)
    results = check_all_corners(point_csv, edge_csv)
    for r in results:
        print(f"Point {r.corner_id}: {'PASS' if r.passed else 'FAIL'} - {r.message}")
"""

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class PointData:
    """Data for a single point from the CSV export."""
    id: int
    position: Tuple[float, float, float]
    debug_orig_face_idx: int = -1
    debug_orig_loop_start: int = -1
    debug_flip_domain: bool = False
    debug_on_edge: bool = False
    debug_domain_x: float = 0.0
    debug_domain_y: float = 0.0
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EdgeData:
    """Data for a single edge from the CSV export."""
    id: int
    vert_x: int  # First vertex index
    vert_y: int  # Second vertex index
    crease: float = 0.0
    selected: bool = False
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TopologyCheckResult:
    """Result of a topology check for a corner point."""
    passed: bool
    corner_id: int
    message: str
    connected_points: List[int] = field(default_factory=list)
    distances: List[float] = field(default_factory=list)
    expected_max_distance: float = 0.0
    actual_max_distance: float = 0.0
    star_pattern_detected: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


def load_point_csv(csv_path: str) -> Dict[int, PointData]:
    """
    Load point data from a CSV file.
    
    Args:
        csv_path: Path to the point CSV file
        
    Returns:
        Dictionary mapping point ID to PointData
    """
    points = {}
    path = Path(csv_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Point CSV not found: {csv_path}")
    
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        
        for row_idx, row in enumerate(reader):
            point_id = row_idx
            if 'debug_point_index' in row:
                try:
                    point_id = int(row['debug_point_index'])
                except (ValueError, TypeError):
                    pass
            try:
                position = (
                    float(row.get('Position_X', 0)),
                    float(row.get('Position_Y', 0)),
                    float(row.get('Position_Z', 0))
                )
            except (ValueError, TypeError):
                position = (0.0, 0.0, 0.0)
            debug_orig_face_idx = int(row.get('debug_orig_face_idx', -1)) if row.get('debug_orig_face_idx') else -1
            debug_orig_loop_start = int(row.get('debug_orig_loop_start', -1)) if row.get('debug_orig_loop_start') else -1
            debug_flip = row.get('debug_flip_domain', 'False')
            debug_flip_domain = debug_flip.lower() == 'true' if isinstance(debug_flip, str) else bool(debug_flip)
            
            debug_edge = row.get('debug_on_edge', 'False')
            debug_on_edge = debug_edge.lower() == 'true' if isinstance(debug_edge, str) else bool(debug_edge)
            debug_domain_x = float(row.get('debug_domain_x', 0)) if row.get('debug_domain_x') else 0.0
            debug_domain_y = float(row.get('debug_domain_y', 0)) if row.get('debug_domain_y') else 0.0
            
            points[point_id] = PointData(
                id=point_id,
                position=position,
                debug_orig_face_idx=debug_orig_face_idx,
                debug_orig_loop_start=debug_orig_loop_start,
                debug_flip_domain=debug_flip_domain,
                debug_on_edge=debug_on_edge,
                debug_domain_x=debug_domain_x,
                debug_domain_y=debug_domain_y,
                raw_data=dict(row)
            )
    
    return points


def load_edge_csv(csv_path: str) -> Dict[int, EdgeData]:
    """
    Load edge data from a CSV file.
    
    Args:
        csv_path: Path to the edge CSV file
        
    Returns:
        Dictionary mapping edge ID to EdgeData
    """
    edges = {}
    path = Path(csv_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Edge CSV not found: {csv_path}")
    
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        
        for row_idx, row in enumerate(reader):
            edge_id = row_idx
            vert_x = None
            vert_y = None
            if '.edge_verts_X' in row:
                vert_x = int(row['.edge_verts_X'])
                vert_y = int(row['.edge_verts_Y'])
            elif 'edge_verts_X' in row:
                vert_x = int(row['edge_verts_X'])
                vert_y = int(row['edge_verts_Y'])
            elif 'vert0_index' in row:
                vert_x = int(row['vert0_index'])
                vert_y = int(row['vert1_index'])
            
            if vert_x is None or vert_y is None:
                continue
            crease = float(row.get('crease', 0)) if row.get('crease') else 0.0
            
            selected = row.get('.select_edge', 'False')
            selected = selected.lower() == 'true' if isinstance(selected, str) else bool(selected)
            
            edges[edge_id] = EdgeData(
                id=edge_id,
                vert_x=vert_x,
                vert_y=vert_y,
                crease=crease,
                selected=selected,
                raw_data=dict(row)
            )
    
    return edges


def distance_3d(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt(
        (p1[0] - p2[0])**2 +
        (p1[1] - p2[1])**2 +
        (p1[2] - p2[2])**2
    )


def find_connected_points(point_id: int, edges: Dict[int, EdgeData]) -> List[Tuple[int, int]]:
    """
    Find all points connected to the given point via edges.
    
    Args:
        point_id: The point to find connections for
        edges: Dictionary of edge data
        
    Returns:
        List of tuples (connected_point_id, edge_id)
    """
    connected = []
    
    for edge_id, edge in edges.items():
        if edge.vert_x == point_id:
            connected.append((edge.vert_y, edge_id))
        elif edge.vert_y == point_id:
            connected.append((edge.vert_x, edge_id))
    
    return connected


def find_corner_points(points: Dict[int, PointData], edges: Dict[int, EdgeData]) -> List[int]:
    """
    Find points that are likely mesh corners (original cube vertices).
    
    Corner points are identified by:
    1. Having integer coordinates (on original mesh)
    2. Being on a domain edge (debug_on_edge=True) with debug_minD=0
    3. Having position at exactly +/-1 on each axis (for a unit cube)
    
    Args:
        points: Dictionary of point data
        edges: Dictionary of edge data
        
    Returns:
        List of corner point IDs
    """
    corners = []
    
    for point_id, point in points.items():
        pos = point.position
        is_corner = True
        for coord in pos:
            if abs(abs(coord) - 1.0) > 0.01:  # Allow small tolerance
                is_corner = False
                break
        
        if is_corner:
            corners.append(point_id)
    
    return corners


def analyze_star_pattern(
    corner_point: PointData,
    connected_points: List[PointData],
    expected_edge_length: float = 2.0,  # For unit cube, edge length is 2
    subdivisions: int = 2
) -> Tuple[bool, str, float]:
    """
    Analyze if connected points form a star pattern (diagonal connections).
    
    For a properly subdivided mesh, connected points should be at most
    edge_length / subdivisions away. If any connected point is more than
    2 * edge_length away, it's likely a diagonal (star pattern).
    
    Args:
        corner_point: The corner point being analyzed
        connected_points: List of points connected to the corner
        expected_edge_length: Expected length of original mesh edges
        subdivisions: Number of subdivision levels applied
        
    Returns:
        Tuple of (is_star_pattern, explanation, max_distance_found)
    """
    if not connected_points:
        return False, "No connected points", 0.0
    grid_step = expected_edge_length / (2 ** subdivisions)
    expected_max = grid_step * 1.5  # Allow some tolerance
    diagonal_threshold = expected_edge_length * 0.8  # ~80% of edge length
    
    max_distance = 0.0
    diagonal_points = []
    
    corner_pos = corner_point.position
    
    for connected in connected_points:
        dist = distance_3d(corner_pos, connected.position)
        max_distance = max(max_distance, dist)
        
        if dist > diagonal_threshold:
            diagonal_points.append((connected.id, dist))
    
    if diagonal_points:
        diag_str = ", ".join([f"point {pid} (dist={d:.3f})" for pid, d in diagonal_points])
        return True, f"Star pattern detected! Diagonal connections to: {diag_str}", max_distance
    
    if max_distance > expected_max:
        return False, f"Max distance {max_distance:.3f} > expected {expected_max:.3f}, but not clearly diagonal", max_distance
    
    return False, f"All connections within expected range (max={max_distance:.3f})", max_distance


def check_corner_topology(
    point_csv: str,
    edge_csv: str,
    corner_point_id: int,
    expected_edge_length: float = 2.0,
    subdivisions: int = 2
) -> TopologyCheckResult:
    """
    Check if a corner point has correct topology (no star pattern).
    
    Args:
        point_csv: Path to the point CSV file
        edge_csv: Path to the edge CSV file
        corner_point_id: ID of the corner point to check
        expected_edge_length: Expected length of original mesh edges
        subdivisions: Number of subdivision levels
        
    Returns:
        TopologyCheckResult with pass/fail and details
    """
    points = load_point_csv(point_csv)
    edges = load_edge_csv(edge_csv)
    
    if corner_point_id not in points:
        return TopologyCheckResult(
            passed=False,
            corner_id=corner_point_id,
            message=f"Corner point {corner_point_id} not found in CSV",
            star_pattern_detected=False
        )
    
    corner_point = points[corner_point_id]
    connected_info = find_connected_points(corner_point_id, edges)
    connected_point_ids = [pid for pid, _ in connected_info]
    connected_edge_ids = [eid for _, eid in connected_info]
    
    if not connected_info:
        return TopologyCheckResult(
            passed=False,
            corner_id=corner_point_id,
            message=f"Corner point {corner_point_id} has no connected edges",
            star_pattern_detected=False
        )
    connected_points = []
    for pid in connected_point_ids:
        if pid in points:
            connected_points.append(points[pid])
    distances = []
    for cp in connected_points:
        dist = distance_3d(corner_point.position, cp.position)
        distances.append(dist)
    is_star, explanation, max_dist = analyze_star_pattern(
        corner_point, connected_points, expected_edge_length, subdivisions
    )
    
    grid_step = expected_edge_length / (2 ** subdivisions)
    expected_max = grid_step * 1.5
    details = {
        "corner_position": corner_point.position,
        "corner_face_idx": corner_point.debug_orig_face_idx,
        "corner_flip_domain": corner_point.debug_flip_domain,
        "corner_domain_pos": (corner_point.debug_domain_x, corner_point.debug_domain_y),
        "connected_edges": connected_edge_ids,
        "connected_positions": [cp.position for cp in connected_points],
        "connected_faces": [cp.debug_orig_face_idx for cp in connected_points],
    }
    
    return TopologyCheckResult(
        passed=not is_star,
        corner_id=corner_point_id,
        message=explanation,
        connected_points=connected_point_ids,
        distances=distances,
        expected_max_distance=expected_max,
        actual_max_distance=max_dist,
        star_pattern_detected=is_star,
        details=details
    )


def check_all_corners(
    point_csv: str,
    edge_csv: str,
    expected_edge_length: float = 2.0,
    subdivisions: int = 2
) -> List[TopologyCheckResult]:
    """
    Check topology for all corner points in the mesh.
    
    Args:
        point_csv: Path to the point CSV file
        edge_csv: Path to the edge CSV file
        expected_edge_length: Expected length of original mesh edges
        subdivisions: Number of subdivision levels
        
    Returns:
        List of TopologyCheckResult for each corner
    """
    points = load_point_csv(point_csv)
    edges = load_edge_csv(edge_csv)
    
    corners = find_corner_points(points, edges)
    
    results = []
    for corner_id in corners:
        result = check_corner_topology(
            point_csv, edge_csv, corner_id,
            expected_edge_length, subdivisions
        )
        results.append(result)
    
    return results


def get_latest_csvs(tmp_dir: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Find the latest point and edge CSV files in the tmp directory.
    
    Args:
        tmp_dir: Path to the tmp directory
        
    Returns:
        Tuple of (point_csv_path, edge_csv_path) or (None, None) if not found
    """
    tmp_path = Path(tmp_dir)
    
    if not tmp_path.exists():
        return None, None
    point_csvs = list(tmp_path.glob("spreadsheet_*_MESH_POINT_*.csv"))
    edge_csvs = list(tmp_path.glob("spreadsheet_*_MESH_EDGE_*.csv"))
    
    if not point_csvs or not edge_csvs:
        return None, None
    point_csvs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    edge_csvs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    
    return str(point_csvs[0]), str(edge_csvs[0])


def run_quick_check(tmp_dir: str = None) -> Dict[str, Any]:
    """
    Run a quick topology check on the latest CSV files.
    
    Args:
        tmp_dir: Path to tmp directory (defaults to procedural_human/tmp)
        
    Returns:
        Dictionary with check results
    """
    if tmp_dir is None:
        from pathlib import Path
        current = Path(__file__).parent.parent
        tmp_dir = str(current / "tmp")
    
    point_csv, edge_csv = get_latest_csvs(tmp_dir)
    
    if not point_csv or not edge_csv:
        return {
            "success": False,
            "error": f"Could not find CSV files in {tmp_dir}",
            "point_csv": None,
            "edge_csv": None,
        }
    
    results = check_all_corners(point_csv, edge_csv)
    
    passed_count = sum(1 for r in results if r.passed)
    failed_count = len(results) - passed_count
    
    failed_corners = [r for r in results if not r.passed]
    
    return {
        "success": failed_count == 0,
        "point_csv": point_csv,
        "edge_csv": edge_csv,
        "total_corners": len(results),
        "passed": passed_count,
        "failed": failed_count,
        "failed_corners": [
            {
                "corner_id": r.corner_id,
                "message": r.message,
                "connected_points": r.connected_points,
                "max_distance": r.actual_max_distance,
            }
            for r in failed_corners
        ],
        "all_results": [
            {
                "corner_id": r.corner_id,
                "passed": r.passed,
                "message": r.message,
            }
            for r in results
        ]
    }


if __name__ == "__main__":
    import json
    result = run_quick_check()
    print(json.dumps(result, indent=2, default=str))
