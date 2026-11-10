"""Trainings resource (``/api/user-training/``)."""

from __future__ import annotations

from typing import Any

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.training import Training as TrainingModel


class Training(BaseResource[TrainingModel]):
    """User trainings.

    Besides the generic CRUD, this adds ``create_training`` (which sends the
    nested structure the backend expects) and exercise actions
    ``mark_exercise_done`` / ``mark_exercise_skipped``.
    """

    path = "/api/user-training/"
    model = TrainingModel
    exercise_path = "/api/user-training-exercise/"

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_training(
        self,
        exercises: list[dict[str, Any]],
        event: dict[str, Any] | None = None,
        main_page_display: dict[str, Any] | None = None,
    ) -> TrainingModel:
        """Create a training (``POST <path>``).

        ``exercises`` is a list of ``{ user_exercise, count, position }``.
        ``event`` is ``{ title: {value, keys}, start, end }`` or ``None``.
        ``main_page_display`` is ``{ display_from, display_to }`` or ``None``.
        """
        payload = {
            "user_training_exercises": exercises,
            "event": event,
            "main_page_display": main_page_display,
        }
        data = self._client.post(self.path, json=payload)
        return self._parse(data)

    def mark_exercise_done(self, exercise_id: int, count: int) -> None:
        """Mark an assigned exercise as done (``PATCH user-training-exercise``).

        Sets ``done`` to ``True`` and ``count_done`` to the planned ``count``.
        """
        self._client.patch(
            f"{self.exercise_path}{exercise_id}/",
            json={"done": True, "count_done": count},
        )

    def mark_exercise_skipped(
        self,
        exercise_id: int,
        extra_data: dict[str, Any],
    ) -> None:
        """Mark an assigned exercise as skipped.

        ``extra_data`` is patched as-is, so callers should add
        ``{"skipped": "on"}`` themselves (keeping existing keys).
        """
        self._client.patch(
            f"{self.exercise_path}{exercise_id}/",
            json={"extra_data": extra_data},
        )
