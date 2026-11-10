# calendar_scripts

A small client library for the calendar/trainer backend, made for scripts that
the backend runs as *handlers*.

The whole idea in one snippet:

```python
from calendar_scripts.models import Exercise

for exercise in Exercise.objects():
    print(exercise.id, exercise.name.value)
```

No client, no setup, no configuration — import the model and call it. The
client is created lazily inside the library from two environment variables:
`base_url` and `jwt_token` (the backend always sets them for a running script).

## Install

```bash
pip install -e .
```

## Models speak to the backend themselves

Every model is a pydantic model **and** a client for its endpoint:

| Call | HTTP |
|---|---|
| `Exercise.objects(**params)` | `GET /api/user-exercise/?params` |
| `Exercise.all(**params)` | same as `objects` |
| `Exercise.one(**params)` | first match, `LookupError` when nothing matches |
| `Exercise.get(id)` | `GET /api/user-exercise/<id>/` |
| `Exercise.create(**fields)` | `POST` |
| `Exercise.update(id, **fields)` | `PATCH` |
| `Exercise.delete(id)` | `DELETE` |
| `exercise.reload()` | re-read this object from the server |
| `exercise.delete_object()` | `DELETE` for this object |

The resource is derived from the class name: `Exercise` → `exercises`,
`RegularEvent` → `regular_events`, `NotificationTransport` →
`notification_transports`. A model that needs a different name sets
`resource_name` (see `ApiKey`).

Models contain only their fields plus methods specific to their endpoint:
`RegularEvent.events(...)`, `ApiKey.create_key(...)`, `Message.question(...)`.

## A script (handler)

```python
from calendar_scripts import get_handler_extra_data
from calendar_scripts.models import Message, NotificationTransport

def handle():
    params = get_handler_extra_data()          # {} if nothing was passed
    Message.simple_message(f"params: {params}", NotificationTransport.telegram())
```

`get_handler_extra_data()` reads the `handler_extra_data` environment variable
(JSON) — that is how the backend passes `extra_data` to a script.

## Notifications

```python
from calendar_scripts.models import Message, NotificationTransport

# Plain text
Message.simple_message("Hey!", NotificationTransport.telegram())

# Questions with buttons: {title, questions} goes to extra_data,
# notification_type becomes "notification_question"
Message.question("Pick one", questions, NotificationTransport.telegram())
```

Transports are positional — ids or `NotificationTransport` models. The shape of
a question is defined by the backend; the library passes it through.

## Encrypted fields

Text is sent as `{ "value": ..., "keys": [...] }` and modelled by
`LocalizedValue`: `field.value`, `field.keys`, `field.is_encrypted`. The library
does **not** encrypt or decrypt — send the pair back as you received it when you
do not change the field.

Server-side `?search=` matches the plain `value` only, so encrypted records are
skipped there. Filter on the client:

```python
matches = [e for e in Exercise.objects() if e.name.value == "N"]
```

## `PATCH` is a diff

`update(...)` sends only what you pass; a field you do not pass is not in the
body. Clearing a field needs an explicit `null`, which endpoints expose as a
flag (`clearTitle`, `clearName`) — not every endpoint has one yet.

## Constants

Model constants and enums are importable as-is:

```python
from calendar_scripts.models import Weekday, HabitReportStatus, ExtraFieldType
```

## Errors

Everything raises `ApiError` with a ready-to-show message:

```python
from calendar_scripts import ApiError

try:
    Exercise.objects()
except ApiError as e:
    print("Failed:", e)
```

## Explicit client (rare)

`CalendarClient` exists for hosts that manage several accounts or an explicit
token — for example to sign in once and hand the token to the environment:

```python
from calendar_scripts import CalendarClient

client = CalendarClient("http://127.0.0.1:8000")
print(client.auth.sign_in("user@example.com", "secret").access)
```

Scripts do not use it: without `jwt_token` in the environment nothing would
work anyway, and with it the default client is already ready.

## More

- `AGENTS.md` — rules and traps for anyone (human or AI) changing this library.
- `examples/` — runnable snippets, not shipped in the package.
