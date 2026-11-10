"""calendar_scripts — a simple client library for the calendar/trainer backend.

The easiest way to use it from a script::

    from calendar_scripts.models import Message, NotificationTransport

    Message.simple_message("Hey!", NotificationTransport.desktop())

No client needs to be created explicitly: one is built under the hood from the
``base_url`` and ``jwt_token`` environment variables.

You can still create and configure a client yourself::

    from calendar_scripts import CalendarClient

    client = CalendarClient("http://127.0.0.1:8000")
    client.auth.sign_in("user@example.com", "secret")
    print(client.profile.get().display_name)
"""

from calendar_scripts.base import get_handler_extra_data
from calendar_scripts.calendar_client import (
    CalendarClient,
    default_client,
    set_default_client,
)
from calendar_scripts.client import ApiClient
from calendar_scripts.exceptions import ApiError

__all__ = [
    "CalendarClient",
    "ApiClient",
    "ApiError",
    "default_client",
    "get_handler_extra_data",
    "set_default_client",
]

__version__ = "0.0.1"
