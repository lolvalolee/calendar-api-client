"""Events resource (``/api/event/``).

Exposes ``current()`` (events happening now), ``end_event()`` and
``delete_event()``.
"""

from __future__ import annotations

from calendar_scripts.client import ApiClient
from calendar_scripts.models.event import Event as EventModel


class Event:
    """Read/act on events."""

    path = "/api/event/"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def current(self) -> list[EventModel]:
        """Return the list of current (active) events."""
        data = self._client.get(f"{self.path}current/")
        if isinstance(data, dict):
            items = data.get("results", [])
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return [Event.model_validate(item) for item in items]

    def list(self, **params: object) -> list[EventModel]:
        """List events (``GET <path>``) with optional query filters.

        Pass filters as keyword arguments, e.g. ``list(regular_event=20)``.
        """
        data = self._client.get(self.path, params=params or None)
        if isinstance(data, dict):
            items = data.get("results", [])
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return [Event.model_validate(item) for item in items]

    def for_regular_event(self, regular_event_id: int) -> list[EventModel]:
        """All events belonging to the regular event ``regular_event_id``."""
        return self.list(regular_event=regular_event_id)

    def end_event(self, id: int, end: str) -> None:
        """Finish an event (``POST <path><id>/end/``).

        ``end`` is an ISO datetime string with the profile timezone offset.
        """
        self._client.post(f"{self.path}{id}/end/", json={"end": end})

    def delete_event(self, id: int) -> None:
        """Delete an event (``DELETE <path><id>/``)."""
        self._client.delete(f"{self.path}{id}/")
