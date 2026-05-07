"""Together AI provider implementation."""

from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

from .request import build_request_body

TOGETHER_BASE_URL = "https://api.together.ai/v1"


class TogetherProvider(OpenAICompatibleProvider):
    """Together AI provider using OpenAI-compatible API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="TOGETHER",
            base_url=config.base_url or TOGETHER_BASE_URL,
            api_key=config.api_key,
        )

    def _build_request_body(self, request):
        """Internal helper for tests and shared building."""
        return build_request_body(request)
