import argparse
import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class IndexSwitchInfo:
    var_name: str
    create_line: int
    data_type_line: int | None = None
    input_access_lines: List[int] = field(default_factory=list)
    max_input_index: int = 0
    item_new_count: int = 0


@dataclass
class ForEachInfo:
    input_var: str
    output_var: str
    input_create_line: int
    output_create_line: int | None = None
    pair_line: int | None = None
    output_item_new_count: int = 0
    custom_indices: Dict[int, str] = field(default_factory=dict)
    custom_input_use_lines: List[int] = field(default_factory=list)


class LineEdits:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.remove_lines: set[int] = set()
        self.insert_after: Dict[int, List[str]] = {}

    def add_after(self, line_no: int, code_lines: List[str]) -> None:
        if not code_lines:
            return
        self.insert_after.setdefault(line_no, []).extend(code_lines)

    def remove(self, line_no: int) -> None:
        self.remove_lines.add(line_no)

    def move_line_after(self, from_line: int, to_line: int) -> None:
        if from_line == to_line:
            return
        src = self.lines[from_line - 1].rstrip("\n")
        self.remove(from_line)
        self.add_after(to_line, [src])

    def build(self) -> str:
        out: List[str] = []
        for i, line in enumerate(self.lines, start=1):
            if i not in self.remove_lines:
                out.append(line.rstrip("\n"))
            for extra in self.insert_after.get(i, []):
                out.append(extra)
        return "\n".join(out) + "\n"


def infer_type_from_value(node: ast.AST) -> str:
    """Infer the socket_type enum value for ForEach/CaptureAttribute items.

    The Blender API uses 'VECTOR' (not 'FLOAT_VECTOR') in socket-type enums
    for collection items like input_items, capture_items, repeat_items.
    """
    if isinstance(node, ast.Call):
        func_name = ast.unparse(node.func)
        if func_name.endswith("Euler"):
            return "ROTATION"
        if func_name.endswith("Vector"):
            return "VECTOR"
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return "BOOLEAN"
        if isinstance(node.value, int):
            return "INT"
        if isinstance(node.value, float):
            return "FLOAT"
    if isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) == 3:
        return "VECTOR"
    return "FLOAT"


def infer_type_from_source(expr: ast.AST) -> str:
    txt = ast.unparse(expr)
    if "curve_to_points" in txt and ".outputs[3]" in txt:
        return "ROTATION"
    if "position" in txt and ".outputs[0]" in txt:
        return "VECTOR"
    if "normal" in txt and ".outputs[0]" in txt:
        return "VECTOR"
    return "FLOAT"


def merge_type(existing: str | None, new_value: str) -> str:
    rank = {"FLOAT": 0, "INT": 1, "BOOLEAN": 1, "FLOAT_VECTOR": 2, "ROTATION": 3}
    if existing is None:
        return new_value
    return new_value if rank.get(new_value, 0) > rank.get(existing, 0) else existing


def parse_subscript_index(node: ast.Subscript) -> int | None:
    sl = node.slice
    if isinstance(sl, ast.Constant) and isinstance(sl.value, int):
        return sl.value
    return None


def get_attr_chain(node: ast.AST) -> List[str]:
    parts: List[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
    return list(reversed(parts))


def analyze_file(path: Path) -> tuple[ast.Module, Dict[str, IndexSwitchInfo], Dict[str, ForEachInfo]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    index_switches: Dict[str, IndexSwitchInfo] = {}
    foreaches: Dict[str, ForEachInfo] = {}

    # Pass 1: collect node declarations.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target = node.targets[0].id
            if isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Attribute) and call.func.attr == "new" and call.args:
                    first = call.args[0]
                    if isinstance(first, ast.Constant) and isinstance(first.value, str):
                        node_type = first.value
                        if node_type == "GeometryNodeIndexSwitch":
                            index_switches[target] = IndexSwitchInfo(var_name=target, create_line=node.lineno)
                        elif node_type == "GeometryNodeForeachGeometryElementInput":
                            output_guess = target.replace("input", "output")
                            foreaches[target] = ForEachInfo(
                                input_var=target,
                                output_var=output_guess,
                                input_create_line=node.lineno,
                            )
                        elif node_type == "GeometryNodeForeachGeometryElementOutput":
                            input_guess = target.replace("output", "input")
                            if input_guess in foreaches:
                                foreaches[input_guess].output_create_line = node.lineno

    # Handle output declarations discovered before input declarations.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target = node.targets[0].id
            if isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Attribute) and call.func.attr == "new" and call.args:
                    first = call.args[0]
                    if isinstance(first, ast.Constant) and isinstance(first.value, str):
                        if first.value == "GeometryNodeForeachGeometryElementOutput":
                            input_guess = target.replace("output", "input")
                            if input_guess in foreaches:
                                foreaches[input_guess].output_create_line = node.lineno

    # Pass 2: collect socket/index usage and method calls.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Attribute):
                tgt = node.targets[0]
                chain = get_attr_chain(tgt)
                if len(chain) == 2 and chain[1] == "data_type" and chain[0] in index_switches:
                    index_switches[chain[0]].data_type_line = node.lineno
                if tgt.attr == "default_value" and isinstance(tgt.value, ast.Subscript):
                    sub = tgt.value
                    if isinstance(sub.value, ast.Attribute) and sub.value.attr == "inputs" and isinstance(sub.value.value, ast.Name):
                        var = sub.value.value.id
                        idx = parse_subscript_index(sub)
                        if idx is not None:
                            if var in index_switches:
                                info = index_switches[var]
                                info.input_access_lines.append(node.lineno)
                                info.max_input_index = max(info.max_input_index, idx)
                            if var in foreaches and idx >= 2:
                                fi = foreaches[var]
                                fi.custom_indices[idx] = merge_type(fi.custom_indices.get(idx), infer_type_from_value(node.value))
                                fi.custom_input_use_lines.append(node.lineno)

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            chain = get_attr_chain(node.func)
            if len(chain) == 3 and chain[1] == "index_switch_items" and chain[2] == "new" and chain[0] in index_switches:
                index_switches[chain[0]].item_new_count += 1
            if len(chain) == 3 and chain[1] == "input_items" and chain[2] == "new":
                out_var = chain[0]
                for fi in foreaches.values():
                    if fi.output_var == out_var:
                        fi.output_item_new_count += 1
                        break
            if len(chain) == 2 and chain[1] == "pair_with_output" and chain[0] in foreaches:
                foreaches[chain[0]].pair_line = node.lineno

            # links.new(source, input_var.inputs[idx])
            if len(chain) == 2 and chain[0] == "links" and chain[1] == "new" and len(node.args) == 2:
                target = node.args[1]
                if isinstance(target, ast.Subscript):
                    if isinstance(target.value, ast.Attribute) and target.value.attr == "inputs" and isinstance(target.value.value, ast.Name):
                        in_var = target.value.value.id
                        idx = parse_subscript_index(target)
                        if idx is not None and in_var in foreaches and idx >= 2:
                            fi = foreaches[in_var]
                            fi.custom_indices[idx] = merge_type(fi.custom_indices.get(idx), infer_type_from_source(node.args[0]))
                            fi.custom_input_use_lines.append(node.lineno)
    return tree, index_switches, foreaches


def indent_of(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" "))]


def apply_index_switch_fixes(lines: List[str], edits: LineEdits, infos: Dict[str, IndexSwitchInfo]) -> int:
    changes = 0
    for info in infos.values():
        if info.max_input_index <= 2:
            continue
        if info.data_type_line is not None and info.input_access_lines and info.data_type_line > min(info.input_access_lines):
            edits.move_line_after(info.data_type_line, info.create_line)
            changes += 1
            insert_anchor = info.create_line
        else:
            insert_anchor = info.data_type_line or info.create_line

        needed = info.max_input_index - 2
        missing = max(0, needed - info.item_new_count)
        if missing:
            ind = indent_of(lines[insert_anchor - 1])
            item_lines = [f"{ind}{info.var_name}.index_switch_items.new()" for _ in range(missing)]
            edits.add_after(insert_anchor, item_lines)
            changes += missing
    return changes


def typename_label(socket_type: str, idx: int) -> str:
    labels = {
        "ROTATION": "Rotation",
        "FLOAT_VECTOR": "Vector",
        "BOOLEAN": "Boolean",
        "INT": "Integer",
        "FLOAT": "Value",
    }
    base = labels.get(socket_type, "Item")
    if idx > 2:
        return f"{base} {idx - 1}"
    return base


def apply_foreach_fixes(lines: List[str], edits: LineEdits, infos: Dict[str, ForEachInfo]) -> int:
    changes = 0
    for fi in infos.values():
        if fi.output_create_line is None:
            continue

        max_idx = max(fi.custom_indices.keys(), default=1)
        needed_items = max(0, max_idx - 1)
        missing_items = max(0, needed_items - fi.output_item_new_count)
        if missing_items:
            ind = indent_of(lines[fi.output_create_line - 1])
            item_lines: List[str] = []
            for idx in range(2 + fi.output_item_new_count, max_idx + 1):
                stype = fi.custom_indices.get(idx, "FLOAT")
                label = typename_label(stype, idx)
                item_lines.append(f'{ind}{fi.output_var}.input_items.new("{stype}", "{label}")')
            edits.add_after(fi.output_create_line, item_lines)
            changes += len(item_lines)

        if fi.pair_line is None:
            pair_anchor = max(fi.input_create_line, fi.output_create_line)
            ind = indent_of(lines[pair_anchor - 1])
            edits.add_after(pair_anchor, [f"{ind}{fi.input_var}.pair_with_output({fi.output_var})"])
            fi.pair_line = pair_anchor + 1
            changes += 1

        # Move any custom input socket usages that occur before pairing.
        move_anchor = fi.pair_line
        use_lines = sorted(set(fi.custom_input_use_lines))
        moving: List[str] = []
        for ln in use_lines:
            if ln < move_anchor:
                moving.append(lines[ln - 1].rstrip("\n"))
                edits.remove(ln)
        if moving:
            edits.add_after(move_anchor, moving)
            changes += len(moving)
    return changes


def process_file(path: Path, dry_run: bool) -> int:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    _, index_switches, foreaches = analyze_file(path)
    edits = LineEdits(lines)
    changes = 0
    changes += apply_index_switch_fixes(lines, edits, index_switches)
    changes += apply_foreach_fixes(lines, edits, foreaches)
    if changes:
        new_source = edits.build()
        if not dry_run:
            path.write_text(new_source, encoding="utf-8")
    return changes


def iter_python_files(targets: List[Path]) -> List[Path]:
    files: List[Path] = []
    for target in targets:
        if target.is_file() and target.suffix == ".py":
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.rglob("*.py")))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix dynamic socket item definitions in exported geo node group files.")
    parser.add_argument("paths", nargs="+", help="Files or directories to process")
    parser.add_argument("--dry-run", action="store_true", help="Analyze and report without writing changes")
    args = parser.parse_args()

    targets = [Path(p) for p in args.paths]
    files = iter_python_files(targets)
    total_changes = 0
    touched = 0
    for file_path in files:
        c = process_file(file_path, dry_run=args.dry_run)
        if c:
            touched += 1
            total_changes += c
            print(f"{file_path}: {c} edits")
    print(f"done: touched={touched}, edits={total_changes}, dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
