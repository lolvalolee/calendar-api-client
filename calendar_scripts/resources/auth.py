"""Authentication resource (``/api/auth-token/signin/``)."""

from __future__ import annotations

from calendar_scripts.client import ApiClient
from calendar_scripts.models.auth import AuthSession


class Auth:
    """Sign-in helper.

    ``sign_in`` exchanges email and password for a token pair, and also stores
    the access token on the shared client so later requests are authorized.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def sign_in(self, email: str, password: str) -> AuthSession:
        """Exchange credentials for tokens and remember the access token."""
        data = self._client.post(
            "/api/auth-token/signin/",
            json={"email": email, "password": password},
        )
        session = AuthSession.model_validate(data)
        # Make the token available to every other resource using this client.
        self._client.access_token = session.access
        return session
