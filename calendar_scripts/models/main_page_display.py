"""Main page display item model (``/api/main-page-display/``)."""

from __future__ import annotations

from datetime import datetime

from calendar_scripts.models.base import BaseModel


class MainPageDisplayItem(BaseModel):
    """A "show on main page" entry.

    Each entry points to some object via ``content_type_id`` +
    ``content_object``. The object type is a string in
    ``content_object_verbose_name`` (e.g. ``"UserTraining"``). Other types are
    not interpreted here; ``content_object`` is kept as a raw dict.
    """

    id: int
    position: int | None = None
    display_from: datetime | None = None
    display_to: datetime | None = None
    object_id: int | None = None
    content_type_id: int | None = None
    content_object_verbose_name: str = ""
    content_object: dict | None = None
