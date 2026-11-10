"""Regular events resource (``/api/regular-event/``)."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.common import LocalizedValue
from calendar_scripts.models.regular_event import RegularEvent as RegularEventModel


class RegularEvent(BaseResource[RegularEventModel]):
    """Recurring events with the usual CRUD plus ``start`` / ``end``."""

    path = "/api/regular-event/"
    model = RegularEventModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_event(
        self,
        value: str,
        keys: list[str] | None = None,
        tags: list[str] | None = None,
        public: bool | None = None,
        max_duration: int | None = None,
        duration_required: bool | None = None,
    ) -> RegularEventModel:
        """Create an event from a name and optional settings.

        ``value`` is the name text (already encrypted if ``keys`` is given),
        ``keys`` are the encryption key names in encryption order, ``tags`` are
        tag names (the server creates missing tags itself).
        """
        payload: dict = {
            "name": {"value": value, "keys": keys or []},
            "tags": tags or [],
        }
        if public is not None:
            payload["public"] = public
        if max_duration is not None:
            payload["max_duration"] = max_duration
        if duration_required is not None:
            payload["duration_required"] = duration_required
        data = self._client.post(self.path, json=payload)
        return self._parse(data)

    def start(
        self,
        id: int,
        title: LocalizedValue,
        start: str,
    ) -> None:
        """Start an event (``POST <path><id>/start/``).

        ``title`` is the event name as it came from the server, ``start`` is an
        ISO datetime string with the profile timezone offset.
        """
        self._client.post(
            f"{self._item_path(id)}start/",
            json={"title": title.model_dump(), "start": start},
        )

    def end(self, id: int, end: str) -> None:
        """Finish an event (``POST <path><id>/end/``)."""
        self._client.post(f"{self._item_path(id)}end/", json={"end": end})

    def update_event(
        self,
        id: int,
        value: str,
        keys: list[str] | None = None,
        tags: list[str] | None = None,
        public: bool | None = None,
    ) -> RegularEventModel:
        """Update an event (``PATCH <path><id>/``).

        ``value`` is the name text (already encrypted if ``keys`` is given),
        ``keys`` are the encryption key names, ``tags`` are tag names.
        """
        payload: dict = {
            "name": {"value": value, "keys": keys or []},
            "tags": tags or [],
        }
        if public is not None:
            payload["public"] = public
        data = self._client.patch(self._item_path(id), json=payload)
        return self._parse(data)

    def delete_event(self, id: int) -> None:
        """Delete an event (``DELETE <path><id>/``)."""
        self._client.delete(self._item_path(id))
