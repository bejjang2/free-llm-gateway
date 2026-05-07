"""zhipu provider implementation."""

from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

from .request import build_request_body

ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"


class ZhipuProvider(OpenAICompatibleProvider):
    """zhipu provider using OpenAI-compatible API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="zhipu",
            base_url=config.base_url or ZHIPU_BASE_URL,
            api_key=config.api_key,
        )

    def _build_request_body(self, request):
        return build_request_body(request)
