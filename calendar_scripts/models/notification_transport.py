"""Notification transport model (``/api/notification-transport/``).

A notification transport is a channel the backend can deliver notifications
through (for example ``desktop``, ``email``, ``telegram``). The list is
read-only: records are managed by the backend and cannot be created, edited or
deleted from the client.
"""

from __future__ import annotations

from calendar_scripts.models.base import BaseModel


class NotificationTransport(BaseModel):
    """A notification transport: ``{ "id": ..., "name": ... }``."""

    id: int
    name: str = ""

    @classmethod
    def desktop(cls) -> NotificationTransport:
        """The ``desktop`` transport: ``search("desktop")[0]``."""
        return cls._res().search("desktop")[0]

    @classmethod
    def telegram(cls) -> NotificationTransport:
        """The ``telegram`` transport: ``search("telegram")[0]``."""
        return cls._res().search("telegram")[0]
