from data.yamler import load_yaml
import random
from service.repo import get_profile, ProfileNotFound, get_average, get_max_all_time
from sqlite_minutils.db import Database
from data.fastlite_db import DB


WORKOUTS = load_yaml("db/workout.yaml")
INTERMEDIATE_PROGRAM = load_yaml("db/intermediate.yaml")
BEGINNER_PROGRAM = load_yaml("db/beginner.yaml")


def get_program(level: str = "intermediate") -> list:
    return (
        BEGINNER_PROGRAM["Program"]
        if level == "beginner"
        else INTERMEDIATE_PROGRAM["Program"]
    )


def get_workout(user_id: int, db: Database = DB) -> str:
    try:
        profile = get_profile(user_id, db=db)
        if profile.training_mode in ["Beginner", "Intermediate"]:
            key = get_program(level=profile.training_mode.lower())[
                profile.training_day or 0
            ]
        else:
            key = random.choice(list(WORKOUTS.keys()))
    except ProfileNotFound:
        key = random.choice(list(WORKOUTS.keys()))

    avg_rep = get_average(user_id, db=db)
    max_rep = get_max_all_time(user_id, db=db)

    desc: str = WORKOUTS[key]
    replacements = {
        "{start_rep}": str(int(avg_rep / 2)),
        "{avg_rep}": str(avg_rep),
        "{avg_rep+1}": str(avg_rep + 1),
        "{avg_rep+2}": str(avg_rep + 2),
        "{avg_rep+3}": str(avg_rep + 3),
        "{max_rep}": str(max_rep),
        "{max_rep-20%}": str(int(max_rep * 0.8)),
        "{max_rep-30%}": str(int(max_rep * 0.7)),
    }

    for placeholder, value in replacements.items():
        desc = desc.replace(placeholder, value)

    return f"<i>{key}</i>\n{desc}"
