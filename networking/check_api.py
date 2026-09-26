"""Data access for the operability-check service.

Reads a random open incident directly from the project's SQLite database
and formats it for JSON serving. This module has no Django dependency of
its own (same principle as ``ml/similarity.py``): it is a plain module that
the Flask app in ``networking/app.py`` calls, and that can be exercised
without starting Django.
"""

import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "src" / "db.sqlite3"

PRIORITY_LABELS = {"low": "Low", "medium": "Medium", "high": "High"}
STATUS_LABELS = {"open": "Open", "in_progress": "In progress", "closed": "Closed"}

RANDOM_INCIDENT_QUERY = """
    SELECT id, title, description, equipment, date, priority, status
    FROM incidents_incident
    WHERE status IN ('open', 'in_progress') AND is_archived = 0
    ORDER BY RANDOM()
    LIMIT 1
"""


def format_incident(row: sqlite3.Row) -> dict[str, Any]:
    """Turn a database row into a JSON-serializable incident dict.

    :param row: A row from ``incidents_incident`` with columns id, title,
        description, equipment, date, priority, status.
    :return: A dict with the same fields plus human-readable
        ``priority_display`` and ``status_display`` labels.
    """
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "equipment": row["equipment"],
        "date": row["date"],
        "priority": row["priority"],
        "priority_display": PRIORITY_LABELS.get(row["priority"], row["priority"]),
        "status": row["status"],
        "status_display": STATUS_LABELS.get(row["status"], row["status"]),
    }


def get_random_incident() -> dict[str, Any] | None:
    """Return a random incident that is neither archived nor closed.

    :return: A formatted incident dict, or ``None`` if there are no
        eligible incidents (all closed, archived, or the table is empty).
    """
    connection = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        row = connection.execute(RANDOM_INCIDENT_QUERY).fetchone()
    finally:
        connection.close()
    return format_incident(row) if row is not None else None
