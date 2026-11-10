"""Auth-related models."""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from calendar_scripts.models.base import BaseModel


class AuthSession(BaseModel):
    """Tokens returned by the sign-in endpoint.

    ``access`` is used for authorized requests, ``refresh`` can be used later to
    obtain a new access token without signing in again.
    """

    access: str | None = None
    refresh: str | None = None

    @property
    def is_logged_in(self) -> bool:
        """True when an access token is present."""
        return bool(self.access)


class Profile(BaseModel):
    """The current user profile from ``GET /api/profile/``.

    ``resource_name`` is explicit: the client attribute is ``profile``
    (singular, the resource is a singleton), while the derived name would be
    ``profiles``.

    The profile is a **singleton**: there is one per token, so instead of
    ``Profile.one()`` read the current one with :meth:`current`::

        profile = Profile.current()
        profile.timezone      # IANA name, e.g. "Europe/Kyiv"; may be None

    Only ``id`` is guaranteed; every other field may be ``None``.
    """

    resource_name = "profile"

    id: int
    first_name: str | None = None
    last_name: str | None = None
    telegram_nickname: str | None = None
    telegram_status: str | None = None
    timezone: str | None = None
    language: str | None = None
    image: str | None = None

    @classmethod
    def current(cls) -> "Profile":
        """The profile of the current user (the only one).

        The endpoint is a singleton: there is no collection and no ``id`` in
        the URL, so it is read with ``get()`` of the singleton resource — not
        with ``one()``, which would hit a list endpoint that does not exist.
        """
        from calendar_scripts.models.base import resource

        return resource(cls.resource_name).get()

    @property
    def tz(self) -> ZoneInfo | None:
        """The profile timezone, or ``None`` when it is not set or unknown."""
        if not self.timezone:
            return None
        try:
            return ZoneInfo(self.timezone)
        except Exception:
            return None

    def now(self) -> datetime:
        """Current time in the profile timezone (host zone when unset)."""
        return datetime.now(self.tz)

    def today(self) -> date:
        """Today's date in the profile timezone (host date when unset)."""
        return self.now().date()

    @property
    def display_name(self) -> str:
        """Full name, or the telegram nickname, or an empty string."""
        full = f"{self.first_name or ''} {self.last_name or ''}".strip()
        if full:
            return full
        return (self.telegram_nickname or "").strip()
