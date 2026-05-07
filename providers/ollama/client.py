"""Ollama provider implementation."""

from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

from .request import build_request_body

OLLAMA_DEFAULT_BASE_URL = "http://localhost:11434/v1"


class OllamaProvider(OpenAICompatibleProvider):
    """Ollama provider using OpenAI-compatible local API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="OLLAMA",
            base_url=config.base_url or OLLAMA_DEFAULT_BASE_URL,
            api_key=config.api_key or "ollama",
        )

    def _build_request_body(self, request):
        """Internal helper for tests and shared building."""
        return build_request_body(request)
