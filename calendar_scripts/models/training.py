"""Training models (``/api/user-training/``)."""

from __future__ import annotations

from datetime import datetime

from pydantic import ConfigDict, Field

from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.common import LocalizedValue


class TrainingEvent(BaseModel):
    """The event attached to a training."""

    id: int = 0
    title: LocalizedValue = LocalizedValue()
    start: datetime | None = None


class TrainingExercise(BaseModel):
    """An exercise assigned inside a training.

    ``count`` — planned amount, ``count_done`` — done amount, ``position`` —
    order, ``done`` — whether it is finished. ``extra_data`` is a free-form
    dict (e.g. ``{"skipped": "on"}`` when the exercise is skipped).
    """

    id: int = 0
    exercise: "Exercise | None" = Field(default=None, alias="user_exercise")
    count: int = 0
    position: int = 0
    count_done: int = 0
    done: bool = False
    extra_data: dict | None = None

    model_config = ConfigDict(populate_by_name=True)

    @property
    def is_skipped(self) -> bool:
        """True when ``extra_data.skipped`` is set to a non-empty value."""
        value = (self.extra_data or {}).get("skipped")
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        return True


class Training(BaseModel):
    """A user training with its exercises and (optional) event."""

    id: int
    exercises: list[TrainingExercise] = Field(
        default=[], alias="user_training_exercises"
    )
    event: TrainingEvent | None = None
    status: str = ""
    extra_data: dict | None = None

    model_config = ConfigDict(populate_by_name=True)

    @property
    def exercises_count(self) -> int:
        """How many exercises are assigned to the training."""
        return len(self.exercises)


# Imported last to avoid a circular import (Exercise lives in its own module).
from calendar_scripts.models.exercise import Exercise  # noqa: E402

TrainingExercise.model_rebuild()
