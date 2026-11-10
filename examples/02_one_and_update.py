"""Find one object, patch a single field, re-read it from the server."""

from calendar_scripts.models import Exercise

# `one` takes query parameters and raises LookupError when nothing matches.
exercise = Exercise.one(id=1)

print("before:", exercise.extra_data)

# PATCH is a diff: only the keys you pass are sent. The others stay as they are.
updated = Exercise.update(exercise.id, extra_data={"from_example": True})
print("after: ", updated.extra_data)

# Re-read the same object fresh from the server.
print("reload:", exercise.reload().extra_data)
