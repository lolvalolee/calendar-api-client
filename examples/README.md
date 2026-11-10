# examples

Runnable snippets showing how the library is used from a script.

They are **not** part of the package: `pyproject.toml` includes only
`calendar_scripts*`, so nothing here ships with the build.

## Requirements

The shared client is created from two environment variables:

```bash
export base_url="http://127.0.0.1:8000"
export jwt_token="<access token>"
```

Inside the backend the token is set for you; locally you can get one with:

```bash
python3 -c "
from calendar_scripts import CalendarClient
c = CalendarClient('http://127.0.0.1:8000')
print(c.auth.sign_in('user@example.com', 'secret').access)
"
```

## Running

```bash
python3 examples/01_list_exercises.py
```

Run them from the repository root (the directory that contains
`pyproject.toml`).

Examples that talk to the backend only read data unless their name says
otherwise (`03_send_question.py` does send a notification).

| File | Shows |
|---|---|
| `01_list_exercises.py` | `Model.objects()`, reading fields |
| `02_one_and_update.py` | `one`, `get`, `update` (PATCH diff), `reload` |
| `03_send_question.py` | `Message.question`, transports, button actions |
| `04_handler.py` | a full handler: `handle()`, `get_handler_extra_data()` |
