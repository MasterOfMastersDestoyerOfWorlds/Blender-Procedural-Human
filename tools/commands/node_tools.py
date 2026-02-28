"""CLI commands for node group development: open, export, list-groups, inspect, diff, promote."""

from __future__ import annotations

import shutil
from pathlib import Path

from tools.cli_registry import cli_command
from tools.commands.common import BlenderClient

REPO_ROOT = Path(__file__).resolve().parents[2]


@cli_command
def open(client: BlenderClient, filepath: str) -> dict:
    """Open a .blend file in the running Blender instance.

    :param client: Blender HTTP client.
    :param filepath: Absolute path to the .blend file to open.
    """
    result = client.command("open_file", {"filepath": filepath})
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def list_groups(client: BlenderClient) -> dict:
    """List all registered geo_node_group functions and Blender node groups.

    :param client: Blender HTTP client.
    """
    result = client.command("list_groups", {})
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def inspect(client: BlenderClient, group: str) -> dict:
    """Inspect a node group's structure: nodes, links, interface, frames.

    :param client: Blender HTTP client.
    :param group: Name of the node group to inspect.
    """
    result = client.command("inspect_group", {"group": group})
    result["ok"] = bool(result.get("success"))
    return result


_EXPORT_NOISE_KEYS = {"helpers_used", "code", "full_code", "generated_code"}


@cli_command
def export(client: BlenderClient, group: str, use_helpers: bool = True,
           split_frames: bool = False, include_labels: bool = True,
           include_locations: bool = False, include_names: bool = False,
           verbose: bool = False) -> dict:
    """Export a node group to Python via the node exporter.

    :param client: Blender HTTP client.
    :param group: Name of the node group to export.
    :param use_helpers: Substitute node_helpers where patterns match.
    :param split_frames: Split top-level frames into separate files.
    :param include_labels: Include node labels in output.
    :param include_locations: Include node locations in output.
    :param include_names: Include node names in output.
    :param verbose: Include all fields (helpers_used, full code) in output.
    """
    result = client.command("export_group", {
        "group": group,
        "use_helpers": use_helpers,
        "split_frames": split_frames,
        "include_labels": include_labels,
        "include_locations": include_locations,
        "include_names": include_names,
    })
    result["ok"] = bool(result.get("success"))

    if not verbose:
        for key in _EXPORT_NOISE_KEYS:
            result.pop(key, None)
        files = result.get("files")
        if isinstance(files, dict):
            result["files"] = sorted(files.keys())
            result["file_count"] = len(result["files"])

    return result


@cli_command
def diff(client: BlenderClient, group: str, baseline: str = "",
         save: str = "") -> dict:
    """Compare mesh metrics of a node group, optionally against a baseline.

    :param client: Blender HTTP client.
    :param group: Name of the node group to evaluate.
    :param baseline: Path to a baseline JSON file to compare against.
    :param save: Path to save current metrics as a new baseline.
    """
    result = client.command("diff_group", {
        "group": group,
        "baseline": baseline,
        "save": save,
    })
    result["ok"] = bool(result.get("success"))
    return result


@cli_command
def deps(client: BlenderClient, group: str, flat: bool = False) -> dict:
    """Show the dependency tree of a node group (which sub-groups it references, recursively).

    :param client: Blender HTTP client.
    :param group: Name of the root node group to inspect.
    :param flat: Return a flat sorted list instead of a tree.
    """
    visited: set[str] = set()

    def _walk(name: str) -> dict:
        if name in visited:
            return {"group": name, "deps": [], "circular": True}
        visited.add(name)

        result = client.command("inspect_group", {"group": name})
        if not result.get("success"):
            return {"group": name, "deps": [], "error": f"Could not inspect: {name}"}

        children = []
        for node in result.get("nodes", []):
            if node.get("type") == "GeometryNodeGroup":
                sub_name = node.get("node_tree")
                if sub_name:
                    children.append(_walk(sub_name))
        return {"group": name, "deps": children}

    tree = _walk(group)

    if flat:
        all_groups = sorted(visited)
        return {"ok": True, "group": group, "dependencies": all_groups, "count": len(all_groups)}

    return {"ok": True, "tree": tree}


def _ensure_init_files(directory: Path) -> list[str]:
    """Create __init__.py in every package directory from REPO_ROOT down to directory."""
    created = []
    pkg_root = REPO_ROOT / "procedural_human"
    for parent in [directory, *directory.parents]:
        if parent == pkg_root or not parent.is_relative_to(pkg_root):
            break
        init_file = parent / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")
            created.append(str(init_file.relative_to(REPO_ROOT)))
    return created


@cli_command
def promote(client: BlenderClient, group: str, dest: str,
            clean: bool = False, brief: bool = False,
            validate_after: bool = False) -> dict:
    """Move exported tmp files to a permanent location, rewriting imports.

    :param client: Blender HTTP client.
    :param group: Name of the exported group (folder under procedural_human/tmp/).
    :param dest: Destination path relative to repo root (e.g. procedural_human/geo_node_groups/armor/blocker).
    :param clean: Remove the tmp source directory after promoting.
    :param brief: Show counts instead of full file lists.
    :param validate_after: Run validate on the promoted group after copying.
    """
    src_dir = REPO_ROOT / "procedural_human" / "tmp" / group.lower()
    dest_dir = REPO_ROOT / dest

    if not src_dir.exists():
        result = {"ok": False, "error": f"Source not found: {src_dir.relative_to(REPO_ROOT)}"}
        if brief:
            result["_brief"] = f"FAIL promote {group}: source not found"
        return result

    src_module = f"procedural_human.tmp.{group.lower()}"
    dest_module = str(dest).replace("/", ".").replace("\\", ".")

    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)

    rewritten = []
    init_files = []
    for py_file in dest_dir.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        new_text = text.replace(src_module, dest_module)
        if new_text != text:
            py_file.write_text(new_text, encoding="utf-8")
            rewritten.append(str(py_file.relative_to(REPO_ROOT)))

    for sub_dir in [dest_dir] + sorted(
        d for d in dest_dir.rglob("*") if d.is_dir()
    ):
        init_files.extend(_ensure_init_files(sub_dir))

    if clean:
        shutil.rmtree(src_dir)

    files_copied = sorted(
        str(p.relative_to(REPO_ROOT)) for p in dest_dir.rglob("*.py")
    )

    result = {
        "ok": True,
        "source": str(src_dir.relative_to(REPO_ROOT)),
        "destination": str(dest_dir.relative_to(REPO_ROOT)),
        "files_copied": files_copied,
        "imports_rewritten": rewritten,
        "init_files_created": init_files,
        "source_cleaned": clean,
    }

    if validate_after:
        from tools.commands.validation import validate as run_validate
        val_result = run_validate(client, group=group)
        result["validation"] = val_result
        if not val_result.get("ok"):
            result["ok"] = False
            result["error"] = f"Post-promote validation failed: {val_result.get('error', 'unknown')}"

    if brief:
        summary = f"Promoted {len(files_copied)} files, rewrote {len(rewritten)} imports to {dest}"
        if validate_after:
            val_ok = result.get("validation", {}).get("ok", False)
            summary += f" | validate: {'PASS' if val_ok else 'FAIL'}"
        result["_brief"] = summary

    return result


@cli_command
def export_and_promote(
    client: BlenderClient,
    group: str,
    dest: str,
    use_helpers: bool = True,
    split_frames: bool = False,
    include_labels: bool = True,
    include_locations: bool = False,
    include_names: bool = False,
    clean: bool = False,
    brief: bool = False,
    validate_after: bool = False,
) -> dict:
    """Export a node group then promote to a permanent location in one step.

    :param client: Blender HTTP client.
    :param group: Name of the node group to export.
    :param dest: Destination path relative to repo root.
    :param use_helpers: Substitute node_helpers where patterns match.
    :param split_frames: Split top-level frames into separate files.
    :param include_labels: Include node labels in output.
    :param include_locations: Include node locations in output.
    :param include_names: Include node names in output.
    :param clean: Remove the tmp source directory after promoting.
    :param brief: Show counts instead of full output.
    :param validate_after: Run validate on the promoted group after copying.
    """
    export_result = export(
        client, group=group, use_helpers=use_helpers,
        split_frames=split_frames, include_labels=include_labels,
        include_locations=include_locations, include_names=include_names,
        verbose=False,
    )

    if not export_result.get("ok"):
        result = {"ok": False, "error": "Export failed", "export": export_result}
        if brief:
            result["_brief"] = f"FAIL {group}: export failed"
        return result

    promote_result = promote(
        client, group=group, dest=dest, clean=clean,
        brief=False, validate_after=validate_after,
    )

    result = {
        "ok": promote_result.get("ok", False),
        "export": export_result,
        "promote": promote_result,
    }
    if not result["ok"]:
        result["error"] = promote_result.get("error", "Promote failed")

    if brief:
        files = promote_result.get("files_copied", [])
        rewritten = promote_result.get("imports_rewritten", [])
        summary = f"Exported + promoted {len(files)} files, rewrote {len(rewritten)} imports to {dest}"
        if validate_after:
            val = promote_result.get("validation", {})
            summary += f" | validate: {'PASS' if val.get('ok') else 'FAIL'}"
        result["_brief"] = summary

    return result
