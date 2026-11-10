"""Note (comment) model (``/api/comment/``)."""

from __future__ import annotations

from datetime import datetime

from pydantic import model_validator

from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.common import LocalizedValue, tag_names


class Note(BaseModel):
    """A user note with text and tag names.

    ``text`` is a localized value (may be encrypted). ``tags`` is a list of
    plain tag names.
    """

    id: int
    text: LocalizedValue = LocalizedValue()
    tags: list[str] = []
    created: datetime | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_tags(cls, data: object) -> object:
        """The server sends ``tags`` as ``[{name}, ...]``; keep only names."""
        if isinstance(data, dict) and "tags" in data:
            data = {**data, "tags": tag_names(data["tags"])}
        return data
