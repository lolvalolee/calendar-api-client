"""Read a collection through the model alone — no client in the script."""

from calendar_scripts.models import Exercise

exercises = Exercise.objects()

print(f"found {len(exercises)} exercises")
for exercise in exercises:
    # name is a LocalizedValue: `value` + `keys` (encrypted when keys is set).
    print(exercise.id, exercise.name.value, exercise.extra_data)
