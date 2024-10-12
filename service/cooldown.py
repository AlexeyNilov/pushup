from data.yamler import load_yaml
import random


COOL_DOWNS = load_yaml("db/cooldown.yaml")


def get_cool_down() -> str:
    r = list()
    for items in COOL_DOWNS.values():
        r.append(random.choice(list(items.keys())))
    return "\n".join(r)
