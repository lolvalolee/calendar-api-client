"""Message model (``/api/message/``)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar

from pydantic import model_validator

from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.notification_transport import NotificationTransport


class Message(BaseModel):
    """A user notification message.

    For ``notification_message`` type the title lives in ``extra_data.title``;
    we expose it as a flat ``title`` for convenience.

    For ``notification_question`` type ``extra_data`` holds ``title`` and
    ``questions`` — see :meth:`question`. For
    ``notification_habit_ask_complish`` see :meth:`habit_report_request`.

    ``transport`` is asymmetric on the wire: the server **returns** it as a
    name (``"desktop"``, ``"telegram"``), while creating a message needs its
    **id**. So the field holds the name when read, and
    :meth:`create`/*the helpers* accept either an id or a
    :class:`NotificationTransport` and send the id.
    """

    #: ``notification_type`` for a plain text message.
    NOTIFICATION_MESSAGE: ClassVar[str] = "notification_message"
    #: ``notification_type`` for a message that asks the user questions.
    NOTIFICATION_QUESTION: ClassVar[str] = "notification_question"
    #: ``notification_type`` for a request to report on a habit. The spelling
    #: (``complish``, not ``accomplish``) is the backend's and is matched
    #: literally by the client.
    NOTIFICATION_HABIT_ASK_COMPLISH: ClassVar[str] = (
        "notification_habit_ask_complish"
    )

    id: int
    notification_type: str = ""
    title: str = ""
    created: datetime | None = None
    #: Transport name as returned by the server (``"desktop"``,
    #: ``"telegram"``). Sent as an id — see :meth:`create`.
    transport: str = ""
    is_read: bool = False
    due_to: datetime | None = None
    processing: bool = False
    uuid: str | None = None
    content_object: dict | None = None
    content_object_verbose_name: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _pull_title(cls, data: object) -> object:
        """Move ``extra_data.title`` to ``title`` before validation."""
        if not isinstance(data, dict):
            return data
        extra = data.get("extra_data")
        if isinstance(extra, dict) and "title" in extra:
            data = {**data, "title": extra.get("title") or ""}
        return data

    @classmethod
    def create(cls, **fields: Any) -> "Message":
        """Create a message; ``transport`` may be an id or a transport model.

        The server returns ``transport`` as a name but expects an id when a
        message is created, so the value is converted here. ``extra_data``
        carries ``title`` (top-level ``title`` is mirrored from it on read).
        """
        transport = fields.pop("transport", None)
        if transport is not None:
            fields["transport"] = _transport_id(transport)
        return super().create(**fields)

    @classmethod
    def question(
        cls,
        title: str,
        questions: list[Any],
        *transports: int | NotificationTransport,
    ) -> list[Message]:
        """Create a question message for each of ``transports``.

        ``notification_type`` is ``notification_question`` and ``extra_data``
        carries ``{"title": title, "questions": questions}``. ``questions`` is
        passed to the server as-is (its shape is defined by the backend, so it
        is kept as a list of arbitrary JSON objects).

        ``transports`` may be transport ids or :class:`NotificationTransport`
        models (their ``id`` is used). Returns one created :class:`Message` per
        transport::

            Message.question(
                "Оціни тиждень",
                [{"id": "q1", "text": "Як пройшов?", "type": "select"}],
                NotificationTransport.telegram(),
            )
        """
        return [
            cls.create(
                notification_type=cls.NOTIFICATION_QUESTION,
                extra_data={"title": title, "questions": questions},
                transport=transport,
            )
            for transport in transports
        ]

    @classmethod
    def habit_report_request(
        cls,
        title: str,
        report_date: str,
        *transports: int | NotificationTransport,
    ) -> list[Message]:
        """Ask the user to report on a habit, once per ``transports`` entry.

        ``notification_type`` is ``notification_habit_ask_complish`` and
        ``extra_data`` carries ``{"title": title, "report_date": report_date}``.
        ``report_date`` is ``YYYY-MM-DD``; the client combines it with the time
        the user picks and sends the habit report. When ``report_date`` is
        missing the client falls back to today, so always pass it.

        ``transports`` may be transport ids or :class:`NotificationTransport`
        models (their ``id`` is used)::

            Message.habit_report_request(
                "Як пройшла зарядка?",
                "2026-10-25",
                NotificationTransport.desktop(),
            )
        """
        return [
            cls.create(
                notification_type=cls.NOTIFICATION_HABIT_ASK_COMPLISH,
                extra_data={"title": title, "report_date": report_date},
                transport=transport,
            )
            for transport in transports
        ]

    @classmethod
    def simple_message(
        cls,
        title: str,
        *transports: int | NotificationTransport,
    ) -> list[Message]:
        """Create a plain text message for each of ``transports``.

        ``transports`` may be transport ids or :class:`NotificationTransport`
        models (their ``id`` is used). Returns one created :class:`Message` per
        transport::

            Message.simple_message("Hey!", NotificationTransport.desktop())
        """
        return [
            cls.create(
                notification_type=cls.NOTIFICATION_MESSAGE,
                extra_data={"title": title},
                transport=transport,
            )
            for transport in transports
        ]


def _transport_id(transport: int | NotificationTransport) -> int:
    """Accept either a transport id or a model; return the id."""
    return transport.id if isinstance(transport, NotificationTransport) else transport
