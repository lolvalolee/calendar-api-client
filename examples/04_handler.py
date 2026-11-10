"""A complete handler: the backend runs `handle()`.

Parameters come from the `handler_extra_data` environment variable (JSON).
The same script handles two cases:

* start — no params, pick an exercise by index `n` and send a question;
* answer — the user pressed a button, so `i` (exercise id) and `a` (action) come
  back in `handler_extra_data`.

Try it locally:

    handler_extra_data='{"n": 0}' python3 examples/04_handler.py
    handler_extra_data='{"i": 1, "a": 1}' python3 examples/04_handler.py
"""

import logging

from calendar_scripts import get_handler_extra_data
from calendar_scripts.models import Exercise, Message, NotificationTransport

logger = logging.getLogger(__name__)


def send_question(exercise: Exercise) -> None:
    """Ask the user what to do with one exercise."""
    questions = [
        {
            "title": "Increment",
            "action": {
                "type": "call_handler",
                "qs": {"name": "04_handler"},
                "handler_extra_data": {"i": exercise.id, "a": 1},
            },
        },
    ]
    Message.question("Warehouse items", questions, NotificationTransport.telegram())


def handle() -> None:
    params = get_handler_extra_data()
    logger.info("handler_extra_data=%s", params)

    # A button was pressed: the answer is already in the parameters.
    if (exercise_id := params.get("i")) is not None:
        exercise = Exercise.get(exercise_id)
        logger.info("action %s for exercise %s", params.get("a"), exercise.id)
        return

    # Start: take the exercise by index; nothing there — just stop.
    n = params.get("n", 0)
    try:
        exercise = Exercise.objects()[n]
    except IndexError:
        logger.info("fewer than %s exercises", n + 1)
        return

    send_question(exercise)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    handle()
