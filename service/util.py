from typing import Any
from datetime import datetime, timezone


def is_number(msg: str) -> bool:
    """Returns True if the input string represents a valid number, False otherwise."""
    msg = msg.strip()
    try:
        int(msg)
        return True
    except ValueError:
        return False


def convert_to_int(text: str | Any) -> int:
    text = str(text).strip()
    if is_number(text):
        return int(text)
    else:
        return 0


def get_current_utc_timestamp() -> str:
    """Returns the current UTC timestamp in ISO 8601 format with timezone awareness."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
