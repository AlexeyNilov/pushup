from data.yamler import load_yaml
import random


WORKOUTS = load_yaml("db/workout.yaml")


def get_workout(avg_rep: int = 5, max_rep: int = 10) -> str:
    key = random.choice(list(WORKOUTS.keys()))
    desc: str = WORKOUTS[key]["desc"]
    desc = desc.replace("{start_rep}", str(int(avg_rep / 2)))
    desc = desc.replace("{avg_rep}", str(avg_rep))
    desc = desc.replace("{max_rep}", str(max_rep))
    return f"{key}\n{desc}"
