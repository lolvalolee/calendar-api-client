"""Event model (e.g. ``GET /api/event/current/``).

The endpoint returns a paginated list of these objects. ``title`` is a
localized value (may be encrypted). ``regular_event`` is the id of the parent
regular event (or ``None``), ``canceled`` tells whether the event was canceled,
``end`` is the finish time (or ``None`` while it is still running).
``extra_data`` is a free-form dict (structure not interpreted).
"""

from __future__ import annotations

from datetime import datetime


from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.common import LocalizedValue


class Event(BaseModel):
    """An event as returned by the event endpoints."""

    id: int
    title: LocalizedValue = LocalizedValue()
    start: datetime | None = None
    end: datetime | None = None
    regular_event: int | None = None
    canceled: bool = False
    event_type: str | None = None
    # Free-form subtasks, kept as raw dicts (structure not interpreted).
    sub_tasks: list[dict] = []
    # Free-form extra data, kept raw (structure not interpreted).
    extra_data: dict | None = None

    @property
    def is_running(self) -> bool:
        """True when the event has started and has not finished yet."""
        return self.start is not None and self.end is None
