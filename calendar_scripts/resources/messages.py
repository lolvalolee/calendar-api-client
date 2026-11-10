"""Messages resource (``/api/message/``)."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.message import Message as MessageModel


class Message(BaseResource[MessageModel]):
    """User messages (notifications)."""

    path = "/api/message/"
    model = MessageModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def unread(self) -> list[MessageModel]:
        """Return unread messages of the desktop channel."""
        return self.list(is_read="false", transport__name="desktop")

    def mark_read(self, id: int) -> None:
        """Mark a message as read (``POST <path><id>/read/``)."""
        self._client.post(f"{self._item_path(id)}read/")
