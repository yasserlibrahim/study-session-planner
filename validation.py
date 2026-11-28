"""Input validation for the Study Session Planner.

Checks task rows (from a CSV file or the interface) and the time budget
before any solver runs.
"""
from models import Task

REQUIRED_FIELDS = ("id", "name", "duration", "score")


class ValidationError(ValueError):
    """Raised when task data or the time budget is invalid."""


def parse_int(value, field, row_number):
    """Convert one cell to an integer, or raise a readable error."""
    try:
        return int(str(value).strip())
    except ValueError:
        raise ValidationError(
            f"Row {row_number}: '{field}' must be a whole number, got '{value}'."
        ) from None


def is_blank(value):
    """Return True when a cell is missing or contains only spaces."""
    return value is None or str(value).strip() == ""


def build_task(row, row_number):
    """Turn one row (a dict) into a Task after checking every field."""
    if row.get(None):
        raise ValidationError(f"Row {row_number}: too many values in this row.")
    for field in REQUIRED_FIELDS:
        if is_blank(row.get(field)):
            raise ValidationError(f"Row {row_number}: missing value for '{field}'.")

    duration = parse_int(row["duration"], "duration", row_number)
    score = parse_int(row["score"], "score", row_number)
    if duration <= 0:
        raise ValidationError(f"Row {row_number}: duration must be greater than 0.")
    if score < 0:
        raise ValidationError(f"Row {row_number}: score cannot be negative.")

    return Task(
        id=str(row["id"]).strip(),
        name=str(row["name"]).strip(),
        duration=duration,
        score=score,
    )


def validate_tasks(rows, first_row=1):
    """Validate a list of row dicts and return them as Task objects.

    Fully empty rows are skipped. Duplicate task IDs are rejected.
    first_row is the number shown in error messages for the first row.
    """
    tasks = []
    seen_ids = set()
    for row_number, row in enumerate(rows, start=first_row):
        if all(is_blank(row.get(field)) for field in REQUIRED_FIELDS):
            continue
        task = build_task(row, row_number)
        if task.id in seen_ids:
            raise ValidationError(f"Row {row_number}: duplicate task ID '{task.id}'.")
        seen_ids.add(task.id)
        tasks.append(task)
    return tasks


def validate_budget(value):
    """Return the time budget as a nonnegative integer number of minutes."""
    message = "Time budget must be a whole number of minutes."
    if isinstance(value, bool) or (isinstance(value, float) and not value.is_integer()):
        raise ValidationError(message)
    try:
        budget = int(str(int(value)) if isinstance(value, float) else str(value).strip())
    except ValueError:
        raise ValidationError(message) from None
    if budget < 0:
        raise ValidationError("Time budget cannot be negative.")
    return budget
