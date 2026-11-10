"""Notification transports resource (``/api/notification-transport/``) — read-only.

The backend owns this collection: transports are fixed channels (``desktop``,
``email``, ``telegram``, ...). The client can only read them, so this resource
deliberately exposes no ``create`` / ``update`` / ``delete``.
"""

from __future__ import annotations

from typing import Any

from calendar_scripts.client import ApiClient
from calendar_scripts.models.notification_transport import (
    NotificationTransport as NotificationTransportModel,
)


class NotificationTransport:
    """Notification transports: read-only ``list`` / ``get``."""

    path = "/api/notification-transport/"
    model = NotificationTransportModel

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def list(self, **params: Any) -> list[NotificationTransportModel]:
        """Fetch the (first page of the) transport list.

        Any keyword arguments are passed as query parameters.
        """
        data = self._client.get(self.path, params=params or None)
        if isinstance(data, dict):
            items = data.get("results", [])
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return [self.model.model_validate(item) for item in items]

    def search(self, search: str, **params: Any) -> list[NotificationTransportModel]:
        """Search transports by name (``?search=<...>``)."""
        return self.list(search=search, **params)

    def get(self, id: int) -> NotificationTransportModel:
        """Fetch a single transport by id."""
        data = self._client.get(f"{self.path}{id}/")
        return self.model.model_validate(data)
