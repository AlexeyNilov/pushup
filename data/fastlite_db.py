import os
from typing import Callable
from typing import Dict

import fastlite as fl
from sqlite_minutils.db import Database


db_path = os.environ.get("PUSHUP_DB_PATH", "db/pushup.sqlite")
DB: Database = fl.database(db_path)


event_structure = dict(
    id=int,
    time=str,
    user_id=int,
    value=int,
)


profile_structure = dict(
    user_id=int,
    max_set=int,
    max_per_day=int,
    goal_set=int,
    goal_per_day=int,
    training_mode=str,
    training_day=int,
    age=int,
)


class EventNotFound(Exception):
    pass


def create_event_table(db=DB) -> fl.Table:
    event = db.t.event
    if event not in db.t:
        event.create(event_structure, pk="id")
    return event


def create_profile_table(db=DB) -> fl.Table:
    profile = db.t.profile
    if profile not in db.t:
        profile.create(profile_structure, pk="user_id")
    return profile


TABLES: Dict[str, Callable] = {
    "event": create_event_table,
    "profile": create_profile_table,
}


def prepare_db(db: Database = DB):
    for create_func in TABLES.values():
        create_func(db)


def recreate_db(db: Database = DB):
    for t in db.tables:
        t.drop()

    prepare_db(db=db)
