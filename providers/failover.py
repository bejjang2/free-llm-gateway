"""Failover manager for automatic provider switching."""

from dataclasses import dataclass, field
from typing import Any

from loguru import logger


@dataclass
class FailoverState:
    """State tracking for failover."""

    provider: str
    retry_count: int = 0
    last_error: str | None = None


class FailoverManager:
    """Manages automatic failover between providers based on priority and availability."""

    def __init__(
        self,
        enabled: bool = False,
        priority: list[str] | None = None,
        max_retries: int = 2,
        fallback_to_local: bool = True,
    ):
        self.enabled = enabled
        self.priority = priority or []
        self.max_retries = max_retries
        self.fallback_to_local = fallback_to_local

        # Track state per provider
        self._states: dict[str, FailoverState] = {}
        self._current_index: int = 0

        # Local providers (no API key needed)
        self._local_providers = {"ollama", "lmstudio"}

    def reset(self) -> None:
        """Reset failover state."""
        self._states.clear()
        self._current_index = 0

    def get_next_provider(
        self,
        requested_provider: str,
        available_providers: list[str],
    ) -> str | None:
        """Get the next available provider based on failover strategy.

        Args:
            requested_provider: The primary provider that was requested
            available_providers: List of provider types that have valid API keys

        Returns:
            Next provider to try, or None if no more providers available
        """
        if not self.enabled:
            return None

        # If this provider hasn't been tried yet, initialize it
        if requested_provider not in self._states:
            self._states[requested_provider] = FailoverState(provider=requested_provider)

        state = self._states[requested_provider]

        # Check if we should try next provider
        if state.retry_count >= self.max_retries:
            next_provider = self._find_next_in_priority(requested_provider, available_providers)
            if next_provider:
                logger.info(
                    "FAILOVER: '{}' exceeded max retries ({}), switching to '{}'",
                    requested_provider,
                    self.max_retries,
                    next_provider,
                )
                self._current_index = self.priority.index(next_provider) if next_provider in self.priority else 0
                return next_provider
            return None

        return None

    def _find_next_in_priority(
        self,
        current: str,
        available: list[str],
    ) -> str | None:
        """Find the next available provider in priority order."""
        if not self.priority:
            # No priority defined, try any available provider
            for p in available:
                if p != current and p in self._states:
                    state = self._states[p]
                    if state.retry_count < self.max_retries:
                        return p
            return None

        try:
            current_idx = self.priority.index(current)
        except ValueError:
            current_idx = -1

        # Try providers after current in priority list
        for i in range(current_idx + 1, len(self.priority)):
            provider = self.priority[i]
            if provider in available and self._should_try_provider(provider):
                return provider

        # Try providers before current in priority list (wrap around)
        for i in range(0, current_idx):
            provider = self.priority[i]
            if provider in available and self._should_try_provider(provider):
                return provider

        # If no providers in priority, try any available
        if not self.priority:
            for p in available:
                if p != current and self._should_try_provider(p):
                    return p

        return None

    def _should_try_provider(self, provider: str) -> bool:
        """Check if a provider should be tried based on its state."""
        state = self._states.get(provider)
        if state is None:
            return True
        return state.retry_count < self.max_retries

    def record_failure(self, provider: str, error: str) -> None:
        """Record a failure for a provider."""
        if provider not in self._states:
            self._states[provider] = FailoverState(provider=provider)
        self._states[provider].retry_count += 1
        self._states[provider].last_error = error
        logger.warning(
            "FAILOVER: '{}' failure #{}/{}: {}",
            provider,
            self._states[provider].retry_count,
            self.max_retries,
            error,
        )

    def record_success(self, provider: str) -> None:
        """Record a successful request for a provider."""
        if provider in self._states:
            self._states[provider].retry_count = 0
            self._states[provider].last_error = None

    def get_available_providers(
        self,
        settings: Any,
    ) -> list[str]:
        """Get list of providers that have valid API keys."""
        available = []

        # Check each provider for valid credentials
        if settings.nvidia_nim_api_key and settings.nvidia_nim_api_key.strip():
            available.append("nvidia_nim")

        if settings.open_router_api_key and settings.open_router_api_key.strip():
            available.append("open_router")

        if settings.deepseek_api_key and settings.deepseek_api_key.strip():
            available.append("deepseek")

        if settings.groq_api_key and settings.groq_api_key.strip():
            available.append("groq")

        if settings.together_api_key and settings.together_api_key.strip():
            available.append("together")

        # Local providers are always available
        if self.fallback_to_local:
            available.extend([p for p in ["ollama", "lmstudio"] if p not in available])

        return available

    def parse_priority(self, priority_str: str) -> list[str]:
        """Parse comma-separated priority string."""
        if not priority_str:
            return []
        return [p.strip() for p in priority_str.split(",") if p.strip()]


# Global failover manager instance
_failover_manager: FailoverManager | None = None


def get_failover_manager() -> FailoverManager:
    """Get or create the global failover manager."""
    global _failover_manager
    if _failover_manager is None:
        _failover_manager = FailoverManager()
    return _failover_manager


def init_failover_manager(
    enabled: bool = False,
    priority: str = "",
    max_retries: int = 2,
    fallback_to_local: bool = True,
) -> FailoverManager:
    """Initialize the global failover manager with settings."""
    global _failover_manager
    _failover_manager = FailoverManager(
        enabled=enabled,
        priority=[p.strip() for p in priority.split(",") if p.strip()],
        max_retries=max_retries,
        fallback_to_local=fallback_to_local,
    )
    return _failover_manager
