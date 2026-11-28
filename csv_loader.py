"""CSV loading for the Study Session Planner.

Reads task rows from a CSV file and passes them to validation.
Expected columns: id, name, duration, score.
"""
import csv
import io
import os

from validation import REQUIRED_FIELDS, ValidationError, validate_tasks


def read_csv_text(text):
    """Parse CSV text with a header row and return validated tasks."""
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        return []

    headers = [name.strip().lower() for name in reader.fieldnames]
    missing = [field for field in REQUIRED_FIELDS if field not in headers]
    if missing:
        raise ValidationError(f"CSV is missing column(s): {', '.join(missing)}.")
    reader.fieldnames = headers

    # Row 1 is the header, so the first task is on row 2.
    return validate_tasks(list(reader), first_row=2)


def load_tasks_from_csv(source):
    """Load tasks from a file path or an open file (such as a Streamlit upload)."""
    if isinstance(source, (str, os.PathLike)):
        with open(source, newline="", encoding="utf-8-sig") as file:
            return read_csv_text(file.read())

    data = source.read()
    if isinstance(data, bytes):
        data = data.decode("utf-8-sig")
    return read_csv_text(data)
