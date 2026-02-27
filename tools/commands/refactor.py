"""CLI commands for codebase refactoring: list-symbols, move-symbol."""

from __future__ import annotations

import ast
from pathlib import Path

from tools.cli_registry import cli_command

REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_path(rel_path: str) -> Path:
    """Resolve a user-supplied path relative to the repo root."""
    candidate = Path(rel_path)
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def _collect_symbols(tree: ast.Module) -> list[dict]:
    """Walk top-level AST nodes and collect classes and functions."""
    symbols: list[dict] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append({
                        "name": item.name,
                        "line": item.lineno,
                        "end_line": item.end_lineno,
                        "decorators": [ast.dump(d) for d in item.decorator_list],
                    })
            symbols.append({
                "type": "class",
                "name": node.name,
                "line": node.lineno,
                "end_line": node.end_lineno,
                "decorators": [ast.dump(d) for d in node.decorator_list],
                "methods": methods,
                "bases": [ast.unparse(b) for b in node.bases],
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append({
                "type": "function",
                "name": node.name,
                "line": node.lineno,
                "end_line": node.end_lineno,
                "decorators": [ast.dump(d) for d in node.decorator_list],
            })
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = []
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        targets.append(t.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets.append(node.target.id)
            for name in targets:
                if name.isupper() or name.startswith("_") and name[1:].isupper():
                    symbols.append({
                        "type": "constant",
                        "name": name,
                        "line": node.lineno,
                        "end_line": node.end_lineno,
                    })
    return symbols


@cli_command
def list_symbols(file: str) -> dict:
    """List all top-level classes, functions, and constants in a Python file.

    :param file: Path to the Python file (relative to repo root or absolute).
    """
    path = _resolve_path(file)
    if not path.exists():
        return {"ok": False, "error": f"File not found: {path}"}
    if not path.suffix == ".py":
        return {"ok": False, "error": f"Not a Python file: {path}"}

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return {"ok": False, "error": f"Syntax error: {exc}"}

    symbols = _collect_symbols(tree)
    total_lines = len(source.splitlines())

    return {
        "ok": True,
        "file": str(path.relative_to(REPO_ROOT)),
        "total_lines": total_lines,
        "symbol_count": len(symbols),
        "symbols": symbols,
    }


@cli_command
def move_symbol(source: str, symbol: str, dest: str) -> dict:
    """Move a top-level class or function to another file, updating imports project-wide.

    Uses the rope refactoring library for safe, AST-aware moves.

    :param source: Source file path (relative to repo root or absolute).
    :param symbol: Name of the class or function to move.
    :param dest: Destination file path (relative to repo root or absolute).
    """
    try:
        import rope.base.project
        from rope.base import libutils
        from rope.refactor.move import MoveGlobal
    except ImportError:
        return {
            "ok": False,
            "error": "rope is not installed. Run: uv pip install rope",
        }

    source_path = _resolve_path(source)
    dest_path = _resolve_path(dest)

    if not source_path.exists():
        return {"ok": False, "error": f"Source file not found: {source_path}"}
    if source_path == dest_path:
        return {"ok": False, "error": "Source and destination are the same file."}

    source_rel = str(source_path.relative_to(REPO_ROOT))
    dest_rel = str(dest_path.relative_to(REPO_ROOT))

    project = rope.base.project.Project(str(REPO_ROOT))
    try:
        source_resource = libutils.path_to_resource(project, source_rel)
        source_code = source_resource.read()

        offset = _find_symbol_offset(source_code, symbol)
        if offset == -1:
            return {
                "ok": False,
                "error": f"Symbol '{symbol}' not found in {source_rel}",
            }

        if not dest_path.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text("", encoding="utf-8")

        dest_resource = libutils.path_to_resource(project, dest_rel)
        mover = MoveGlobal(project, source_resource, offset)
        changes = mover.get_changes(dest_resource)

        changed_files = []
        for change in changes.changes:
            changed_files.append(change.resource.path)

        project.do(changes)

        return {
            "ok": True,
            "symbol": symbol,
            "source": source_rel,
            "destination": dest_rel,
            "files_changed": sorted(changed_files),
        }
    except Exception as exc:
        return {"ok": False, "error": f"Refactoring failed: {exc}"}
    finally:
        project.close()


def _find_symbol_offset(source: str, symbol: str) -> int:
    """Find the character offset of a top-level symbol using AST for accuracy."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return -1

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == symbol:
                lines = source.splitlines(keepends=True)
                offset = sum(len(lines[i]) for i in range(node.lineno - 1))
                keyword = "class " if isinstance(node, ast.ClassDef) else "def "
                line = lines[node.lineno - 1]
                col = line.find(keyword + symbol)
                if col != -1:
                    return offset + col + len(keyword)
                return offset
    return -1
