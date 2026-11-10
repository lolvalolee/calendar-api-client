"""Condition model (``/api/condition/``) and its constants.

The constant classes below mirror the backend wire values one-to-one and are
used in ``Condition`` (``section``, ``case``, ``action``) and in ``extra_data``
keys (``ConditionField``).
"""

from __future__ import annotations

from pydantic import model_validator

from calendar_scripts.models.base import BaseModel
from calendar_scripts.models.common import LocalizedValue


class ConditionSection:
    """Rule sections (``section``)."""

    EVENT_REGULAR = "SECTION_EVENT_REGULAR"
    CALENDAR = "SECTION_CALENDAR"
    COMMON = "SECTION_COMMON"
    HABIT = "SECTION_HABIT"
    MEAL = "SECTION_MEAL"
    PARAM = "SECTION_PARAM"
    TRAINING = "SECTION_TRAINING"
    STOCK = "SECTION_STOCK"


class ConditionCase:
    """Events (``case``) that trigger a rule."""

    NOT_STARTED = "CASE_NOT_STARTED"
    REGULAR_EVENT_FINISHED = "CASE_REGULAR_EVENT_FINISHED"
    REGULAR_EVENT_POST_FINISHED = "CASE_REGULAR_EVENT_POST_FINISHED"
    REGULAR_EVENT_STARTED = "CASE_REGULAR_EVENT_STARTED"
    REGULAR_INCOMING = "CASE_REGULAR_INCOMING"

    EXACT_TIME = "CASE_EXACT_TIME"
    EXACT_TIME_CRON = "CASE_EXACT_TIME_CRON"
    REPORTED = "CASE_REPORTED"
    NOT_REPORTED_TILL = "CASE_NOT_REPORTED_TILL"
    MEAL_COMPLETED = "meal_completed"
    MEAL_COMPLETED_WITH_DEBT = "meal_completed_with_debt"
    INACTION = "CASE_INACTION"
    TRAINING_FINISHED = "CASE_TRAINING_FINISHED"
    ONGOING_DURATION_GREATER = "CASE_ONGOING_DURATION_GREATER"
    REGULAR_CANCELED = "CASE_REGULAR_CANCELED"
    USER_STOCK_ROOM_ITEM_ADDED = "CASE_USER_STOCK_ROOM_ITEM_ADDED"


class ConditionAction:
    """Actions (``action``) a rule performs."""

    SEND_NOTIFY = "ACTION_SEND_NOTIFY"
    RUN_SCRIPT = "ACTION_RUN_SCRIPT"
    APPLY_POINTS = "ACTION_APPLY_POINTS"
    ASK_ACCOMPLISH = "ACTION_ASK_ACCOMPLISH"


class ConditionField:
    """Names of keys in ``extra_data`` (and related places)."""

    EXACT_TIME = "exact_time"
    INACTION_DURATION = "inaction_duration"
    DURATION = "duration"
    CRON = "cron"
    TO = "to"
    RECORD = "record"
    POINT_DURATION = "point_duration"
    ACTION_NAME = "action_name"

    MESSAGE = "message"
    SCRIPT = "script"
    PATH = "path"
    HABIT_RESULT = "habit_result"
    NOT_REPORTED_TILL = "not_reported_till"


class Condition(BaseModel):
    """A rule: which object, on which event, doing which action.

    ``object`` is the object the rule is attached to (e.g. a habit). Its
    ``object_name`` may be encrypted. ``extra_data`` holds whatever the
    specific action/case needs.
    """

    id: int
    section: str = ""
    case: str = ""
    action: str = ""
    object_id: int | None = None
    content_type: int | None = None
    object_name: LocalizedValue = LocalizedValue()
    extra_data: dict | None = None

    @model_validator(mode="before")
    @classmethod
    def _flatten_object_name(cls, data: object) -> object:
        """Pull ``object.name`` up to ``object_name`` before validation.

        The backend nests the name under ``object``; the model exposes it as a
        flat ``object_name`` field, so we move it here.
        """
        if not isinstance(data, dict):
            return data
        obj = data.get("object")
        if isinstance(obj, dict):
            data = {**data, "object_name": obj.get("name") or {}}
        return data
