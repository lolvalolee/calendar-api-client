"""Content types resource (``/api/content-type/``) — read-only, flat list."""

from __future__ import annotations

from calendar_scripts.base import BaseResource
from calendar_scripts.client import ApiClient
from calendar_scripts.models.common import ContentType as ContentTypeModel


class ContentType(BaseResource[ContentTypeModel]):
    """Content types. The server returns a flat list (no pagination), which
    :meth:`BaseResource._parse_list` already handles."""

    path = "/api/content-type/"
    model = ContentTypeModel

    def __init__(self, client: ApiClient) -> None:
        super().__init__(client)
