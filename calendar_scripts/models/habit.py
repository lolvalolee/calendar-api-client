"""Habit model (``/api/user-habit/``)."""

from __future__ import annotations

from enum import Enum

from pydantic import Field

from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.common import LocalizedValue


class HabitReportStatus(str, Enum):
    """Status of a habit report.

    The value is exactly what the backend expects in the ``status`` field.
    Being a ``str`` enum, it can be passed directly to ``report(...)``.
    """

    COMPLETED = "completed"
    SKIPPED = "skipped"
    FAILED = "failed"


class Habit(BaseModel):
    """A user habit.

    ``count_per_day`` is how many times the habit should be done per day.
    The backend field is called ``count_daily``; we expose it as
    ``count_per_day`` for readability.

    ``count_today`` is computed by the backend and only present in responses
    (it is not a writable field), so sending it in ``create``/``update`` is
    pointless — read it from a fetched object instead.
    """

    id: int
    name: LocalizedValue = LocalizedValue()
    count_per_day: int | None = Field(default=None, alias="count_daily")
    count_today: int | None = Field(default=None, exclude=True)
