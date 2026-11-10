# AGENTS.md — how to work with `calendar_scripts`

**Read this before writing any code that talks to the calendar/trainer backend.**

**These two files are the whole contract: `AGENTS.md` (how to work) and
`API.md` (what exists — models, fields, methods, constants).** Write code from
them alone; do not open the library sources to look something up.

**If a fact you need is missing from both files, add it to `API.md`** — a
documentation gap is a bug, not an excuse to read the code. Put the fact under
the right section; put anything not yet confirmed under "Known gaps".

---

## 1. The one rule that matters

**Import a model and use it. Never build a client in a script.**

```python
from calendar_scripts.models import Exercise

for exercise in Exercise.objects():
    print(exercise.id, exercise.name.value)
```

That is a complete, working program. The shared client is created lazily
inside the library from the `base_url` and `jwt_token` environment variables.

### Do NOT write any of this

```python
# ❌ the model already knows its resource
client = CalendarClient()
client.exercises.list()

# ❌ internal helper, not for scripts
from calendar_scripts.calendar_client import default_client
default_client().exercises.list()

# ❌ the model already knows its resource
from calendar_scripts.models.base import resource
resource("exercises").list()
```

`CalendarClient` still exists and is public, but it is for hosts that manage
several accounts or an explicit token. Scripts run by the backend never need
it — the user is fixed by `jwt_token`.

---

## 2. Every model is a resource client

All models in `calendar_scripts/models/` inherit one base class —
`calendar_scripts.models.base.BaseModel` — which already has everything:

| Call | HTTP |
|---|---|
| `Exercise.objects(**params)` | `GET /api/user-exercise/?params` |
| `Exercise.all(**params)` | same as `objects` |
| `Exercise.one(**params)` | first match, `LookupError` if none |
| `Exercise.get(id)` | `GET /api/user-exercise/<id>/` |
| `Exercise.create(**fields)` | `POST` |
| `Exercise.update(id, **fields)` | `PATCH` |
| `Exercise.delete(id)` | `DELETE` |
| `obj.reload()` | re-read from the server |
| `obj.delete_object()` | `DELETE` for this object |

**Never re-implement these per model.** A model contains only its fields plus
methods unique to that endpoint (e.g. `RegularEvent.events(...)`,
`ApiKey.create_key(...)`, `Message.question(...)`).

---

## 3. Envelope types that are *not* resources

`LocalizedValue`, `Tag`, `Handler`, `ContentType` also inherit the shared base
class, so they *have* `objects()` etc. — but there is no such resource for
them and calling it raises `AttributeError`. They are nested value objects:
use them as fields, never as resources.

---

## 4. Encrypted fields

A text field from the backend is `{ "value": "...", "keys": ["key_name", ...] }`
and is modelled by `LocalizedValue`:

```python
event.name.value          # the stored value (ciphertext when encrypted)
event.name.keys           # list of key names, or None
event.name.is_encrypted   # bool
```

The library **does not encrypt or decrypt**. Produce the pair yourself and
send it back unchanged when you do not touch the field.

**Search does not work on encrypted fields.** `?search=` matches the plain
`value` text on the server, so encrypted records are skipped. Filter on the
client when the field may be encrypted:

```python
matches = [e for e in Exercise.objects() if e.name.value == "N"]
```

---

## 5. `PATCH` is a diff

For `update(...)` only the fields you pass are sent. Passing `None` means
"do not touch" (the field is omitted from the body). To **clear** a field, the
endpoint needs an explicit `null` — that is a per-endpoint flag, not something
you get for free:

- events: `clearTitle: true` in the API layer, exposes as `"title": null`
- regular events: `clearName: true` → `"name": null`

If an endpoint has no such flag, it cannot be cleared from this library yet.

## 5.1 Empty values

Empty string after `trim()` is **not** automatically "clear" — the backend
decides. Do not invent messages: show the server's `detail`.

---

## 6. Scripts (handlers)

A script is a module with `handle()`. The backend passes parameters through the
`handler_extra_data` environment variable (JSON):

```python
from calendar_scripts import get_handler_extra_data

def handle():
    params = get_handler_extra_data()   # {} when absent or not valid JSON
    n = params.get("n", 0)
```

`get_handler_extra_data()` never raises — it returns `{}` on a missing
variable or broken JSON.

**Not every value in a script comes from the server.** Before writing
`params.get("x")`, establish where `x` comes from:

- **from the server** — it is passed through `handler_extra_data` (typically
  values typed into a condition or a form, or `action.handler_extra_data` of a
  notification button);
- **a constant** — it is defined in the script itself (`HABIT_NAME = "..."`).

If it is a constant, use it directly; do not invent a parameter, and do not
add "missing parameter" branches for something the backend never sends.
When unsure **ask** — do not guess.

---

## 7. Notifications

```python
from calendar_scripts.models import Message, NotificationTransport

Message.simple_message("Hey!", NotificationTransport.telegram())
Message.question("Pick one", questions, NotificationTransport.desktop())
```

Transports are passed **positionally** (ids or `NotificationTransport`
models). `question(...)` puts `{"title": ..., "questions": [...]}` into
`extra_data` and sets `notification_type = notification_question`. Question
objects are opaque to the library — send whatever the backend expects.

A button usually carries `action.handler_extra_data`; on click the backend
calls that handler again with those values in `handler_extra_data`. This is how
a script tells "start" from "the user pressed a button".

---

## 8. Traps

- **`reload()`, not `refresh()`.** `AuthSession` has a *field* `refresh`
  (the token); a method of that name would shadow it.
- **`id` is required on some models, optional (`= 0`) on others.** Follow the
  model; do not assume.
- **Import cycle.** `calendar_client` imports resources, resources import
  models. That is why `models/base.py` imports `default_client` **inside** the
  function. Do not move it to module level.
- **The plural `s` rule breaks on irregular plurals.** `ApiKey` derives to
  `api_keys` fine, but a future `Person`-style name would not. Always check the
  derived name against `CalendarClient` attributes; set `resource_name`
  explicitly when in doubt.
- **Only one base class.** Models import `BaseModel` from
  `calendar_scripts.models.base`, never from `pydantic`. Two different bases
  would silently break resource lookup.

---
