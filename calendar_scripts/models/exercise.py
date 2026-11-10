"""User exercise model (``/api/user-exercise/``)."""

from __future__ import annotations

from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.common import LocalizedValue


class Exercise(BaseModel):
    """A user exercise.

    ``extra_data`` is a free-form dict with unpredictable keys, so it is kept
    as a plain ``dict`` instead of a fixed structure.

    Ready to use right after the import::

        from calendar_scripts.models import Exercise

        for exercise in Exercise.objects():
            print(exercise.id, exercise.name.value)
    """

    id: int = 0
    name: LocalizedValue = LocalizedValue()
    extra_data: dict | None = None
