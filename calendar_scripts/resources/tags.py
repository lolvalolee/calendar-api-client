"""Tags resource (``/api/tag/``) — read-only."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.common import Tag as TagModel


class Tag(BaseResource[TagModel]):
    """Tags are plain names; the client only reads them."""

    path = "/api/tag/"
    model = TagModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)
