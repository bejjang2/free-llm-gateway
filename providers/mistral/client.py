"""mistral provider implementation."""

from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

from .request import build_request_body

MISTRAL_BASE_URL = "https://api.mistral.ai/v1"


class MistralProvider(OpenAICompatibleProvider):
    """mistral provider using OpenAI-compatible API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="mistral",
            base_url=config.base_url or MISTRAL_BASE_URL,
            api_key=config.api_key,
        )

    def _build_request_body(self, request):
        return build_request_body(request)
