"""Private settings model (``/api/private-settings/``).

There is exactly one settings record per user, and it can only be edited (no
create/delete). ``handler_repo`` is a plain string (not encrypted): a git
repository path in ``owner/name`` form.
"""

from __future__ import annotations
from calendar_scripts.models.base import BaseModel


class PrivateSettings(BaseModel):
    """User private settings."""

    handler_repo: str = ""
