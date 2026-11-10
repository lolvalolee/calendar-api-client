"""Notes (comments) resource (``/api/comment/``)."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.note import Note as NoteModel


class Note(BaseResource[NoteModel]):
    """User notes with the usual CRUD."""

    path = "/api/comment/"
    model = NoteModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def create_note(
        self,
        value: str,
        keys: list[str] | None = None,
        tags: list[str] | None = None,
        object_id: int | None = None,
        content_type_id: int | None = None,
    ) -> NoteModel:
        """Create a note.

        ``value`` is the text (already encrypted if ``keys`` is given),
        ``tags`` are tag names. ``object_id`` + ``content_type_id`` optionally
        attach the note to another object.
        """
        payload: dict = {
            "text": {"value": value, "keys": keys or []},
            "tags": tags or [],
        }
        if object_id is not None:
            payload["object_id"] = object_id
        if content_type_id is not None:
            payload["content_type_id"] = content_type_id
        data = self._client.post(self.path, json=payload)
        return self._parse(data)
