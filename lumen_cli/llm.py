import requests
import json
import sys
from typing import Dict, Any

class OllamaClient:
    """A client for interacting with a local Ollama API."""

    def __init__(self, host: str):
        """
        Initializes the OllamaClient.

        Args:
            host (str): The URL of the Ollama server (e.g., 'http://localhost:11434').
        """
        self.host = host
        self.api_url = f"{host}/api/generate"
        self.tags_url = f"{host}/api/tags"

    def check_model_availability(self, model_name: str) -> bool:
        """
        Checks if a specific model is available on the Ollama server.

        Args:
            model_name (str): The name of the model to check.

        Returns:
            bool: True if the model is available, False otherwise.
        """
        try:
            response = requests.get(self.tags_url, timeout=10)
            response.raise_for_status()
            models = response.json().get('models', [])
            # Model names can have tags, e.g., 'llama3:latest'
            available_models = [m['name'].split(':')[0] for m in models]
            return model_name in available_models
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama at {self.host}: {e}", file=sys.stderr)
            print("Please ensure Ollama is running and accessible.", file=sys.stderr)
            sys.exit(1)

    def generate(self, prompt: str, model: str) -> str:
        """
        Sends a prompt to the Ollama API and streams the response.

        Args:
            prompt (str): The input prompt for the language model.
            model (str): The name of the model to use.

        Returns:
            str: The complete, concatenated response from the model.
        """
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False, # Set to False for a single response object
        }

        try:
            with requests.post(self.api_url, json=payload, stream=False, timeout=300) as response:
                response.raise_for_status()
                response_data = response.json()
                return response_data.get('response', '').strip()

        except requests.exceptions.RequestException as e:
            print(f"Error during API request to Ollama: {e}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error decoding JSON response from Ollama.", file=sys.stderr)
            sys.exit(1)
