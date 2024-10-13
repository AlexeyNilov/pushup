from data.yamler import load_yaml
import random


WORKOUTS = load_yaml("db/workout.yaml")
PROGRAM = load_yaml("db/program.yaml")


def get_workout(avg_rep: int = 5, max_rep: int = 10) -> str:
    key = random.choice(list(WORKOUTS.keys()))
    desc: str = WORKOUTS[key]
    desc = desc.replace("{start_rep}", str(int(avg_rep / 2)))
    desc = desc.replace("{avg_rep}", str(avg_rep))
    desc = desc.replace("{avg_rep+1}", str(avg_rep + 1))
    desc = desc.replace("{avg_rep+2}", str(avg_rep + 2))
    desc = desc.replace("{max_rep}", str(max_rep))
    desc = desc.replace("{max_rep-20%}", str(int(max_rep * 0.8)))
    desc = desc.replace("{max_rep-30%}", str(int(max_rep * 0.7)))
    return f"<i>{key}</i>\n{desc}"


def get_program() -> list:
    return PROGRAM["Program"]
