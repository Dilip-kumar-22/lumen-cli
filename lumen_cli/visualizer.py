import os
import ast
from graphviz import Digraph
from typing import Set

from .analyzer import find_imports

def generate_dependency_graph(dir_path: str, output_file: str):
    """
    Generates a module dependency graph for a Python project.

    Args:
        dir_path (str): The root directory of the project.
        output_file (str): The path to save the output graph image.
    """
    dot = Digraph(comment='Python Project Dependencies', format=output_file.split('.')[-1])
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica')
    dot.attr('edge', color='gray40')
    dot.attr(rankdir='LR', splines='ortho')

    project_modules: Set[str] = set()
    py_files = []

    # First pass: find all .py files and identify project modules
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                # Convert file path to module name (e.g., src/utils/helpers.py -> src.utils.helpers)
                rel_path = os.path.relpath(module_path, dir_path)
                module_name = os.path.splitext(rel_path)[0].replace(os.sep, '.')
                project_modules.add(module_name)
                py_files.append((module_name, module_path))

    # Second pass: build the graph
    for module_name, file_path in py_files:
        dot.node(module_name, module_name)
        imports = find_imports(file_path)
        for imp in imports:
            # Check if the import is a local project module
            # This is a simple check; more complex resolution might be needed for advanced cases
            if imp in project_modules:
                dot.edge(module_name, imp)
            # You could optionally add nodes for external libraries
            # else:
            #     dot.node(imp, imp, style='filled', fillcolor='lightblue')
            #     dot.edge(module_name, imp)

    # Render the graph
    output_path_base = os.path.splitext(output_file)[0]
    dot.render(output_path_base, view=False, cleanup=True)
