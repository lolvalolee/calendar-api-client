"""Resource classes, one per backend endpoint.

Each resource is named after the model it serves (``ApiKey``, ``Habit``, ...)
and lives in ``calendar_scripts.resources``; the models with the same names live
in ``calendar_scripts.models``.
"""

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
from calendar_scripts.resources.notification_transports import (
    NotificationTransport,
)
from calendar_scripts.resources.private_settings import PrivateSettings
from calendar_scripts.resources.profile import Profile
from calendar_scripts.resources.regular_events import RegularEvent
from calendar_scripts.resources.tags import Tag
from calendar_scripts.resources.trainings import Training

__all__ = [
    "Auth",
    "Condition",
    "ContentType",
    "CustomForm",
    "EncryptionKey",
    "Event",
    "Exercise",
    "Habit",
    "Handler",
    "MainPageDisplay",
    "Message",
    "Note",
    "NotificationTransport",
    "Profile",
    "PrivateSettings",
    "RegularEvent",
    "Tag",
    "Training",
]
