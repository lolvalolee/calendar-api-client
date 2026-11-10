"""Custom forms resource (``/api/custom-form/``)."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.custom_form import CustomForm as CustomFormModel
from calendar_scripts.models.custom_form import CustomFormItem


class CustomForm(BaseResource[CustomFormModel]):
    """Custom forms. The backend does not support editing, so only create/get/list/delete."""

    path = "/api/custom-form/"
    model = CustomFormModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_form(
        self,
        value: str,
        keys: list[str] | None = None,
        items: list[CustomFormItem] | None = None,
    ) -> CustomFormModel:
        """Create a form from a name and field definitions.

        ``value`` is the form name (already encrypted if ``keys`` is given),
        ``items`` are the field definitions.
        """
        payload = {
            "name": {"value": value, "keys": keys or []},
            "custom_form_items": [
                item.model_dump(exclude_none=True) for item in (items or [])
            ],
        }
        data = self._client.post(self.path, json=payload)
        return self._parse(data)
