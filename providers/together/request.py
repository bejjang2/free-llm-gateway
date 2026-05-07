"""Request builder for Together AI provider."""

from providers.common.message_converter import build_base_request_body

TOGETHER_DEFAULT_MAX_TOKENS = 8192


def build_request_body(request_data):
    """Build OpenAI-format request body from Anthropic request for Together."""
    return build_base_request_body(
        request_data, default_max_tokens=TOGETHER_DEFAULT_MAX_TOKENS
    )
