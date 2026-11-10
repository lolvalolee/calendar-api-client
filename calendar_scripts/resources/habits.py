"""Habits resource (``/api/user-habit/``)."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.habit import Habit as HabitModel


class Habit(BaseResource[HabitModel]):
    """User habits with the usual CRUD plus ``report``."""

    path = "/api/user-habit/"
    model = HabitModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_habit(
        self,
        value: str,
        keys: list[str] | None = None,
        count_per_day: int | None = None,
    ) -> HabitModel:
        """Create a habit from a name and optional daily count.

        ``value`` is the name (already encrypted if ``keys`` is given),
        ``keys`` are the encryption key names in encryption order.
        """
        payload: dict = {"name": {"value": value, "keys": keys or []}}
        if count_per_day is not None:
            payload["count_daily"] = count_per_day
        data = self._client.post(self.path, json=payload)
        return self._parse(data)

    def report(self, id: int, date: str, status: str) -> None:
        """Report a habit result (``POST <path><id>/report/``).

        ``status`` is one of ``completed`` / ``skipped`` / ``failed``.
        ``date`` is an ISO datetime string with the user's timezone offset.
        """
        self._client.post(
            f"{self._item_path(id)}report/",
            json={"date": date, "status": status},
        )
