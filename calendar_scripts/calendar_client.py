"""A high-level client that groups all resources in one place.

This is the easiest entry point for scripts: create a :class:`CalendarClient`,
(optionally) sign in, then use ``client.<resource>`` for everything.

Example::

    from calendar_scripts import CalendarClient

    client = CalendarClient("http://127.0.0.1:8000")
    client.auth.sign_in("user@example.com", "secret")

    habits = client.habits.list()
    for habit in habits:
        print(habit.id, habit.name.value)
"""

from __future__ import annotations

import threading

from calendar_scripts.client import ApiClient
from calendar_scripts.resources.auth import Auth
from calendar_scripts.resources.api_keys import ApiKey
from calendar_scripts.resources.conditions import Condition
from calendar_scripts.resources.content_types import ContentType
from calendar_scripts.resources.custom_forms import CustomForm
from calendar_scripts.resources.encryption_keys import EncryptionKey
from calendar_scripts.resources.events import Event
from calendar_scripts.resources.exercises import Exercise
from calendar_scripts.resources.habits import Habit
from calendar_scripts.resources.handlers import Handler
from calendar_scripts.resources.main_page_display import MainPageDisplay
from calendar_scripts.resources.messages import Message
from calendar_scripts.resources.notes import Note
from calendar_scripts.resources.notification_transports import NotificationTransport
from calendar_scripts.resources.private_settings import PrivateSettings
from calendar_scripts.resources.profile import Profile
from calendar_scripts.resources.regular_events import RegularEvent
from calendar_scripts.resources.tags import Tag
from calendar_scripts.resources.trainings import Training


class CalendarClient:
    """All API resources grouped behind one object.

    Pass ``base_url`` (e.g. ``"http://127.0.0.1:8000"``). Optionally pass an
    existing ``access_token`` to skip signing in.

    When omitted, ``base_url`` is taken from the ``base_url`` environment
    variable and the token from ``jwt_token``, so ``CalendarClient()`` works
    as-is inside a container.
    """

    def __init__(
        self,
        base_url: str | None = None,
        access_token: str | None = None,
        timeout: float = 15,
    ) -> None:
        self.api = ApiClient(base_url, access_token=access_token, timeout=timeout)

        self.auth = Auth(self.api)
        self.profile = Profile(self.api)
        self.private_settings = PrivateSettings(self.api)
        self.regular_events = RegularEvent(self.api)
        self.habits = Habit(self.api)
        self.trainings = Training(self.api)
        self.exercises = Exercise(self.api)
        self.events = Event(self.api)
        self.notes = Note(self.api)
        self.notification_transports = NotificationTransport(self.api)
        self.custom_forms = CustomForm(self.api)
        self.encryption_keys = EncryptionKey(self.api)
        self.api_keys = ApiKey(self.api)
        self.conditions = Condition(self.api)
        self.handlers = Handler(self.api)
        self.messages = Message(self.api)
        self.main_page_display = MainPageDisplay(self.api)
        self.tags = Tag(self.api)
        self.content_types = ContentType(self.api)


_default_lock = threading.Lock()
_default_client: CalendarClient | None = None


def default_client() -> CalendarClient:
    """The shared client, created lazily from the environment.

    Returns a single :class:`CalendarClient` built from the ``base_url`` and
    ``jwt_token`` environment variables. Call it from models/resources when no
    client was passed explicitly, so plain scripts need no setup at all::

        from calendar_scripts.models import Message, NotificationTransport

        def handle():
            Message.simple_message("Hey!", NotificationTransport.desktop())
    """
    global _default_client
    if _default_client is None:
        with _default_lock:
            if _default_client is None:
                _default_client = CalendarClient()
    return _default_client


def set_default_client(client: CalendarClient | None) -> None:
    """Override the shared client (mainly for tests); ``None`` resets it."""
    global _default_client
    with _default_lock:
        _default_client = client
