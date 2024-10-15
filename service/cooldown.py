from data.yamler import load_yaml
import random


COOL_DOWNS = load_yaml("db/cooldown.yaml")


def get_cool_down() -> str:
    return "\n".join(random.choice(list(items.keys())) for items in COOL_DOWNS.values())
