from data.yamler import load_yaml
import random


IDEAS = load_yaml("db/idea.yaml")


def get_idea() -> str:
    return random.choice(IDEAS["Idea"])
