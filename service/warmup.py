from data.yamler import load_yaml
import random


WARMUPS = load_yaml("db/warmup.yaml")


def get_warmup() -> str:
    warmup = list()
    for items in WARMUPS.values():
        warmup.append(random.choice(list(items.keys())))
    return "\n".join(warmup)
