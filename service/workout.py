from data.yamler import load_yaml
import random
from service.repo import get_profile, ProfileNotFound, get_average, get_max_all_time
from sqlite_minutils.db import Database
from data.fastlite_db import DB


WORKOUTS = load_yaml("db/workout.yaml")
PROGRAM = load_yaml("db/program.yaml")


def get_program() -> list:
    return PROGRAM["Program"]


def get_workout(user_id: int, db: Database = DB) -> str:
    key = random.choice(list(WORKOUTS.keys()))
    try:
        profile = get_profile(user_id, db=db)
        if profile.training_mode == "Program":
            key = get_program()[profile.training_day or 0]
    except ProfileNotFound:
        pass

    avg_rep = get_average(user_id, db=db)
    max_rep = get_max_all_time(user_id, db=db)

    desc: str = WORKOUTS[key]
    desc = desc.replace("{start_rep}", str(int(avg_rep / 2)))
    desc = desc.replace("{avg_rep}", str(avg_rep))
    desc = desc.replace("{avg_rep+1}", str(avg_rep + 1))
    desc = desc.replace("{avg_rep+2}", str(avg_rep + 2))
    desc = desc.replace("{max_rep}", str(max_rep))
    desc = desc.replace("{max_rep-20%}", str(int(max_rep * 0.8)))
    desc = desc.replace("{max_rep-30%}", str(int(max_rep * 0.7)))
    return f"<i>{key}</i>\n{desc}"
