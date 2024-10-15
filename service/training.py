from service.repo import get_profile, update_profile, ProfileNotFound
from model.profile import Profile
from data.fastlite_db import DB
from sqlite_minutils.db import Database


def activate_training(user_id: int, max_set: int = 5, db: Database = DB):
    try:
        profile = get_profile(user_id=user_id, db=db)
    except ProfileNotFound:
        profile = Profile(user_id=user_id)

    if max_set < 3:
        profile.training_mode = "Beginner"
    else:
        profile.training_mode = "Intermediate"
    profile.training_day = 0
    update_profile(dict(profile), db=db)


def deactivate_training(user_id: int, db: Database = DB):
    try:
        profile = get_profile(user_id=user_id, db=db)
    except ProfileNotFound:
        return
    profile.training_mode = "Freestyle"
    profile.training_day = 0
    update_profile(dict(profile), db=db)


def increment_training_day(user_id: int, db: Database = DB):
    try:
        profile = get_profile(user_id, db)
    except ProfileNotFound:
        return

    if profile.training_mode in ["Beginner", "Intermediate"]:
        profile.training_day = (profile.training_day or 0) + 1
    update_profile(dict(profile), db)
