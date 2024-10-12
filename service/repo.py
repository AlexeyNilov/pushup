from data.fastlite_db import DB
from sqlite_minutils.db import Database
from datetime import datetime, timezone


def get_current_utc_timestamp() -> str:
    """Returns the current UTC timestamp in ISO 8601 format with timezone awareness."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_pushup(value: int, user_id: int, db: Database = DB) -> dict:
    e = {"time": get_current_utc_timestamp(), "user_id": user_id, "value": value}
    event = db.t.event
    return event.insert(**e)


def is_number(msg: str) -> bool:
    """Returns True if the input string represents a valid number, False otherwise."""
    try:
        int(msg)
        return True
    except ValueError:
        return False
