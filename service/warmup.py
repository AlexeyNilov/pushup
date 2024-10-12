from data.yamler import load_yaml
import random


WARM_UPS = load_yaml("db/warmup.yaml")


def get_warmup() -> str:
    warmup = list()
    for items in WARM_UPS.values():
        warmup.append(random.choice(list(items.keys())))
    return "\n".join(warmup)
