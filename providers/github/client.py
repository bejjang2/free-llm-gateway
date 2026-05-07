"""github provider implementation."""

from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

from .request import build_request_body

GITHUB_BASE_URL = "https://models.github.ai/inference"


class GitHubProvider(OpenAICompatibleProvider):
    """github provider using OpenAI-compatible API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="github",
            base_url=config.base_url or GITHUB_BASE_URL,
            api_key=config.api_key,
        )

    def _build_request_body(self, request):
        return build_request_body(request)
