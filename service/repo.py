from data.fastlite_db import DB, EventNotFound
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


def get_sum_for_today(user_id: int, db: Database = DB) -> int:
    sql = f"SELECT SUM(value) FROM event WHERE user_id = {user_id} AND date(time) = date('now');"
    data = db.q(sql)
    if not data:
        raise EventNotFound
    return data[0]["SUM(value)"] or 0


def get_max_for_today(user_id: int, db: Database = DB) -> int:
    sql = f"SELECT MAX(value) FROM event WHERE user_id = {user_id} AND date(time) = date('now');"
    data = db.q(sql)
    if not data:
        raise EventNotFound
    return data[0]["MAX(value)"] or 0


def get_record(user_id: int, db: Database = DB) -> int:
    sql = f"SELECT MAX(value) FROM event WHERE user_id = {user_id};"
    data = db.q(sql)
    if not data:
        raise EventNotFound
    return data[0]["MAX(value)"] or 0
