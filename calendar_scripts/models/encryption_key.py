"""Encryption key model (``/api/encryption-key/``)."""

from __future__ import annotations
from calendar_scripts.models.base import BaseModel


class EncryptionKey(BaseModel):
    """An encryption key.

    ``name`` is required, ``check_phrase`` is optional. Keys are created or
    deleted, never edited.
    """

    id: int = 0
    name: str = ""
    check_phrase: str | None = None
