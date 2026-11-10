"""Profile resource (``/api/profile/``) — a singleton."""

from __future__ import annotations

from calendar_scripts.base import SingletonResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.auth import Profile as ProfileModel


class Profile(SingletonResource[ProfileModel]):
    """The current user profile.

    There is exactly one profile per user and no ``id`` in the URL, so this is
    a singleton: use ``get()`` to read it and ``save()`` to change fields.
    """

    path = "/api/profile/"
    model = ProfileModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)
