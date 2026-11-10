"""API keys resource (``/api/key/``)."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.api_key import ApiKey as ApiKeyModel


class ApiKey(BaseResource[ApiKeyModel]):
    """Personal API keys: ``list`` / ``create`` / ``delete``."""

    path = "/api/key/"
    model = ApiKeyModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_key(self, name: str, key: str) -> ApiKeyModel:
        """Create a key (``POST <path>``) with a ``name`` and a ``key``."""
        data = self._client.post(self.path, json={"name": name, "key": key})
        return self._parse(data)

    def delete_key(self, id: int) -> None:
        """Delete a key (``DELETE <path><id>/``)."""
        self._client.delete(self._item_path(id))
