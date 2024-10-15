from data.yamler import load_yaml
import random


WARM_UPS = load_yaml("db/warmup.yaml")


def get_warmup() -> str:
    return "\n".join(random.choice(list(items.keys())) for items in WARM_UPS.values())
