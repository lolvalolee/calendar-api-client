# `API.md` — reference for `calendar_scripts`

Read this together with `AGENTS.md`. `AGENTS.md` explains *how* to work
(import a model, never build a client); this file lists *what* exists —
models, fields, methods, constants.

**Rule: if the answer is not here or in `AGENTS.md`, do not read the library
sources — ask the user, then add the fact here.** This file must be complete
enough that a new contributor (human or AI) can write a working script from
these two documents alone.

Generated from the runtime (`model_fields`). If code and this file disagree,
**the code is right** and this file must be updated.

---

## 0. Minimal script

```python
import sys

from calendar_scripts import get_handler_extra_data
from calendar_scripts.models import Habit

sys.path.append('./')          # convention used by every script


def handle():
    params = get_handler_extra_data()      # dict; {} when absent/invalid
    for habit in Habit.objects():
        print(habit.id, habit.name.value, habit.count_today)
```

Entry point is always **`handle()`**. Parameters arrive as JSON in the
`handler_extra_data` environment variable and are read with
`get_handler_extra_data()` (never raises).

---

## 1. Shared model API (`BaseModel`)

Every model in `calendar_scripts.models` has:

| Call | HTTP | Returns |
|---|---|---|
| `Model.objects(**params)` | `GET /api/<res>/` | `list[Model]` |
| `Model.all(**params)` | same | `list[Model]` |
| `Model.one(**params)` | same | first match; `LookupError` if none |
| `Model.get(id)` | `GET /api/<res>/<id>/` | `Model` |
| `Model.create(**fields)` | `POST /api/<res>/` | created `Model` |
| `Model.update(id, **fields)` | `PATCH /api/<res>/<id>/` | updated `Model` |
| `Model.delete(id)` | `DELETE /api/<res>/<id>/` | `None` |
| `obj.reload()` | re-read from server | fresh `Model` |
| `obj.delete_object()` | `DELETE` for `obj.id` | `None` |

`kwargs` are query parameters (`objects`, `one`) or body fields
(`create`, `update`). `update` is a **diff**: only the fields you pass are
sent. `None` means "do not touch", not "clear" — clearing needs an
endpoint-specific flag (`clearTitle`, `clearName`).

`LocalizedValue`, `Tag`, `Handler`, `ContentType` also inherit `BaseModel` but
are **nested value objects**: use them as fields, not as resources
(`NotificationTransport` is the exception — it does have a resource).

---

## 2. Models — fields and `resource_name`

`resource_name` is derived from the class name (CamelCase → snake_case + `s`)
unless noted. It must match an attribute on `CalendarClient`.

### User and access

The profile is a **singleton per token** — there is exactly one, the current
user. Read it with `current()`, not `one()`:

```python
from calendar_scripts.models import Profile

profile = Profile.current()    # GET /api/profile/ — the only object, no id
profile.timezone               # IANA name, e.g. "Europe/Kyiv"; may be None
```

`Profile` is a **singleton resource**: the endpoint has no collection and no
`id` in the URL. Do not call `Profile.objects()`/`Profile.one()`/`Profile.get(id)`
on it — use `Profile.current()` to read and `profile.save(**fields)` (the
resource's PATCH) to change fields.

Date/time in the user's timezone (never use the host's clock):

| Call | Returns |
|---|---|
| `profile.now()` | `datetime` in the profile timezone |
| `profile.today()` | `date` in the profile timezone |
| `profile.tz` | `ZoneInfo` or `None` (unset/unknown name) |

When `timezone` is unset or unknown, these fall back to the host zone. Dates
that go to the backend as `YYYY-MM-DD` (e.g. `report_date` of a habit-report
request) are produced with `profile.today().isoformat()`.

| Model | resource | Fields |
|---|---|---|
| `Profile` | `profiles` | `id: int`, `first_name: str \| None`, `last_name: str \| None`, `telegram_nickname: str \| None`, `telegram_status: str \| None`, `timezone: str \| None`, `language: str \| None`, `image: str \| None` |
| `AuthSession` | — (not a resource) | `access: str \| None`, `refresh: str \| None` |
| `ApiKey` | `api_keys` | `id: int`, `name: str`, `key: str` |
| `EncryptionKey` | `encryption_keys` | `id: int`, `name: str`, `check_phrase: str \| None` |
| `PrivateSettings` | `private_settingss` | `handler_repo: str` |

### Habits

| Model | resource | Fields |
|---|---|---|
| `Habit` | `habits` | `id: int`, `name: LocalizedValue`, `count_per_day: int \| None` (alias `count_daily`), `count_today: int \| None` **read-only, computed by the server** |

`count_today` is present in responses only and is excluded from serialisation;
sending it in `create`/`update` has no effect.

### Events

| Model | resource | Fields |
|---|---|---|
| `Event` | `events` | `id: int`, `title: LocalizedValue`, `start: datetime \| None`, `end: datetime \| None`, `regular_event: int \| None`, `canceled: bool`, `event_type: str \| None`, `sub_tasks: list[dict]`, `extra_data: dict \| None` |
| `RegularEvent` | `regular_events` | `id: int`, `name: LocalizedValue`, `weekdays: list[int] \| None`, `public: bool`, `delayed_start_at: datetime \| None`, `started_at: datetime \| None`, `max_duration: int \| None`, `duration_required: bool \| None`, `archived: bool`, `tags: list[str]` |

`RegularEvent` also has `events(...)` — events of this regular event.

### Conditions

| Model | resource | Fields |
|---|---|---|
| `Condition` | `conditions` | `id: int`, `section: str`, `case: str`, `action: str`, `object_id: int \| None`, `content_type: int \| None`, `object_name: LocalizedValue`, `extra_data: dict \| None` |

### Exercises and trainings

| Model | resource | Fields |
|---|---|---|
| `Exercise` | `exercises` | `id: int`, `name: LocalizedValue`, `extra_data: dict \| None` |
| `Training` | `trainings` | `id: int`, `exercises: list[TrainingExercise]`, `event: TrainingEvent \| None`, `status: str`, `extra_data: dict \| None` |
| `TrainingExercise` | `training_exercises` | `id: int`, `exercise: Exercise \| None`, `count: int`, `position: int`, `count_done: int`, `done: bool`, `extra_data: dict \| None` |
| `TrainingEvent` | `training_events` | `id: int`, `title: LocalizedValue`, `start: datetime \| None` |

### Notes, custom forms, main page

| Model | resource | Fields |
|---|---|---|
| `Note` | `notes` | `id: int`, `text: LocalizedValue`, `tags: list[str]`, `created: datetime \| None` |
| `CustomForm` | `custom_forms` | `id: int`, `name: LocalizedValue`, `items: list[CustomFormItem]` |
| `CustomFormItem` | `custom_form_items` | `id: int \| None`, `name: str`, `field_label: str`, `data_type: ExtraFieldType` |
| `MainPageDisplayItem` | `main_page_display_items` | `id: int`, `position: int \| None`, `display_from: datetime \| None`, `display_to: datetime \| None`, `object_id: int \| None`, `content_type_id: int \| None`, `content_object_verbose_name: str`, `content_object: dict \| None` |

### Notifications

| Model | resource | Fields |
|---|---|---|
| `Message` | `messages` | `id: int`, `notification_type: str`, `title: str` (mirrored from `extra_data.title`), `created: datetime \| None`, `transport: str`, `is_read: bool`, `due_to: datetime \| None`, `processing: bool`, `uuid: str \| None`, `content_object: dict \| None`, `content_object_verbose_name: str \| None` — send via the helpers in §3 |
| `NotificationTransport` | `notification_transports` | `id: int`, `name: str` |

### Nested value objects

| Model | Fields |
|---|---|
| `LocalizedValue` | `value: str`, `keys: list[str] \| None` |
| `Tag` | `id: int`, `name: str` |
| `Handler` | `id: int`, `name: str`, `path: str` |
| `ContentType` | `id: int`, `name: str` |

---

## 3. Notifications

```python
from calendar_scripts.models import Message, NotificationTransport

# one transport
Message.simple_message("Text", NotificationTransport.telegram())

# the same text to both
Message.simple_message(
    "Text",
    NotificationTransport.telegram(),
    NotificationTransport.desktop(),
)

# question with buttons
Message.question("Title", [
    {"title": "No",  "action": {"type": "delete_notification",
                                "qs": {"name": "Sleep"}}},
    {"title": "Yes", "action": {"type": "start_regular_event",
                                "qs": {"name": "Sleep"}}},
], NotificationTransport.desktop())
```

- `simple_message(title, *transports) -> list[Message]` — one message per
  transport;
- `question(title, questions, *transports) -> list[Message]`;
- `transport` is **asymmetric**: the server returns it as a name
  (`"desktop"`, `"telegram"`), while creating a message needs its **id**.
  `Message.create(...)` accepts either an id or a `NotificationTransport` and
  sends the id; on a fetched message read `message.transport` as the name;
- transports are **positional**: an `int` id or a `NotificationTransport`;
- factories: `NotificationTransport.telegram()`,
  `NotificationTransport.desktop()`;
- the `questions` structure is opaque to the library — it is sent as is.

### Message types the frontend understands

The `notification_type` value decides how a message is rendered in the client.
Send **exactly** these strings — they are matched literally:

| `notification_type` | Meaning | `extra_data` |
|---|---|---|
| `notification_message` | plain text card | `title: str` |
| `notification_question` | card with buttons | `title: str`, `questions: list` |
| `notification_habit_ask_complish` | request for a habit report | `title: str`, `report_date: "YYYY-MM-DD"` |

Each type has a helper:

- `Message.NOTIFICATION_MESSAGE` — set by `Message.simple_message(...)`;
- `Message.NOTIFICATION_QUESTION` — set by `Message.question(...)`;
- `Message.NOTIFICATION_HABIT_ASK_COMPLISH` — set by
  `Message.habit_report_request(title, report_date, *transports)`.

**Habit report message** (`notification_habit_ask_complish`):

- note the spelling: `complish`, not `accomplish` (the backend type name);
- the client shows `extra_data.title` as the card text (falls back to a default
  when empty) and opens a dialog with four answers on tap;
- the answer is sent as a habit report dated `extra_data.report_date` combined
  with the time the user picks. `report_date` is `YYYY-MM-DD`; when it is
  missing, the client uses today's date, so always set it;
- only messages with `transport == "desktop"` are listed in the client, and
  unread ones only (`is_read == false`);

**Reading messages.** When a script fetches messages, it usually wants the
**unread** ones — that is what the client lists and that is what awaits the
user's answer:

```python
from calendar_scripts.models import Message

for message in Message.objects(is_read=False):
    ...
```

`is_read` works as a query parameter (verified). `transport` does **not** —
`?transport=desktop` is accepted but ignored (returns everything), so filter
the channel on the client, after fetching:

```python
desktop = [m for m in Message.objects(is_read=False) if m.transport == "desktop"]
```

**Sender side.** The library has a helper for each type — prefer them over
`Message.create(...)`: they set `notification_type`, `extra_data` and
`transport` correctly.

```python
from calendar_scripts.models import Message, NotificationTransport

Message.habit_report_request(
    "How was the habit?",
    "2026-10-25",
    NotificationTransport.desktop(),
)
```

---

## 4. Constants

### `ConditionCase` — the event that triggers a rule

| Constant | Value |
|---|---|
| `EXACT_TIME` | `CASE_EXACT_TIME` |
| `EXACT_TIME_CRON` | `CASE_EXACT_TIME_CRON` |
| `INACTION` | `CASE_INACTION` |
| `NOT_STARTED` | `CASE_NOT_STARTED` |
| `ONGOING_DURATION_GREATER` | `CASE_ONGOING_DURATION_GREATER` |
| `REGULAR_INCOMING` | `CASE_REGULAR_INCOMING` |
| `REGULAR_EVENT_STARTED` | `CASE_REGULAR_EVENT_STARTED` |
| `REGULAR_EVENT_FINISHED` | `CASE_REGULAR_EVENT_FINISHED` |
| `REGULAR_EVENT_POST_FINISHED` | `CASE_REGULAR_EVENT_POST_FINISHED` |
| `REGULAR_CANCELED` | `CASE_REGULAR_CANCELED` |
| `NOT_REPORTED_TILL` | `CASE_NOT_REPORTED_TILL` |
| `REPORTED` | `CASE_REPORTED` |
| `TRAINING_FINISHED` | `CASE_TRAINING_FINISHED` |
| `MEAL_COMPLETED` | `meal_completed` |
| `MEAL_COMPLETED_WITH_DEBT` | `meal_completed_with_debt` |
| `USER_STOCK_ROOM_ITEM_ADDED` | `CASE_USER_STOCK_ROOM_ITEM_ADDED` |

### `ConditionAction`

| Constant | Value |
|---|---|
| `SEND_NOTIFY` | `ACTION_SEND_NOTIFY` |
| `RUN_SCRIPT` | `ACTION_RUN_SCRIPT` |
| `APPLY_POINTS` | `ACTION_APPLY_POINTS` |
| `ASK_ACCOMPLISH` | `ACTION_ASK_ACCOMPLISH` |

### `ConditionField` — keys inside `Condition.extra_data`

| Constant | String |
|---|---|
| `EXACT_TIME` | `exact_time` |
| `INACTION_DURATION` | `inaction_duration` |
| `DURATION` | `duration` |
| `CRON` | `cron` |
| `TO` | `to` |
| `RECORD` | `record` |
| `POINT_DURATION` | `point_duration` |
| `ACTION_NAME` | `action_name` |
| `MESSAGE` | `message` |
| `SCRIPT` | `script` |
| `PATH` | `path` |
| `HABIT_RESULT` | `habit_result` |
| `NOT_REPORTED_TILL` | `not_reported_till` |

`ConditionField.DURATION` for `CASE_REGULAR_EVENT_POST_FINISHED` is an
**integer number of seconds**.

### `Weekday`

`MONDAY=1`, `TUESDAY=2`, `WEDNESDAY=3`, `THURSDAY=4`, `FRIDAY=5`,
`SATURDAY=6`, `SUNDAY=0`.

### `HabitReportStatus`

`COMPLETED='completed'`, `FAILED='failed'`, `SKIPPED='skipped'`.

---

## 5. Rules that are easy to get wrong

### Encrypted fields (`LocalizedValue`)

The server cannot search them: `?search=` and filters on `name`/`title`
return nothing for encrypted records. Filter on the client:

```python
matches = [h for h in Habit.objects() if h.name.value == "Exercise"]
```

The library neither encrypts nor decrypts. An untouched field is sent back
unchanged.

### Writing

`create`/`update` send only the keyword arguments you pass. Computed,
read-only fields (for example `Habit.count_today`) are never sent.

### Scripts

A script is a module with `handle()`; parameters come from
`get_handler_extra_data()`. See `AGENTS.md` §7.

---

## 6. Known gaps

Facts that are not confirmed yet, or are broken. Do not guess — ask, then move
the answer up into the right section.

- None at the moment.
