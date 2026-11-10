"""API key model (``/api/key/``)."""

from __future__ import annotations

from calendar_scripts.models.base import BaseModel


class ApiKey(BaseModel):
    """A personal API key: ``{ "id": ..., "name": ..., "key": ... }``.

    Keys are created or deleted, never edited. A key is looked up by its name::

        from calendar_scripts.models import ApiKey

        key = ApiKey.get_object("deepseek")
        ApiKey.create_key("deepseek", "sk-...")
        key.delete_object()
    """

    #: Derived from the name would be ``api_keys``; kept explicit.
    resource_name = "api_keys"

    id: int = 0
    name: str = ""
    key: str = ""

    @classmethod
    def get_object(cls, name: str) -> ApiKey:
        """The key with this ``name``; ``LookupError`` if there is none.

        Several matches are not an error: the first one is used and a warning
        is logged.
        """
        return cls._res().one(search=name)

    @classmethod
    def create_key(cls, name: str, key: str) -> ApiKey:
        """Create a key with ``name`` and ``key`` (``POST /api/key/``)."""
        return cls._res().create_key(name=name, key=key)
