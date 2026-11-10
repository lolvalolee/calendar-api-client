"""Library errors.

A single error type for everything: :class:`ApiError`. It carries the message
the server returned (the ``detail`` field), or a friendly generic message when
there was no response. Callers only need to catch one exception.
"""


class ApiError(Exception):
    """Any failure while talking to the API.

    ``message`` is a ready-to-show text. ``status`` is the HTTP status code
    (or ``None`` when the server could not be reached at all).
    """

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        return self.message
