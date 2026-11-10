"""Shared models used by several resources.

Everything here mirrors the backend JSON one-to-one. Fields that the server may
omit or send as ``null`` are optional (``None`` default) so parsing never fails.
"""

from __future__ import annotations

from enum import Enum

from pydantic import Field

from calendar_scripts.models.base import BaseModel


class ExtraFieldType(str, Enum):
    """Type of a value in ``extra_data`` / a custom form field.

    The backend does not send the type separately for ``extra_data``; it is
    inferred from the value. For custom form fields it comes as ``data_type``.
    ``wire`` is the exact string the backend uses.
    """

    STRING = "string"
    INTEGER = "int"
    DATETIME = "datetime"


class LocalizedValue(BaseModel):
    """Text field as the backend sends it: ``{ "value": ..., "keys": [...] }``.

    If ``keys`` is present, ``value`` is encrypted layer by layer with the
    passwords of those keys. The library does **not** decrypt anything yet; it
    only stores ``value`` and ``keys`` as they came.

    Note for searching: the backend's ``?search=`` matches plain ``value``
    text only, so encrypted records are skipped. Filter by decrypted text on
    the client when the field may be encrypted.
    """

    value: str = ""
    keys: list[str] | None = None

    @property
    def is_encrypted(self) -> bool:
        """True when the server sent a non-empty ``keys`` list."""
        return bool(self.keys)


class Tag(BaseModel):
    """A tag: ``{ "id": ..., "name": ... }``. The name is a plain string."""

    id: int
    name: str = ""


class ContentType(BaseModel):
    """A Django content type: ``{ "id": ..., "name": ... }``."""

    id: int
    name: str = ""


class Handler(BaseModel):
    """A handler/script entry from ``/api/handler/``.

    Used in conditions (``ACTION_RUN_SCRIPT``): we send the ``id`` in
    ``extra_data.script`` and show ``name``.
    """

    id: int
    name: str = ""
    path: str = ""


def tag_names(tags: object) -> list[str]:
    """Extract tag names from a backend list of ``{ "name": ... }`` objects.

    The backend may return ``None`` or an unexpected shape; we always give a
    clean ``list[str]`` and drop empty names.
    """
    if not isinstance(tags, list):
        return []
    names: list[str] = []
    for item in tags:
        if isinstance(item, dict):
            name = item.get("name")
            if isinstance(name, str) and name:
                names.append(name)
    return names
