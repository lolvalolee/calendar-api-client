"""Conditions resource (``/api/condition/``)."""

from __future__ import annotations

from typing import Any

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.condition import Condition as ConditionModel


class Condition(BaseResource[ConditionModel]):
    """Rules (conditions) for objects."""

    path = "/api/condition/"
    model = ConditionModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def for_object(self, object_id: int, content_type: int) -> list[ConditionModel]:
        """List conditions attached to a single object."""
        return self.list(object_id=object_id, content_type=content_type)

    def create_condition(
        self,
        section: str,
        object_id: int,
        content_type: int,
        case: str,
        action: str,
        extra_data: dict[str, Any] | None = None,
    ) -> None:
        """Create a rule (``POST <path>``).

        The backend returns no body here, so nothing is returned.
        """
        self._client.post(
            self.path,
            json={
                "section": section,
                "object_id": object_id,
                "content_type": content_type,
                "case": case,
                "action": action,
                "extra_data": extra_data or {},
            },
        )
