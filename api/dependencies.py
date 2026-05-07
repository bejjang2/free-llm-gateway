"""Dependency injection for FastAPI."""

from fastapi import HTTPException
from loguru import logger

from config.settings import Settings
from config.settings import get_settings as _get_settings
from providers.base import BaseProvider, ProviderConfig
from providers.cerebras import CerebrasProvider
from providers.common import get_user_facing_error_message
from providers.deepseek import DeepSeekProvider
from providers.exceptions import AuthenticationError
from providers.github import GitHubProvider
from providers.groq import GroqProvider
from providers.lmstudio import LMStudioProvider
from providers.mistral import MistralProvider
from providers.nvidia_nim import NVIDIA_NIM_BASE_URL, NvidiaNimProvider
from providers.ollama import OllamaProvider
from providers.open_router import OPENROUTER_BASE_URL, OpenRouterProvider
from providers.sambanova import SambaNovaProvider
from providers.together import TogetherProvider
from providers.zhipu import ZhipuProvider
from providers.gemini import GeminiProvider, GEMINI_BASE_URL

# Provider registry: keyed by provider type string, lazily populated
_providers: dict[str, BaseProvider] = {}

# Base URLs
from providers.cerebras import CEREBRAS_BASE_URL
from providers.sambanova import SAMBANOVA_BASE_URL
from providers.mistral import MISTRAL_BASE_URL
from providers.github import GITHUB_BASE_URL
from providers.zhipu import ZHIPU_BASE_URL
from providers.deepseek import DEEPSEEK_BASE_URL
from providers.groq import GROQ_BASE_URL
from providers.together import TOGETHER_BASE_URL
from providers.gemini import GEMINI_BASE_URL


def get_settings() -> Settings:
    return _get_settings()


def _create_provider_for_type(provider_type: str, settings: Settings) -> BaseProvider:
    """Construct and return a new provider instance."""
    if provider_type == "nvidia_nim":
        if not settings.nvidia_nim_api_key or not settings.nvidia_nim_api_key.strip():
            raise AuthenticationError(
                "NVIDIA_NIM_API_KEY is not set. Add it to your .env file."
            )
        config = ProviderConfig(
            api_key=settings.nvidia_nim_api_key, base_url=NVIDIA_NIM_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout,
        )
        return NvidiaNimProvider(config, nim_settings=settings.nim)
    if provider_type == "open_router":
        if not settings.open_router_api_key or not settings.open_router_api_key.strip():
            raise AuthenticationError("OPENROUTER_API_KEY is not set.")
        config = ProviderConfig(
            api_key=settings.open_router_api_key, base_url=OPENROUTER_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout,
        )
        return OpenRouterProvider(config)
    if provider_type == "lmstudio":
        config = ProviderConfig(api_key="lm-studio", base_url=settings.lm_studio_base_url,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return LMStudioProvider(config)
    if provider_type == "ollama":
        config = ProviderConfig(api_key="ollama", base_url=settings.ollama_base_url,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return OllamaProvider(config)
    if provider_type == "deepseek":
        if not settings.deepseek_api_key or not settings.deepseek_api_key.strip():
            raise AuthenticationError("DEEPSEEK_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.deepseek_api_key, base_url=DEEPSEEK_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return DeepSeekProvider(config)
    if provider_type == "groq":
        if not settings.groq_api_key or not settings.groq_api_key.strip():
            raise AuthenticationError("GROQ_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.groq_api_key, base_url=GROQ_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return GroqProvider(config)
    if provider_type == "together":
        if not settings.together_api_key or not settings.together_api_key.strip():
            raise AuthenticationError("TOGETHER_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.together_api_key, base_url=TOGETHER_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return TogetherProvider(config)
    if provider_type == "cerebras":
        if not settings.cerebras_api_key or not settings.cerebras_api_key.strip():
            raise AuthenticationError("CEREBRAS_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.cerebras_api_key, base_url=CEREBRAS_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return CerebrasProvider(config)
    if provider_type == "sambanova":
        if not settings.sambanova_api_key or not settings.sambanova_api_key.strip():
            raise AuthenticationError("SAMBANOVA_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.sambanova_api_key, base_url=SAMBANOVA_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return SambaNovaProvider(config)
    if provider_type == "mistral":
        if not settings.mistral_api_key or not settings.mistral_api_key.strip():
            raise AuthenticationError("MISTRAL_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.mistral_api_key, base_url=MISTRAL_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return MistralProvider(config)
    if provider_type == "github":
        if not settings.github_api_key or not settings.github_api_key.strip():
            raise AuthenticationError("GITHUB_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.github_api_key, base_url=GITHUB_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return GitHubProvider(config)
    if provider_type == "zhipu":
        if not settings.zhipu_api_key or not settings.zhipu_api_key.strip():
            raise AuthenticationError("ZHIPU_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.zhipu_api_key, base_url=ZHIPU_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return ZhipuProvider(config)
    if provider_type == "gemini":
        if not settings.gemini_api_key or not settings.gemini_api_key.strip():
            raise AuthenticationError("GEMINI_API_KEY is not set.")
        config = ProviderConfig(api_key=settings.gemini_api_key, base_url=GEMINI_BASE_URL,
            rate_limit=settings.provider_rate_limit, rate_window=settings.provider_rate_window,
            max_concurrency=settings.provider_max_concurrency, http_read_timeout=settings.http_read_timeout,
            http_write_timeout=settings.http_write_timeout, http_connect_timeout=settings.http_connect_timeout)
        return GeminiProvider(config)
    supported = 'nvidia_nim, open_router, lmstudio, ollama, deepseek, groq, together, cerebras, sambanova, mistral, github, zhipu'
    raise ValueError(f"Unknown provider_type: '{provider_type}'. Supported: {supported}")


def get_provider_for_type(provider_type: str) -> BaseProvider:
    if provider_type not in _providers:
        try:
            _providers[provider_type] = _create_provider_for_type(provider_type, get_settings())
        except AuthenticationError as e:
            raise HTTPException(status_code=503, detail=get_user_facing_error_message(e)) from e
        logger.info("Provider initialized: {}", provider_type)
    return _providers[provider_type]


def get_provider() -> BaseProvider:
    return get_provider_for_type(get_settings().provider_type)


async def cleanup_provider():
    global _providers
    for provider in _providers.values():
        await provider.cleanup()
    _providers = {}
    logger.debug("Provider cleanup completed")
