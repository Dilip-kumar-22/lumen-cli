# lumen-cli 💡

An AI-powered CLI that uses local LLMs to illuminate your codebase with automated documentation, refactoring insights, and architecture visualization.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/lumen-cli.svg?color=green)](https://pypi.org/project/lumen-cli/) <!-- Placeholder -->

---

`lumen-cli` brings the power of Large Language Models directly to your terminal, running completely offline against your local Ollama instance. Keep your code private while leveraging AI to accelerate your development workflow.

## Features

-   **🔒 Private & Offline:** All processing is done locally. Your code never leaves your machine.
-   **✍️ Auto-Documentation:** Generate context-aware docstrings for Python functions and classes or create a comprehensive `README.md` for your entire project.
-   **🔧 Refactoring Suggestions:** Get actionable, AI-driven insights to improve code quality, readability, and performance.
-   **🗺️ Architecture Visualization:** Automatically generate an interactive module dependency graph to understand your project's structure at a glance.

## Prerequisites

1.  **Python 3.8+**
2.  **Ollama:** You must have [Ollama](https://ollama.ai/) installed and running. You'll also need to have a model pulled, for example:
    ```sh
    ollama pull llama3
    ```
3.  **Graphviz:** For the `visualize` command, you need to install the Graphviz system package.
    -   **macOS (using Homebrew):** `brew install graphviz`
    -   **Ubuntu/Debian:** `sudo apt-get install graphviz`
    -   **Windows (using Chocolatey):** `choco install graphviz`

## Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com/your-username/lumen-cli.git
    cd lumen-cli
    ```

2.  Create and activate a virtual environment (recommended):
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required packages and the CLI tool:
    ```sh
    pip install -r requirements.txt
    pip install -e .
    ```

Now the `lumen` command will be available in your terminal.

## Usage

### General Help

```sh
lumen --help
```

### 1. Document Code

Generate docstrings for a specific file and print them to the console.

```sh
lumen document --file path/to/your/file.py
```

Generate a complete `README.md` for a project directory.

```sh
lumen document --dir . --output README.gen.md
```

### 2. Get Refactoring Suggestions

Receive AI-powered suggestions to improve your code.

```sh
lumen refactor --file path/to/your/code.py
```

### 3. Visualize Project Structure

Generate a module dependency graph for your project.

```sh
lumen visualize --dir . --output dependency_graph.png
```

This will create a `dependency_graph.png` file in your current directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.