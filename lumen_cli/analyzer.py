import os
import ast
from typing import List

def get_file_content(file_path: str) -> str:
    """
    Reads and returns the content of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        raise
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise

def get_project_structure(dir_path: str, indent: str = '') -> str:
    """
    Recursively builds a string representation of the project's directory structure.

    Args:
        dir_path (str): The root directory of the project.
        indent (str): The indentation string for formatting the tree.

    Returns:
        str: A formatted string representing the file tree.
    """
    structure = ''
    items = sorted(os.listdir(dir_path))
    for i, name in enumerate(items):
        path = os.path.join(dir_path, name)
        # Ignore common unnecessary directories/files
        if name in ['__pycache__', '.git', '.vscode', 'venv', '.env']:
            continue

        # Determine connector for tree structure
        connector = '└── ' if i == len(items) - 1 else '├── '
        structure += f"{indent}{connector}{name}\n"

        if os.path.isdir(path):
            # Determine indentation for subdirectory
            sub_indent = '    ' if i == len(items) - 1 else '│   '
            structure += get_project_structure(path, indent + sub_indent)

    return structure

def find_imports(file_path: str) -> List[str]:
    """
    Parses a Python file and extracts all imported modules.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        List[str]: A list of imported module names.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
    except (SyntaxError, UnicodeDecodeError):
        # Skip files that can't be parsed
        return []

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])

    return sorted(list(imports))
