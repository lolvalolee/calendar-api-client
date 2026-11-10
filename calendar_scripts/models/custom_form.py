"""Custom form models (``/api/custom-form/``)."""

from __future__ import annotations

from pydantic import ConfigDict, Field

from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.common import ExtraFieldType, LocalizedValue


class CustomFormItem(BaseModel):
    """A single field definition inside a custom form.

    ``name`` — machine name, ``field_label`` — human label, ``data_type`` —
    one of ``string`` / ``int`` / ``datetime`` (see :class:`ExtraFieldType`).
    """

    id: int | None = None
    name: str = ""
    field_label: str = ""
    data_type: ExtraFieldType = ExtraFieldType.STRING


class CustomForm(BaseModel):
    """A user-defined form with its field definitions."""

    id: int = 0
    name: LocalizedValue = LocalizedValue()
    items: list[CustomFormItem] = Field(
        default=[], alias="custom_form_items"
    )

    model_config = ConfigDict(populate_by_name=True)
