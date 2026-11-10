"""Exercises resource (``/api/user-exercise/``)."""

from __future__ import annotations

from typing import Any

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.exercise import Exercise as ExerciseModel


class Exercise(BaseResource[ExerciseModel]):
    """User exercises with the usual CRUD."""

    path = "/api/user-exercise/"
    model = ExerciseModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_exercise(
        self,
        value: str,
        keys: list[str] | None = None,
        extra_data: dict[str, Any] | None = None,
    ) -> ExerciseModel:
        """Create an exercise from a name and free-form ``extra_data``.

        ``value`` is the name (already encrypted if ``keys`` is given).
        """
        payload = {
            "name": {"value": value, "keys": keys or []},
            "extra_data": extra_data or {},
        }
        data = self._client.post(self.path, json=payload)
        return self._parse(data)

    def update_exercise(
        self,
        id: int,
        value: str,
        keys: list[str] | None = None,
        extra_data: dict[str, Any] | None = None,
    ) -> None:
        """Replace an exercise (``PUT <path><id>/``)."""
        self._client.put(
            self._item_path(id),
            json={
                "name": {"value": value, "keys": keys or []},
                "extra_data": extra_data or {},
            },
        )
