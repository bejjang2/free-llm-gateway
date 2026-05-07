"""Unified API Key Manager.

Implements freellmapi-style unified key system:
- Single free-llm-xxxx key for all providers
- Keys encrypted with AES-256-GCM in SQLite
- Per-key usage tracking
"""

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timezone

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from loguru import logger


class UnifiedKeyManager:
    """Manages unified API keys and encrypted provider keys."""

    KEY_PREFIX = "free-llm-"
    KEY_LENGTH = 32  # Random bytes for key (after prefix)

    def __init__(self, encryption_key: bytes):
        self._aesgcm = AESGCM(encryption_key)

    @classmethod
    def generate_system_key(cls) -> bytes:
        """Generate a random 32-byte encryption key for AES-256-GCM."""
        return os.urandom(32)

    @classmethod
    def generate_unified_key(cls) -> str:
        """Generate a new unified API key in free-llm-xxxx format."""
        random_part = secrets.token_hex(cls.KEY_LENGTH)
        return cls.KEY_PREFIX + random_part

    def hash_key(self, key: str) -> str:
        """Hash a unified key for storage lookup."""
        return hashlib.sha256(key.encode()).hexdigest()

    def encrypt_provider_key(self, provider_key: str) -> bytes:
        """Encrypt a provider API key with AES-256-GCM.
        
        Returns bytes: nonce (12) + tag (16) + ciphertext
        """
        nonce = os.urandom(12)
        encrypted = self._aesgcm.encrypt(nonce, provider_key.encode(), None)
        return nonce + encrypted

    def decrypt_provider_key(self, encrypted_data: bytes) -> str:
        """Decrypt a provider API key.
        
        Args:
            encrypted_data: nonce (12) + tag (16) + ciphertext
        """
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        return self._aesgcm.decrypt(nonce, ciphertext, None).decode()

    def verify_unified_key(self, key: str, stored_hash: str) -> bool:
        """Verify a unified key against its stored hash."""
        return hmac.compare_digest(
            self.hash_key(key),
            stored_hash
        )

    @staticmethod
    def format_timestamp(dt: datetime | None = None) -> str:
        """Format timestamp for ISO format."""
        dt = dt or datetime.now(timezone.utc)
        return dt.isoformat()


# Global instance
_key_manager: UnifiedKeyManager | None = None


def get_key_manager() -> UnifiedKeyManager:
    """Get or initialize the unified key manager."""
    global _key_manager
    if _key_manager is None:
        from config.settings import get_settings
        settings = get_settings()
        enc_key = settings.encryption_key
        if not enc_key:
            enc_key = secrets.token_hex(32)
            logger.warning("No ENCRYPTION_KEY set, generated temporary key")
        else:
            enc_key = bytes.fromhex(enc_key)
        _key_manager = UnifiedKeyManager(enc_key)
    return _key_manager
