"""Handlers (scripts) resource (``/api/handler/``) — list/search plus ``execute`` and ``delete``."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.common import Handler as HandlerModel


class Handler(BaseResource[HandlerModel]):
    """Handler/script list. Supports server-side ``search`` by name."""

    path = "/api/handler/"
    model = HandlerModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def search(self, query: str) -> list[HandlerModel]:
        """Return handlers whose name matches ``query`` (case-insensitive)."""
        return self.list(search=query)

    def execute(self, id: int) -> None:
        """Run a handler (``POST <path><id>/execute/``)."""
        self._client.post(f"{self._item_path(id)}execute/")

    def delete_handler(self, id: int) -> None:
        """Delete a handler (``DELETE <path><id>/``)."""
        self._client.delete(self._item_path(id))
