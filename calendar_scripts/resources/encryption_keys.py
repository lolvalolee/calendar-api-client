"""Encryption keys resource (``/api/encryption-key/``)."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.encryption_key import EncryptionKey as EncryptionKeyModel


class EncryptionKey(BaseResource[EncryptionKeyModel]):
    """Encryption keys.

    Keys are created or deleted, never edited, so editing is not provided.
    """

    path = "/api/encryption-key/"
    model = EncryptionKeyModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_key(self, name: str, check_phrase: str | None = None) -> EncryptionKeyModel:
        """Create a key with a name and optional check phrase."""
        payload: dict = {"name": name}
        if check_phrase:
            payload["check_phrase"] = check_phrase
        data = self._client.post(self.path, json=payload)
        return self._parse(data)
