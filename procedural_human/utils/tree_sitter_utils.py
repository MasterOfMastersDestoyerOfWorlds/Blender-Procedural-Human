"""
Tree-sitter utilities for parsing and modifying Python files.
"""

import os
from typing import Optional, Dict, List, Tuple

try:
    import tree_sitter_python as tspython
    from tree_sitter import Language, Parser
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    tspython = None
    Language = None
    Parser = None


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
                    print(f"Error scanning {file_path}: {e}")
    
    return presets


def get_python_language() -> Language:
    """Get the Python language parser."""
    if not TREE_SITTER_AVAILABLE:
        raise ImportError(
            "tree-sitter-python is not available. Install it with: pip install tree-sitter-python"
        )
    return Language(tspython.language())


def parse_python_file(file_path: str) -> Tuple[Parser, bytes]:
    """
    Parse a Python file using tree-sitter.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Tuple of (parser, source_bytes)
    """
    if not TREE_SITTER_AVAILABLE:
        raise ImportError(
            "tree-sitter-python is not available. Install it with: pip install tree-sitter-python"
        )
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "rb") as f:
        source_bytes = f.read()
    
    parser = Parser()
    parser.set_language(get_python_language())
    
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

