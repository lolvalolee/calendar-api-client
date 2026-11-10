"""Main page display resource (``/api/main-page-display/``) — entries shown on the main page, plus ``assign``."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.main_page_display import MainPageDisplayItem as MainPageDisplayItemModel


class MainPageDisplay(BaseResource[MainPageDisplayItemModel]):
    """Entries shown on the main page."""

    path = "/api/main-page-display/"
    model = MainPageDisplayItemModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)

    def assign(self, content_type_id: int, object_id: int) -> None:
        """Assign an object to the main page (``POST /api/dashboard/assign/``).

        ``content_type_id`` is the content type id (e.g. ``RegularEvent``),
        ``object_id`` is the id of the object itself.
        """
        self._client.post(
            "/api/dashboard/assign/",
            json={"content_type_id": content_type_id, "object_id": object_id},
        )
