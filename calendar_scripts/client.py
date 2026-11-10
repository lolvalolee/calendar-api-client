"""HTTP client: one place that knows how to talk to the backend."""

from __future__ import annotations

import os
from typing import Any

import requests

from calendar_scripts.exceptions import ApiError

# Friendly messages for the most common network failures.
_TIMEOUT_MESSAGE = "Server is not responding. Check your connection."
_CONNECTION_MESSAGE = "Could not connect to the server."
_GENERIC_MESSAGE = "Request failed."

# Header carrying the library version, so the backend can tell which client
# sent the request (support, debugging, compatibility checks).
VERSION_HEADER = "X-Client-Version"


class ApiClient:
    """Thin wrapper over :class:`requests.Session`.

    Holds ``base_url`` and an optional access token, and turns HTTP responses
    into JSON (dict / list) or raises :class:`ApiError`. Higher-level resource
    classes use it; in simple scripts you create one client and share it.

    Both ``base_url`` and ``access_token`` fall back to the ``base_url`` and
    ``jwt_token`` environment variables, so in a container you can create the
    client with no arguments and still be configured correctly.

    Example::

        client = ApiClient("http://127.0.0.1:8000", access_token="...")
        client.get("/api/user-habit/")
    """

    def __init__(
        self,
        base_url: str | None = None,
        access_token: str | None = None,
        timeout: float = 15,
    ) -> None:
        # Explicit base_url wins; otherwise take it from the ``base_url`` env
        # var, then fall back to an empty value ("same host").
        self.base_url = (
            base_url if base_url is not None else os.environ.get("base_url", "")
        ).rstrip("/")
        # Explicit token wins; otherwise take it from the ``jwt_token`` env var.
        self.access_token = (
            access_token if access_token is not None else os.environ.get("jwt_token")
        )
        self.timeout = timeout
        self.session = requests.Session()

    def _headers(self) -> dict[str, str]:
        """Build request headers with ``Authorization`` and the client version.

        The token is read from ``os.environ["jwt_token"]`` on every request
        (falling back to ``self.access_token``), so the env var always wins
        when it is set.

        Every request also carries ``X-Client-Version: <library version>`` so
        the backend knows which library build it is talking to.
        """
        headers = {
            "Accept": "application/json",
            VERSION_HEADER: _library_version(),
        }
        token = os.environ.get("jwt_token") or self.access_token
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Perform a request and return parsed JSON (or ``None`` if empty).

        Raises :class:`ApiError` on any non-2xx response or network failure.
        """
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(
                method,
                url,
                json=json,
                params=params,
                headers=self._headers(),
                timeout=self.timeout,
            )
        except requests.Timeout as exc:
            raise ApiError(_TIMEOUT_MESSAGE) from exc
        except requests.ConnectionError as exc:
            raise ApiError(_CONNECTION_MESSAGE) from exc
        except requests.RequestException as exc:
            raise ApiError(_GENERIC_MESSAGE) from exc

        if not response.ok:
            raise ApiError(_error_message(response), status=response.status_code)

        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return None

    # Convenience shortcuts, so resources read naturally.
    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Any:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, **kwargs)


def _library_version() -> str:
    """Return the package version, read at call time.

    Imported inside the function on purpose: ``calendar_scripts.__init__``
    imports this module, so a module-level import would be circular.
    """
    from calendar_scripts import __version__

    return __version__


def _error_message(response: requests.Response) -> str:
    """Pick the most informative error text from a failed response."""
    try:
        data = response.json()
    except ValueError:
        data = None
    if isinstance(data, dict):
        detail = data.get("detail")
        if isinstance(detail, str) and detail:
            return detail
    return f"{_GENERIC_MESSAGE} (HTTP {response.status_code})"
