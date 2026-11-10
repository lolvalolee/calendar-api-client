"""Base classes for resources.

There are two kinds of resources:

* :class:`BaseResource` — a collection (``/api/thing/``) with standard CRUD:
  ``list`` / ``search`` / ``get`` / ``create`` / ``update`` / ``delete``.
* :class:`SingletonResource` — a single object with no ``id`` (e.g. the
  profile). It behaves like a singleton: always the same object, ``get`` /
  ``save``.

Subclasses set ``path`` and ``model`` and may add their own methods (like
``start`` / ``end`` for events) on top of the generic CRUD.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from calendar_scripts.client import ApiClient

logger = logging.getLogger(__name__)

ModelT = TypeVar("ModelT", bound=BaseModel)


def get_handler_extra_data() -> dict[str, Any]:
    """The ``extra_data`` the backend passed to the script being run.

    The backend runs a handler (script) and passes its ``extra_data`` as the
    ``handler_extra_data`` environment variable — a JSON object. Inside a
    script this is the only way to read the parameters configured in
    ``ACTION_RUN_SCRIPT``.

    When run outside a handler (or when the variable holds invalid JSON) it
    returns an empty dict, so scripts can always do
    ``params = get_handler_extra_data()`` without guarding.

    Example::

        from calendar_scripts import get_handler_extra_data

        params = get_handler_extra_data()
        report_date = params.get("report_date")
    """
    try:
        return json.loads(os.environ.get("handler_extra_data"))
    except (TypeError, json.JSONDecodeError):
        return {}


class BaseResource(Generic[ModelT]):
    """A collection endpoint with standard CRUD.

    ``path`` is the endpoint path with a trailing slash (e.g.
    ``"/api/user-habit/"``). ``model`` is the pydantic class used to parse
    server responses.
    """

    path: str = ""
    model: type[ModelT]

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    # ---- helpers -----------------------------------------------------------

    def _item_path(self, id: int) -> str:
        """Path of a single item: ``<path><id>/``."""
        return f"{self.path}{id}/"

    def _parse(self, data: Any) -> ModelT:
        """Parse one object from the server into ``self.model``."""
        return self.model.model_validate(data)

    def _parse_list(self, data: Any) -> list[ModelT]:
        """Parse a list response.

        Supports both a paginated response (``{ "results": [...] }``) and a
        plain list.
        """
        if isinstance(data, dict):
            items = data.get("results", [])
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return [self._parse(item) for item in items]

    # ---- generic CRUD ------------------------------------------------------

    def list(self, **params: Any) -> list[ModelT]:
        """Fetch the (first page of the) collection.

        Any keyword arguments are passed as query parameters.
        """
        data = self._client.get(self.path, params=params or None)
        return self._parse_list(data)

    def search(self, search: str, **params: Any) -> list[ModelT]:
        """Search the collection by a query string.

        ``search`` is sent as the ``search`` GET parameter; any extra keyword
        arguments are passed as additional query parameters (GET params).

        Only plain text is matched: the backend searches over the stored
        ``value`` as-is, so encrypted fields (``{value, keys}`` with non-empty
        ``keys``) are skipped. Filter those on the client instead.
        """
        return self.list(search=search, **params)

    def one(self, **params: Any) -> ModelT:
        """The first object matching ``params``.

        Shorthand for ``list(**params)`` that returns a single model instead
        of a list and raises :class:`LookupError` when nothing matched.
        If several objects matched, the first one is returned and a warning is
        logged — the query was expected to be precise.
        """
        items = self.list(**params)
        if not items:
            raise LookupError(f"No {self.model.__name__} matches {params!r}")
        if len(items) > 1:
            logger.warning(
                "Several %s objects match %r (%d), taking the first",
                self.model.__name__,
                params,
                len(items),
            )
        return items[0]

    def get(self, id: int) -> ModelT:
        """Fetch a single object by id."""
        data = self._client.get(self._item_path(id))
        return self._parse(data)

    def create(self, **fields: Any) -> ModelT:
        """Create an object from the given fields and return it."""
        data = self._client.post(self.path, json=fields)
        return self._parse(data)

    def update(self, id: int, **fields: Any) -> ModelT:
        """Partially update an object (PATCH) and return it."""
        data = self._client.patch(self._item_path(id), json=fields)
        return self._parse(data)

    def delete(self, id: int) -> None:
        """Delete an object by id."""
        self._client.delete(self._item_path(id))


class SingletonResource(Generic[ModelT]):
    """A single-object endpoint with no ``id`` (e.g. the profile).

    There is only ever one instance of this resource: you do not create it
    with arguments, you just call :meth:`get` / :meth:`save`.
    """

    path: str = ""
    model: type[ModelT]

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def get(self) -> ModelT:
        """Fetch the single object."""
        data = self._client.get(self.path)
        return self.model.model_validate(data)

    def save(self, **fields: Any) -> ModelT:
        """Update the single object (PATCH) and return it."""
        data = self._client.patch(self.path, json=fields)
        return self.model.model_validate(data)
