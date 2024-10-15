from data.fastlite_db import DB
from sqlite_minutils.db import Database
from model.profile import Profile
from service.util import get_current_utc_timestamp


class ProfileNotFound(Exception):
    pass


def save_pushup(value: int, user_id: int, db: Database = DB) -> dict:
    return db.t.event.insert(
        time=get_current_utc_timestamp(), user_id=user_id, value=value
    )


def get_sum_for_today(user_id: int, db: Database = DB) -> int:
    return db.q(
        f"SELECT COALESCE(SUM(value), 0) AS sum FROM event WHERE user_id = {user_id} AND date(time) = date('now');"
    )[0]["sum"]


def get_max_for_today(user_id: int, db: Database = DB) -> int:
    return db.q(
        f"SELECT COALESCE(MAX(value), 0) AS max_value FROM event WHERE user_id = {user_id} AND date(time) = date('now');"
    )[0]["max_value"]


def get_max_all_time(user_id: int, db: Database = DB) -> int:
    return db.q(
        f"SELECT COALESCE(MAX(value), 0) AS max_value FROM event WHERE user_id = {user_id};"
    )[0]["max_value"]


def get_average(user_id: int, limit: int = 100, db: Database = DB) -> int:
    result = db.q(
        f"""
        SELECT COALESCE(ROUND(AVG(value)), 5) AS average_value
        FROM (
            SELECT value
            FROM event
            WHERE user_id = {user_id}
            ORDER BY time DESC
            LIMIT {limit}
        );
    """
    )[0]["average_value"]
    return int(result)


def update_profile(profile: dict, db: Database = DB) -> dict:
    return db.t.profile.upsert(**profile)


def get_profile(user_id: int, db: Database = DB) -> Profile:
    try:
        return Profile(**db.t.profile[user_id])
    except Exception:
        raise ProfileNotFound


def sync_profile(user_id: int, db: Database = DB):
    try:
        profile = get_profile(user_id, db)
    except ProfileNotFound:
        profile = Profile(user_id=user_id)

    profile.max_set = get_max_all_time(user_id, db)
    profile.sum_per_day = max(get_sum_for_today(user_id, db), profile.sum_per_day or 0)
    update_profile(dict(profile), db)


def get_max_sum(user_id: int, db: Database = DB) -> int:
    try:
        return get_profile(user_id, db).sum_per_day or 0
    except ProfileNotFound:
        return 0


def has_profile(user_id: int, db: Database = DB) -> bool:
    try:
        get_profile(user_id, db)
        return True
    except ProfileNotFound:
        return False
