"""All data models and their constants in one place, easy to import.

Example::

    from calendar_scripts.models import Habit, HabitReportStatus, Weekday
"""

from calendar_scripts.models.api_key import ApiKey
from calendar_scripts.models.auth import AuthSession, Profile
from calendar_scripts.models.common import (
    ContentType,
    ExtraFieldType,
    Handler,
    LocalizedValue,
    Tag,
)
from calendar_scripts.models.condition import (
    Condition,
    ConditionAction,
    ConditionCase,
    ConditionField,
    ConditionSection,
)
from calendar_scripts.models.custom_form import CustomForm, CustomFormItem
from calendar_scripts.models.encryption_key import EncryptionKey
from calendar_scripts.models.event import Event
from calendar_scripts.models.exercise import Exercise
from calendar_scripts.models.habit import Habit, HabitReportStatus
from calendar_scripts.models.main_page_display import MainPageDisplayItem
from calendar_scripts.models.message import Message
from calendar_scripts.models.note import Note
from calendar_scripts.models.notification_transport import NotificationTransport
from calendar_scripts.models.private_settings import PrivateSettings
from calendar_scripts.models.regular_event import RegularEvent, Weekday
from calendar_scripts.models.training import Training, TrainingEvent, TrainingExercise

__all__ = [
    "ApiKey",
    "AuthSession",
    "Profile",
    "ContentType",
    "ExtraFieldType",
    "Handler",
    "LocalizedValue",
    "Tag",
    "Condition",
    "ConditionAction",
    "ConditionCase",
    "ConditionField",
    "ConditionSection",
    "CustomForm",
    "CustomFormItem",
    "EncryptionKey",
    "Event",
    "Exercise",
    "Habit",
    "HabitReportStatus",
    "MainPageDisplayItem",
    "Message",
    "Note",
    "NotificationTransport",
    "PrivateSettings",
    "RegularEvent",
    "Weekday",
    "Training",
    "TrainingEvent",
    "TrainingExercise",
]
