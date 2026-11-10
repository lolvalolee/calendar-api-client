"""Send a question with buttons, like the old `question_v2`.

This example **sends a real notification** to the current user's desktop
transport.
"""

from calendar_scripts.models import Message, NotificationTransport

#: What the backend does when the button is pressed. It calls the handler named
#: in `qs.name` and puts `handler_extra_data` into that script's env variable.
ACTION_CALL_HANDLER = "call_handler"
HANDLER_NAME = "test"


def build_questions(exercise_id: int) -> list[dict]:
    return [
        {
            "title": "Increment",
            "action": {
                "type": ACTION_CALL_HANDLER,
                "qs": {"name": HANDLER_NAME},
                "handler_extra_data": {"i": exercise_id, "a": 1},
            },
        },
        {
            "title": "Skip",
            "action": {
                "type": ACTION_CALL_HANDLER,
                "qs": {"name": HANDLER_NAME},
                "handler_extra_data": {"i": exercise_id, "a": 2},
            },
        },
    ]


# Transports are positional: ids or NotificationTransport models.
Message.question(
    "Warehouse items",
    build_questions(exercise_id=1),
    NotificationTransport.desktop(),
)
print("question sent")  # real notification, check the app

# A plain text notification for comparison:
Message.simple_message("Hey!", NotificationTransport.desktop())
