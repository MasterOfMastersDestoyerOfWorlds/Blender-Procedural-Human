"""
Tree-sitter utilities for parsing and modifying Python files.
Extended with DSL parsing capabilities.
"""

import os
import inspect
from typing import Optional, Dict, List, Tuple, Any

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Node
from procedural_human.logger import *

DSL_PRIMITIVE_TYPES = {
    "DualRadial": {"profile_type": "dual", "profiles": ["X", "Y"]},
    "QuadRadial": {"profile_type": "quad", "profiles": ["0", "90", "180", "270"]},
    "Joint": {"profile_type": "quad", "profiles": ["0", "90", "180", "270"]},
    "RadialAttachment": {"profile_type": "dual", "profiles": ["X", "Y"]},
    "IKLimits": {"profile_type": None, "profiles": []},
}
 

def get_caller_file_path() -> Optional[str]:
    """
    Get the file path of the caller (where the decorator is being applied).
    
    Returns:
        Absolute file path or None if not found
    """
    frame = inspect.currentframe()
    try:
        # Go up the stack to find the caller
        caller_frame = frame.f_back
        if caller_frame:
            caller_frame = caller_frame.f_back
            if caller_frame:
                file_path = caller_frame.f_code.co_filename
                if file_path and os.path.exists(file_path):
                    return os.path.abspath(file_path)
    finally:
        del frame
    
    return None


def locate_preset_in_file(file_path: str, preset_name: str) -> Optional[Dict]:
    """
    Locate a preset class in a file using tree-sitter.
    
    Args:
        file_path: Path to the Python file
        preset_name: Name of the preset (from decorator argument)
        
    Returns:
        Dictionary with location information or None if not found
    """
    if not os.path.exists(file_path):
        return None
    
    class_info = find_class_with_decorator(file_path, "register_preset_class", preset_name)
    
    if class_info:
        class_info["file_path"] = file_path
        return class_info
    
    return None


def scan_directory_for_presets(directory: str) -> List[Dict]:
    """
    Scan a directory for all preset classes.
    
    Args:
        directory: Directory to scan
        
    Returns:
        List of preset location dictionaries
    """
    presets = []
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "node_modules")]
        
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    # Try to find any preset classes in this file
                    # We'll need to parse and check for decorators
                    # For now, we'll rely on the registry to provide preset names
                    pass
                except Exception as e:
                    logger.info(f"Error scanning {file_path}: {e}")
    
    return presets


def get_python_language() -> Language:
    """Get the Python language parser."""
    return Language(tspython.language())


def parse_python_file(file_path: str) -> Tuple[Parser, bytes]:
    """
    Parse a Python file using tree-sitter.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Tuple of (parser, source_bytes)
    """
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "rb") as f:
        source_bytes = f.read()
    
    language = get_python_language()
    parser = Parser(language)
    
    return parser, source_bytes


def find_class_with_decorator(
    file_path: str, decorator_name: str, preset_name: Optional[str] = None
) -> Optional[Dict]:
    """
    Find a class definition with a specific decorator.
    
    Args:
        file_path: Path to the Python file
        decorator_name: Name of the decorator to find (e.g., "register_preset_class")
        preset_name: Optional preset name to match (from decorator argument)
        
    Returns:
        Dictionary with class information including:
        - class_name: Name of the class
        - decorator_line: Line number of the decorator
        - class_start_line: Starting line of class definition
        - class_end_line: Ending line of class definition
        - get_data_start_line: Starting line of get_data method (if found)
        - get_data_end_line: Ending line of get_data method (if found)
        Or None if not found
    """
    parser, source_bytes = parse_python_file(file_path)
    tree = parser.parse(source_bytes)
    
    source_lines = source_bytes.decode("utf-8").split("\n")
    
    # Query to find decorated class definitions
    query_string = """
    (decorated_definition
      decorator: (call
        function: (attribute
          object: (identifier) @decorator_obj
          attribute: (identifier) @decorator_attr)
        arguments: (argument_list
          (string) @preset_name_string)?)
      definition: (class_definition
        name: (identifier) @class_name
        body: (block) @class_body))
    """
    
    query = get_python_language().query(query_string)
    captures = query.captures(tree.root_node)
    
    # Build a map of captures by type
    captures_map = {}
    for node, capture_name in captures:
        if capture_name not in captures_map:
            captures_map[capture_name] = []
        captures_map[capture_name].append(node)
    
    # Find matching decorator
    for i, decorator_attr_node in enumerate(captures_map.get("@decorator_attr", [])):
        decorator_attr = source_bytes[
            decorator_attr_node.start_byte : decorator_attr_node.end_byte
        ].decode("utf-8")
        
        if decorator_attr == decorator_name:
            # Check if preset_name matches if provided
            if preset_name:
                preset_name_nodes = captures_map.get("@preset_name_string", [])
                if i < len(preset_name_nodes):
                    preset_name_str = source_bytes[
                        preset_name_nodes[i].start_byte : preset_name_nodes[i].end_byte
                    ].decode("utf-8").strip('"\'')
                    if preset_name_str != preset_name:
                        continue
            
            # Get class name
            class_name_nodes = captures_map.get("@class_name", [])
            if i < len(class_name_nodes):
                class_name_node = class_name_nodes[i]
                class_name = source_bytes[
                    class_name_node.start_byte : class_name_node.end_byte
                ].decode("utf-8")
                
                # Get class body
                class_body_nodes = captures_map.get("@class_body", [])
                if i < len(class_body_nodes):
                    class_body_node = class_body_nodes[i]
                    
                    # Find get_data method
                    get_data_start = None
                    get_data_end = None
                    
                    for child in class_body_node.children:
                        if child.type == "function_definition":
                            func_name_node = None
                            for func_child in child.children:
                                if func_child.type == "identifier":
                                    func_name_node = func_child
                                    break
                            
                            if func_name_node:
                                func_name = source_bytes[
                                    func_name_node.start_byte : func_name_node.end_byte
                                ].decode("utf-8")
                                
                                if func_name == "get_data":
                                    get_data_start = child.start_point[0] + 1  # 1-indexed
                                    get_data_end = child.end_point[0] + 1  # 1-indexed
                                    break
                    
                    # Get decorator line
                    decorator_obj_nodes = captures_map.get("@decorator_obj", [])
                    decorator_line = None
                    if i < len(decorator_obj_nodes):
                        decorator_line = decorator_obj_nodes[i].start_point[0] + 1
                    
                    return {
                        "class_name": class_name,
                        "decorator_line": decorator_line,
                        "class_start_line": class_name_node.start_point[0] + 1,
                        "class_end_line": class_body_node.end_point[0] + 1,
                        "get_data_start_line": get_data_start,
                        "get_data_end_line": get_data_end,
                    }
    
    return None


def replace_get_data_method(
    file_path: str, preset_name: str, new_data: dict
) -> bool:
    """
    Replace the get_data method body in a preset class.
    
    Args:
        file_path: Path to the Python file
        preset_name: Name of the preset (from decorator argument)
        new_data: New data dictionary to return
        
    Returns:
        True if replacement was successful, False otherwise
    """
    import json
    
    class_info = find_class_with_decorator(
        file_path, "register_preset_class", preset_name
    )
    
    if not class_info or not class_info.get("get_data_start_line"):
        return False
    
    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Format the new data as JSON
    formatted_data = json.dumps(new_data, indent=4)
    
    # Find the get_data method and replace its return statement
    get_data_start = class_info["get_data_start_line"] - 1  # Convert to 0-indexed
    get_data_end = class_info["get_data_end_line"] - 1  # Convert to 0-indexed
    
    # Find the return statement line
    return_line_idx = None
    indent = None
    
    for i in range(get_data_start, min(get_data_end + 1, len(lines))):
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith("return"):
            return_line_idx = i
            indent = line[: len(line) - len(stripped)]
            break
    
    if return_line_idx is None:
        # No return statement found, add one
        # Find the method body start (first non-empty line after def get_data)
        method_body_start = get_data_start + 1
        while method_body_start < len(lines) and not lines[method_body_start].strip():
            method_body_start += 1
        
        if method_body_start < len(lines):
            indent = lines[method_body_start][: len(lines[method_body_start]) - len(lines[method_body_start].lstrip())]
            indent += "    "  # Add extra indent for return statement
        
        # Replace everything from method body start to end with new return
        new_lines = lines[:method_body_start]
        new_lines.append(f"{indent}return {formatted_data}\n")
        new_lines.extend(lines[get_data_end:])
        lines = new_lines
    else:
        # Replace the return statement
        new_return_line = f"{indent}return {formatted_data}\n"
        
        # Replace from return line to end of method
        lines = lines[:return_line_idx] + [new_return_line] + lines[get_data_end:]
    
    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    return True


def parse_dsl_file(file_path: str) -> Tuple[Any, bytes, Any]:
    """Parse a DSL file using tree-sitter."""
    parser, source_bytes = parse_python_file(file_path)
    tree = parser.parse(source_bytes)
    return tree, source_bytes, tree.root_node


def _get_node_text(node: Any, source_bytes: bytes) -> str:
    """Extract text from a tree-sitter node."""
    return source_bytes[node.start_byte:node.end_byte].decode("utf-8")


def _parse_argument_list(node: Any, source_bytes: bytes) -> Dict:
    """Parse function call arguments into a dictionary."""
    args = {"positional": [], "keyword": {}}
    
    for child in node.children:
        if child.type == "keyword_argument":
            key_node = None
            value_node = None
            for arg_child in child.children:
                if arg_child.type == "identifier":
                    key_node = arg_child
                elif arg_child.type not in ("=",):
                    value_node = arg_child
            if key_node and value_node:
                key = _get_node_text(key_node, source_bytes)
                value = _get_node_text(value_node, source_bytes)
                args["keyword"][key] = value
        elif child.type == "list":
            args["positional"].append(_get_node_text(child, source_bytes))
        elif child.type not in ("(", ")", ","):
            args["positional"].append(_get_node_text(child, source_bytes))
    
    return args


def extract_class_definitions(file_path: str) -> List[Dict]:
    """Extract all class definitions from a DSL file."""
    
    tree, source_bytes, root_node = parse_dsl_file(file_path)
    class_defs = []
    
    for child in root_node.children:
        if child.type == "class_definition":
            class_info = _extract_class_info(child, source_bytes)
            if class_info:
                class_defs.append(class_info)
    
    return class_defs


def _extract_class_info(class_node: Any, source_bytes: bytes) -> Optional[Dict]:
    """Extract information from a class definition node."""
    class_name = None
    class_body = None
    
    for child in class_node.children:
        if child.type == "identifier":
            class_name = _get_node_text(child, source_bytes)
        elif child.type == "block":
            class_body = child
    
    if not class_name or not class_body:
        return None
    
    class_info = {
        "name": class_name,
        "components": {},
        "init_params": [],
        "line_start": class_node.start_point[0] + 1,
        "line_end": class_node.end_point[0] + 1,
    }
    
    for body_child in class_body.children:
        if body_child.type == "function_definition":
            func_name = None
            func_params = None
            func_body = None
            
            for func_child in body_child.children:
                if func_child.type == "identifier":
                    func_name = _get_node_text(func_child, source_bytes)
                elif func_child.type == "parameters":
                    func_params = func_child
                elif func_child.type == "block":
                    func_body = func_child
            
            if func_name == "__init__":
                if func_params:
                    class_info["init_params"] = _extract_params(func_params, source_bytes)
                if func_body:
                    class_info["components"] = _extract_components(func_body, source_bytes)
                break
    
    return class_info


def _extract_params(params_node: Any, source_bytes: bytes) -> List[Dict]:
    """Extract function parameters."""
    params = []
    
    for child in params_node.children:
        if child.type == "identifier":
            name = _get_node_text(child, source_bytes)
            if name != "self":
                params.append({"name": name, "default": None})
        elif child.type == "default_parameter":
            name = None
            default = None
            for param_child in child.children:
                if param_child.type == "identifier":
                    name = _get_node_text(param_child, source_bytes)
                elif param_child.type not in ("=",):
                    default = _get_node_text(param_child, source_bytes)
            if name:
                params.append({"name": name, "default": default})
    
    return params


def _extract_components(body_node: Any, source_bytes: bytes) -> Dict:
    """Extract component assignments from a function body."""
    components = {}
    
    for child in body_node.children:
        if child.type == "expression_statement":
            expr = child.children[0] if child.children else None
            if expr and expr.type == "assignment":
                component_info = _parse_component_assignment(expr, source_bytes)
                if component_info:
                    components[component_info["name"]] = component_info
        elif child.type == "for_statement":
            loop_info = _parse_loop_for_indexed_components(child, source_bytes)
            if loop_info:
                for name, info in loop_info.items():
                    components[name] = info
    
    return components


def _parse_component_assignment(assign_node: Any, source_bytes: bytes) -> Optional[Dict]:
    """Parse a component assignment like Segment = DualRadial(...)"""
    left = None
    right = None
    
    for child in assign_node.children:
        if child.type == "identifier" and left is None:
            left = _get_node_text(child, source_bytes)
        elif child.type == "call":
            right = child
        elif child.type not in ("=",) and right is None and child.type != "identifier":
            return None
    
    if not left or not right:
        return None
    
    func_name = None
    args = {}
    
    for call_child in right.children:
        if call_child.type == "identifier":
            func_name = _get_node_text(call_child, source_bytes)
        elif call_child.type == "argument_list":
            args = _parse_argument_list(call_child, source_bytes)
    
    if func_name not in DSL_PRIMITIVE_TYPES:
        return None
    
    primitive_info = DSL_PRIMITIVE_TYPES[func_name]
    
    return {
        "name": left,
        "type": func_name,
        "profile_type": primitive_info["profile_type"],
        "profiles": primitive_info["profiles"],
        "indexed": False,
        "args": args,
    }


def _parse_loop_for_indexed_components(for_node: Any, source_bytes: bytes) -> Dict:
    """Parse a for loop to detect indexed component creation."""
    components = {}
    loop_var = None
    
    for child in for_node.children:
        if child.type == "identifier":
            loop_var = _get_node_text(child, source_bytes)
            break
    
    for child in for_node.children:
        if child.type == "block":
            for body_child in child.children:
                if body_child.type == "expression_statement":
                    expr = body_child.children[0] if body_child.children else None
                    if expr and expr.type == "assignment":
                        component_info = _parse_indexed_component(expr, source_bytes, loop_var)
                        if component_info:
                            component_info["indexed"] = True
                            components[component_info["name"]] = component_info
    
    return components


def _parse_indexed_component(assign_node: Any, source_bytes: bytes, loop_var: str) -> Optional[Dict]:
    """Parse an indexed component assignment inside a loop."""
    left = None
    right = None
    
    for child in assign_node.children:
        if child.type == "identifier" and left is None:
            left = _get_node_text(child, source_bytes)
        elif child.type == "call":
            right = child
    
    if not left or not right:
        return None
    
    func_name = None
    args = {}
    
    for call_child in right.children:
        if call_child.type == "identifier":
            func_name = _get_node_text(call_child, source_bytes)
        elif call_child.type == "argument_list":
            args = _parse_argument_list(call_child, source_bytes)
    
    if not func_name or not func_name[0].isupper():
        return None
    
    return {
        "name": func_name,
        "type": func_name,
        "profile_type": "dual",
        "profiles": ["X", "Y"],
        "indexed": True,
        "args": args,
    }


def extract_instance_assignments(file_path: str) -> List[Dict]:
    """Extract instance assignments from a DSL file."""
    
    tree, source_bytes, root_node = parse_dsl_file(file_path)
    instances = []
    
    class_names = set()
    for child in root_node.children:
        if child.type == "class_definition":
            for class_child in child.children:
                if class_child.type == "identifier":
                    class_names.add(_get_node_text(class_child, source_bytes))
                    break
    
    for child in root_node.children:
        if child.type == "expression_statement":
            expr = child.children[0] if child.children else None
            if expr and expr.type == "assignment":
                instance_info = _parse_instance_assignment(expr, source_bytes, class_names)
                if instance_info:
                    instances.append(instance_info)
    
    return instances


def _parse_instance_assignment(assign_node: Any, source_bytes: bytes, class_names: set) -> Optional[Dict]:
    """Parse an instance assignment like Index = Finger([...])"""
    left = None
    right = None
    
    for child in assign_node.children:
        if child.type == "identifier" and left is None:
            left = _get_node_text(child, source_bytes)
        elif child.type == "call":
            right = child
    
    if not left or not right:
        return None
    
    class_name = None
    args = {}
    
    for call_child in right.children:
        if call_child.type == "identifier":
            class_name = _get_node_text(call_child, source_bytes)
        elif call_child.type == "argument_list":
            args = _parse_argument_list(call_child, source_bytes)
    
    if class_name not in class_names:
        return None
    
    return {
        "name": left,
        "definition": class_name,
        "args": args,
        "line": assign_node.start_point[0] + 1,
    }


def find_preset_class_range(file_path: str, preset_name: str) -> Optional[Dict]:
    """
    Find the byte range and line range of a preset class in a file.
    
    Returns dict with start_byte, end_byte, start_line, end_line or None.
    """
    if not os.path.exists(file_path):
        return None
    
    parser, source_bytes = parse_python_file(file_path)
    tree = parser.parse(source_bytes)
    
    for node in tree.root_node.children:
        if node.type == "decorated_definition":
            decorators = []
            class_node = None
            
            for child in node.children:
                if child.type == "decorator":
                    decorators.append(child)
                elif child.type == "class_definition":
                    class_node = child
            
            if decorators and class_node:
                for decorator_node in decorators:
                    decorator_text = _get_node_text(decorator_node, source_bytes)
                    # Check both positional and keyword arg forms
                    if (f'register_preset_class("{preset_name}")' in decorator_text or
                        f'register_preset_class(name="{preset_name}")' in decorator_text):
                        return {
                            "start_byte": node.start_byte,
                            "end_byte": node.end_byte,
                            "start_line": node.start_point[0] + 1,
                            "end_line": node.end_point[0] + 1,
                        }
    
    return None


def find_last_import_position(file_path: str) -> Dict:
    """
    Find the position after the last import statement in a file.
    
    Returns dict with byte position and line number.
    """
    parser, source_bytes = parse_python_file(file_path)
    tree = parser.parse(source_bytes)
    
    last_import_end = 0
    last_import_line = 0
    
    for node in tree.root_node.children:
        if node.type in ("import_statement", "import_from_statement"):
            last_import_end = node.end_byte
            last_import_line = node.end_point[0] + 1
    
    return {
        "byte": last_import_end,
        "line": last_import_line,
    }


def find_file_end_position(file_path: str) -> Dict:
    """
    Find the end position of a file.
    
    Returns dict with byte position and line number.
    """
    parser, source_bytes = parse_python_file(file_path)
    tree = parser.parse(source_bytes)
    
    return {
        "byte": len(source_bytes),
        "line": tree.root_node.end_point[0] + 1,
    }


def has_import(file_path: str, import_text: str) -> bool:
    """Check if a file contains a specific import statement."""
    if not os.path.exists(file_path):
        return False
    
    parser, source_bytes = parse_python_file(file_path)
    tree = parser.parse(source_bytes)
    source_str = source_bytes.decode("utf-8")
    
    for node in tree.root_node.children:
        if node.type in ("import_statement", "import_from_statement"):
            node_text = _get_node_text(node, source_bytes)
            if import_text in node_text:
                return True
    
    return False


def insert_import_after_last(file_path: str, import_statement: str) -> bool:
    """
    Insert an import statement after the last existing import.
    Uses tree-sitter to find the correct position.
    
    Returns True if successful, False otherwise.
    """
    if has_import(file_path, import_statement.split()[-1].split(".")[0]):
        return True
    
    parser, source_bytes = parse_python_file(file_path)
    tree = parser.parse(source_bytes)
    
    last_import_end = 0
    
    for node in tree.root_node.children:
        if node.type in ("import_statement", "import_from_statement"):
            last_import_end = node.end_byte
    
    source_str = source_bytes.decode("utf-8")
    
    if last_import_end > 0:
        new_content = (
            source_str[:last_import_end] + 
            "\n" + import_statement + 
            source_str[last_import_end:]
        )
    else:
        if source_str.startswith('"""') or source_str.startswith("'''"):
            end_docstring = source_str.find('"""', 3)
            if end_docstring == -1:
                end_docstring = source_str.find("'''", 3)
            if end_docstring != -1:
                end_docstring += 3
                while end_docstring < len(source_str) and source_str[end_docstring] in "\n\r":
                    end_docstring += 1
                new_content = (
                    source_str[:end_docstring] + 
                    "\n" + import_statement + "\n" + 
                    source_str[end_docstring:]
                )
            else:
                new_content = import_statement + "\n\n" + source_str
        else:
            new_content = import_statement + "\n\n" + source_str
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True


def replace_or_append_preset_class(
    file_path: str,
    preset_name: str,
    class_name: str,
    curves_data: dict,
) -> bool:
    """
    Replace an existing preset class or append a new one using tree-sitter.
    
    Uses line-based replacement to be more robust against concurrent modifications.
    
    Args:
        file_path: Path to the Python file
        preset_name: Name for the @register_preset_class decorator
        class_name: Name of the class to create
        curves_data: Dictionary of curve data
        
    Returns:
        True if successful, False otherwise.
    """
    import json
    
    formatted_data = json.dumps(curves_data, indent=4)
    formatted_data_lines = formatted_data.split("\n")
    indented_data = "\n".join(
        "        " + line if i > 0 else "        " + line 
        for i, line in enumerate(formatted_data_lines)
    )
    
    new_class = f'''@register_preset_class(name="{preset_name}")
class {class_name}(Preset):
    """Preset for {preset_name} curves"""

    def get_data(self):
        return {indented_data.strip()}
'''
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    existing_range = find_preset_class_range(file_path, preset_name)
    
    if existing_range:
        lines = content.split("\n")
        start_line = existing_range["start_line"] - 1
        end_line = existing_range["end_line"]
        
        new_class_lines = new_class.rstrip("\n").split("\n")
        new_lines = lines[:start_line] + new_class_lines + lines[end_line:]
        new_content = "\n".join(new_lines)
    else:
        if not content.endswith("\n"):
            content += "\n"
        if not content.endswith("\n\n"):
            content += "\n"
        new_content = content + new_class
    
    try:
        compile(new_content, file_path, "exec")
    except SyntaxError as e:
        logger.info(f"[TreeSitter] Warning: Generated code has syntax error: {e}")
        logger.info(f"[TreeSitter] Skipping write to {file_path}")
        return False
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True


def _compact_blank_lines(lines: List[str], max_consecutive: int = 2) -> List[str]:
    """
    Compact consecutive blank lines to at most max_consecutive.
    
    This prevents blank line accumulation when repeatedly removing and re-adding content.
    """
    result = []
    blank_count = 0
    
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= max_consecutive:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    
    # Also trim trailing blank lines
    while result and result[-1].strip() == "":
        result.pop()
    
    return result


def batch_update_preset_classes(
    file_path: str,
    presets: List[Dict],
) -> bool:
    """
    Update multiple preset classes in a single file operation.
    
    This avoids race conditions from multiple sequential writes.
    
    Args:
        file_path: Path to the Python file
        presets: List of dicts with keys: preset_name, class_name, curves_data
        
    Returns:
        True if successful, False otherwise.
    """
    import json
    
    if not os.path.exists(file_path):
        return False
    
    existing_presets = {}
    for preset_info in presets:
        preset_name = preset_info["preset_name"]
        existing_range = find_preset_class_range(file_path, preset_name)
        existing_presets[preset_name] = existing_range
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
    
    ranges_to_remove = []
    for preset_name, existing_range in existing_presets.items():
        if existing_range:
            ranges_to_remove.append((existing_range["start_line"] - 1, existing_range["end_line"]))
    
    ranges_to_remove.sort(key=lambda x: x[0], reverse=True)
    for start_line, end_line in ranges_to_remove:
        lines = lines[:start_line] + lines[end_line:]
    
    # Compact blank lines to prevent accumulation (max 2 consecutive)
    lines = _compact_blank_lines(lines, max_consecutive=2)
    
    for preset_info in presets:
        preset_name = preset_info["preset_name"]
        class_name = preset_info["class_name"]
        curves_data = preset_info["curves_data"]
        
        formatted_data = json.dumps(curves_data, indent=4)
        formatted_data_lines = formatted_data.split("\n")
        indented_data = "\n".join(
            "        " + line if i > 0 else "        " + line 
            for i, line in enumerate(formatted_data_lines)
        )
        
        new_class_text = f'''

@register_preset_class(name="{preset_name}")
class {class_name}(Preset):
    """Preset for {preset_name} curves"""

    def get_data(self):
        return {indented_data.strip()}
'''
        new_class_lines = new_class_text.split("\n")
        lines.extend(new_class_lines)
    
    new_content = "\n".join(lines)
    
    try:
        compile(new_content, file_path, "exec")
    except SyntaxError as e:
        logger.info(f"[TreeSitter] Warning: Generated code has syntax error at line {e.lineno}: {e.msg}")
        logger.info(f"[TreeSitter] Skipping write to {file_path}")
        return False
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True


def ensure_presets_file_exists(source_file: str) -> str:
    """
    Ensure the presets file for a DSL source file exists.
    Creates it if it doesn't exist.
    
    Args:
        source_file: Path to the main DSL file (e.g., finger.py)
        
    Returns:
        Path to the presets file (e.g., finger_float_curve_presets.py)
    """
    dir_path = os.path.dirname(source_file)
    base_name = os.path.basename(source_file)
    name_without_ext = os.path.splitext(base_name)[0]
    presets_file = os.path.join(dir_path, f"{name_without_ext}_float_curve_presets.py")
    
    if not os.path.exists(presets_file):
        with open(presets_file, "w", encoding="utf-8") as f:
            f.write(f'''"""
Float curve presets for {name_without_ext} DSL.

Auto-generated file - do not edit manually.
Presets are saved here when curves are modified in Blender.
"""

from procedural_human.decorators.curve_preset_decorator import register_preset_class, Preset

''')
    
    return presets_file
