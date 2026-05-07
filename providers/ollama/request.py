"""Request builder for Ollama provider."""

from providers.common.message_converter import build_base_request_body

OLLAMA_DEFAULT_MAX_TOKENS = 81920


def build_request_body(request_data):
    """Build OpenAI-format request body from Anthropic request for Ollama."""
    return build_base_request_body(
        request_data, default_max_tokens=OLLAMA_DEFAULT_MAX_TOKENS
    )
