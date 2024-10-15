from data.fastlite_db import DB
from sqlite_minutils.db import Database
from model.profile import Profile
from service.util import get_current_utc_timestamp


class ProfileNotFound(Exception):
    pass


def save_pushup(value: int, user_id: int, db: Database = DB) -> dict:
    e = {"time": get_current_utc_timestamp(), "user_id": user_id, "value": value}
    event = db.t.event
    return event.insert(**e)


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
        return 5


def update_profile(profile: dict, db: Database = DB) -> dict:
    table = db.t.profile
    return table.upsert(**profile)


def get_profile(user_id: int, db: Database = DB) -> Profile:
    try:
        data = db.t.profile[user_id]
    except Exception:
        raise ProfileNotFound
    return Profile(**data)


def sync_profile(user_id: int, db: Database = DB):
    try:
        profile = get_profile(user_id, db)
    except ProfileNotFound:
        profile = Profile(user_id=user_id)

    sum_per_day_prev = profile.sum_per_day or 0
    profile.max_set = get_max_all_time(user_id, db)
    profile.sum_per_day = max(get_sum_for_today(user_id, db), sum_per_day_prev)
    update_profile(dict(profile), db)


def get_max_sum(user_id: int, db: Database = DB) -> int:
    try:
        p = get_profile(user_id, db)
    except ProfileNotFound:
        return 0
    return p.sum_per_day or 0


def has_profile(user_id: int, db: Database = DB) -> bool:
    try:
        get_profile(user_id, db)
    except ProfileNotFound:
        return False
    return True
