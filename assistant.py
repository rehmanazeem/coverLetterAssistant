"""CoverLetterAssistant — Ollama-backed LLM wrapper for the cover letter pipeline."""

from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM


class CoverLetterAssistant:
    """Thin wrapper around an Ollama LLM for generating cover letter content."""

    def __init__(self, model_name: str, model_temperature: float = 0.6):
        """
        Args:
            model_name: Ollama model identifier (e.g. 'llama3.2').
            model_temperature: Sampling temperature; lower = more deterministic.
        """
        self.llm = OllamaLLM(model=model_name, temperature=model_temperature)
        self.output_parser = StrOutputParser()

    def get_response(self, messages) -> str:
        """Send a pre-formatted prompt to the LLM and return the string response."""
        return self.output_parser.parse(self.llm.invoke(messages))
