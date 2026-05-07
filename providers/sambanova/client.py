"""sambanova provider implementation."""

from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

from .request import build_request_body

SAMBANOVA_BASE_URL = "https://api.sambanova.ai/v1"


class SambaNovaProvider(OpenAICompatibleProvider):
    """sambanova provider using OpenAI-compatible API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="sambanova",
            base_url=config.base_url or SAMBANOVA_BASE_URL,
            api_key=config.api_key,
        )

    def _build_request_body(self, request):
        return build_request_body(request)
