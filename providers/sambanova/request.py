"""Request builder for sambanova provider."""

from providers.common.message_converter import build_base_request_body

SAMBANOVA_DEFAULT_MAX_TOKENS = 8192


def build_request_body(request_data):
    return build_base_request_body(
        request_data, default_max_tokens=SAMBANOVA_DEFAULT_MAX_TOKENS
    )
