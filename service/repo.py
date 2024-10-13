from data.fastlite_db import DB
from sqlite_minutils.db import Database
from datetime import datetime, timezone
from model.profile import Profile


class ProfileNotFound(Exception):
    pass


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
    sql = f"SELECT SUM(value) AS sum FROM event WHERE user_id = {user_id} AND date(time) = date('now');"
    data = db.q(sql)
    return data[0]["sum"] or 0


def get_max_for_today(user_id: int, db: Database = DB) -> int:
    sql = f"SELECT MAX(value) AS max_value FROM event WHERE user_id = {user_id} AND date(time) = date('now');"
    data = db.q(sql)
    return data[0]["max_value"] or 0


def get_max_all_time(user_id: int, db: Database = DB) -> int:
    sql = f"SELECT MAX(value) AS max_value FROM event WHERE user_id = {user_id};"
    data = db.q(sql)
    return data[0]["max_value"] or 0


def get_average(user_id: int, limit: int = 100, db: Database = DB) -> int:
    sql = f"""SELECT AVG(value) AS average_value
    FROM (
    SELECT value
    FROM event
    WHERE user_id = {user_id}
    ORDER BY time DESC
    LIMIT {limit}
    );"""
    data = db.q(sql)
    if data[0]["average_value"]:
        return int(round(data[0]["average_value"], 0))
    else:
        return 0


def update_profile(profile: dict, db: Database = DB) -> dict:
    table = db.t.profile
    return table.upsert(**profile)


def get_profile(user_id: int, db: Database = DB) -> Profile:
    try:
        data = db.t.profile[user_id]
    except Exception:
        raise ProfileNotFound
    return Profile(**data)


def activate_training(user_id: int, db: Database = DB):
    try:
        profile = get_profile(user_id=user_id, db=db)
    except ProfileNotFound:
        profile = Profile(user_id=user_id)

    profile.training_mode = "Program"
    profile.training_day = 0
    update_profile(dict(profile), db=db)


def sync_profile(user_id: int, db: Database = DB):
    try:
        old_profile = get_profile(user_id, db)
        sum_per_day_prev = old_profile.sum_per_day or 0
    except ProfileNotFound:
        sum_per_day_prev = 0

    sum_per_day = get_sum_for_today(user_id, db)
    max_all_time = get_max_all_time(user_id, db)
    profile = Profile(
        user_id=user_id,
        max_set=max_all_time,
        sum_per_day=max(sum_per_day, sum_per_day_prev),
    )
    update_profile(dict(profile), db)
