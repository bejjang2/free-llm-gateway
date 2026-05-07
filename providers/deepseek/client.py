"""DeepSeek provider implementation."""

from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

from .request import build_request_body

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"


class DeepSeekProvider(OpenAICompatibleProvider):
    """DeepSeek provider using OpenAI-compatible API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="DEEPSEEK",
            base_url=config.base_url or DEEPSEEK_BASE_URL,
            api_key=config.api_key,
        )

    def _build_request_body(self, request):
        """Internal helper for tests and shared building."""
        return build_request_body(request)
