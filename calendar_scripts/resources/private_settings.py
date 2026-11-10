"""Private settings resource (``/api/private-settings/``) — a singleton."""

from __future__ import annotations

from calendar_scripts.base import SingletonResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.private_settings import (
    PrivateSettings as PrivateSettingsModel,
)


class PrivateSettings(SingletonResource[PrivateSettingsModel]):
    """The current user's private settings.

    Only one record exists per user, so this is a singleton: ``get()`` to read
    and ``save()`` to edit. There is no create/delete.
    """

    path = "/api/private-settings/"
    model = PrivateSettingsModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)
