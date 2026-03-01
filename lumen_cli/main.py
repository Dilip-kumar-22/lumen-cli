import click
import sys
from typing import Optional

from .analyzer import get_file_content, get_project_structure
from .llm import OllamaClient
from .visualizer import generate_dependency_graph

# Default configuration
DEFAULT_MODEL = 'llama3'
DEFAULT_OLLAMA_HOST = 'http://localhost:11434'

@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Lumen CLI: An AI-powered assistant for your codebase."""
    pass

@cli.command()
@click.option('--file', 'file_path', type=click.Path(exists=True, dir_okay=False), help='Path to the Python file to document.')
@click.option('--dir', 'dir_path', type=click.Path(exists=True, file_okay=False), help='Path to the project directory to generate a README for.')
@click.option('--output', type=click.Path(), default=None, help='Output file path for generated README.md.')
@click.option('--model', default=DEFAULT_MODEL, help=f'Ollama model to use (default: {DEFAULT_MODEL}).')
def document(file_path: Optional[str], dir_path: Optional[str], output: Optional[str], model: str):
    """Generates docstrings for a file or a README.md for a directory."""
    if not file_path and not dir_path:
        raise click.UsageError('Either --file or --dir must be provided.')
    if file_path and dir_path:
        raise click.UsageError('Cannot use --file and --dir at the same time.')

    client = OllamaClient(host=DEFAULT_OLLAMA_HOST)
    if not client.check_model_availability(model):
        click.secho(f"Error: Model '{model}' not found. Please pull it with 'ollama pull {model}'.", fg='red')
        sys.exit(1)

    if file_path:
        click.echo(f"✨ Analyzing {file_path} for docstrings with model '{model}'...")
        content = get_file_content(file_path)
        if not content.strip():
            click.echo("File is empty. Nothing to document.")
            return
        prompt = f"Generate a concise, Google-style Python docstring for the following code. Only return the docstring itself, without any explanation or markdown formatting.\n\nCode:\n```python\n{content}\n```"
        response = client.generate(prompt, model)
        click.echo("\n--- Generated Docstring ---")
        click.echo(response)
        click.echo("---------------------------")

    if dir_path:
        if output is None:
            raise click.UsageError('The --output option is required when using --dir.')
        click.echo(f"✨ Analyzing project structure in {dir_path} to generate README.md with model '{model}'...")
        structure = get_project_structure(dir_path)
        prompt = f"Generate a comprehensive README.md for a Python project with the following file structure. The README should include a project title, a brief description, a list of key features, and basic usage instructions. Do not include an installation section.\n\nProject Structure:\n```\n{structure}\n```"
        response = client.generate(prompt, model)
        with open(output, 'w', encoding='utf-8') as f:
            f.write(response)
        click.secho(f"✅ Successfully generated README at {output}", fg='green')

@cli.command()
@click.option('--file', 'file_path', required=True, type=click.Path(exists=True, dir_okay=False), help='Path to the file to refactor.')
@click.option('--model', default=DEFAULT_MODEL, help=f'Ollama model to use (default: {DEFAULT_MODEL}).')
def refactor(file_path: str, model: str):
    """Provides AI-driven refactoring suggestions for a file."""
    client = OllamaClient(host=DEFAULT_OLLAMA_HOST)
    if not client.check_model_availability(model):
        click.secho(f"Error: Model '{model}' not found. Please pull it with 'ollama pull {model}'.", fg='red')
        sys.exit(1)

    click.echo(f"✨ Analyzing {file_path} for refactoring insights with model '{model}'...")
    content = get_file_content(file_path)
    if not content.strip():
        click.echo("File is empty. Nothing to refactor.")
        return

    prompt = f"Analyze the following Python code and provide actionable refactoring suggestions. For each suggestion, explain the reasoning and show a 'before' and 'after' code snippet. Focus on improving readability, maintainability, and performance.\n\nCode:\n```python\n{content}\n```"
    response = client.generate(prompt, model)
    click.echo("\n--- Refactoring Suggestions ---")
    click.echo(response)
    click.echo("-----------------------------")

@cli.command()
@click.option('--dir', 'dir_path', required=True, type=click.Path(exists=True, file_okay=False), help='Path to the project directory to visualize.')
@click.option('--output', default='dependency_graph.png', help='Output file for the graph (e.g., graph.png, graph.svg).')
def visualize(dir_path: str, output: str):
    """Generates a module dependency graph for a project."""
    click.echo(f"✨ Generating dependency graph for '{dir_path}'...")
    try:
        generate_dependency_graph(dir_path, output)
        click.secho(f"✅ Dependency graph saved to '{output}'", fg='green')
    except FileNotFoundError:
        click.secho("Error: 'graphviz' command not found.", fg='red')
        click.secho("Please install the Graphviz system package. See README.md for instructions.", fg='yellow')
        sys.exit(1)
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", fg='red')
        sys.exit(1)

if __name__ == '__main__':
    cli()
