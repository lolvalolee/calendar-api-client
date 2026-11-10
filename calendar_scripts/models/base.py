"""The base class every backend model inherits from.

A model is fully usable right after the import — no client, no setup::

    from calendar_scripts.models import Exercise

    for exercise in Exercise.objects():
        print(exercise.id)

How the request reaches the server: the model's class name is turned into a
resource name of the shared client (``Exercise`` -> ``exercises``,
``RegularEvent`` -> ``regular_events``, ``NotificationTransport`` ->
``notification_transports``). Models whose name does not follow that rule
override ``resource_name``.

:class:`BaseModel` is exported under the name ``BaseModel`` on purpose: models
import it from here instead of from ``pydantic``, so the base class can only be
one — ``calendar_scripts.models.base.BaseModel``.
"""

from __future__ import annotations

import re
import threading
from typing import Any, ClassVar

from pydantic import BaseModel as PydanticBaseModel

__all__ = ["BaseModel", "resource"]


def resource(name: str) -> Any:
    """A resource of the shared default client, by attribute name.

    ``name`` is the attribute on :class:`~calendar_scripts.calendar_client.
    CalendarClient`, e.g. ``"exercises"``, ``"messages"``, ``"regular_events"``.

    The import is local on purpose: ``calendar_client`` imports every resource,
    resources import models, so a module-level import here would form a cycle.
    """
    from calendar_scripts.calendar_client import default_client

    return getattr(default_client(), name)


def camel_to_snake(name: str) -> str:
    """``RegularEvent`` -> ``regular_event``, ``ApiKey`` -> ``api_key``."""
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()


class BaseModel(PydanticBaseModel):
    """Base for every model: knows the backend resource it belongs to.

    Subclasses must not do anything to become usable — the resource is derived
    from the class name (override ``resource_name`` when it differs, for
    example ``Exercise`` -> ``exercises``).

    Working with the backend from a model::

        Exercise.objects()                # GET /api/user-exercise/
        Exercise.objects(ordering="id")   # the same, with query parameters
        Exercise.one(id=1)                # the first match, LookupError if none
        exercise = Exercise.get(1)        # GET /api/user-exercise/1/
        exercise.reload()                 # re-read from the server
        exercise.delete_object()          # DELETE /api/user-exercise/1/

    Fields are optional by default (``None``) so a response that omits a key
    never fails to parse; models that need a stricter shape add their own.
    """

    #: Attribute name on ``CalendarClient``; derived from the class name.
    resource_name: ClassVar[str] = ""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.resource_name:
            cls.resource_name = camel_to_snake(cls.__name__) + "s"

    # ---- the resource of this model ---------------------------------------

    @classmethod
    def _res(cls) -> Any:
        """The backend resource for this model (``client.exercises`` etc.)."""
        return resource(cls.resource_name)

    # ---- reading ----------------------------------------------------------

    @classmethod
    def objects(cls, **params: Any) -> list["BaseModel"]:
        """Fetch a collection; keyword arguments are query parameters."""
        return cls._res().list(**params)

    #: Old name kept so scripts read naturally: ``all(...)`` / ``objects()``.
    all = objects

    @classmethod
    def one(cls, **params: Any) -> "BaseModel":
        """The first object matching ``params``; ``LookupError`` if none."""
        return cls._res().one(**params)

    @classmethod
    def get(cls, id: int) -> "BaseModel":
        """One object by id."""
        return cls._res().get(id)

    # ---- writing ----------------------------------------------------------

    @classmethod
    def create(cls, **fields: Any) -> "BaseModel":
        """Create an object from ``fields`` (``POST``) and return it."""
        return cls._res().create(**fields)

    @classmethod
    def update(cls, id: int, **fields: Any) -> "BaseModel":
        """Partially update an object (``PATCH``) and return it."""
        return cls._res().update(id, **fields)

    @classmethod
    def delete(cls, id: int) -> None:
        """Delete an object by id."""
        cls._res().delete(id)

    # ---- on an instance ---------------------------------------------------

    def reload(self) -> "BaseModel":
        """Re-read this object from the server and return the fresh copy.

        Not ``refresh``: ``AuthSession`` has a token field called ``refresh``,
        so a method with that name would shadow it.
        """
        return type(self).get(self._model_id())

    def delete_object(self) -> None:
        """Delete this object from the server."""
        type(self).delete(self._model_id())

    def _model_id(self) -> int:
        """The ``id`` field of this object."""
        return getattr(self, "id")
