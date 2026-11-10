"""Regular event model (``/api/regular-event/``)."""

from __future__ import annotations

from datetime import datetime
from enum import IntEnum

from pydantic import model_validator

from calendar_scripts.models.base import BaseModel, resource
from calendar_scripts.models.common import LocalizedValue, tag_names
from calendar_scripts.models.event import Event


class Weekday(IntEnum):
    """Weekdays as the backend expects them in ``weekdays`` (0 — Sunday … 6 — Saturday)."""

    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class RegularEvent(BaseModel):
    """A recurring event.

    ``weekdays`` holds weekday numbers (0 — Sunday … 6 — Saturday).
    ``tags`` is a list of tag names (plain strings, not encrypted).

    Work with it through the model itself, so no client has to be created::

        from calendar_scripts.models import RegularEvent

        workout = RegularEvent.get(1)
        workout.events(start__gte=..., end__lte=...)
    """

    id: int
    name: LocalizedValue = LocalizedValue()
    weekdays: list[int] | None = None
    public: bool = False
    delayed_start_at: datetime | None = None
    started_at: datetime | None = None
    max_duration: int | None = None
    duration_required: bool | None = None
    archived: bool = False
    tags: list[str] = []

    @model_validator(mode="before")
    @classmethod
    def _normalize_tags(cls, data: object) -> object:
        """The server sends ``tags`` as ``[{name}, ...]``; keep only names."""
        if isinstance(data, dict) and "tags" in data:
            data = {**data, "tags": tag_names(data["tags"])}
        return data

    # ---- access to the backend --------------------------------------------

    def events(self, **filters: object) -> list[Event]:
        """Events of this regular event, oldest first.

        ``filters`` are backend query parameters with Django-style lookups, so
        the filtering happens on the server::

            event.events(start__gte=since, end__lte=now)
            event.events(canceled=False)

        ``datetime`` values are sent as ISO strings. ``regular_event`` and
        ``ordering`` are always set by the model itself.
        """
        params = {"regular_event": self.id, "ordering": "start"}
        params.update(
            {
                key: value.isoformat() if isinstance(value, datetime) else value
                for key, value in filters.items()
            }
        )
        return resource("events").list(**params)
