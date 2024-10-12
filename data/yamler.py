from functools import lru_cache

import yaml


@lru_cache
def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as fp:
        return yaml.safe_load(stream=fp)
