from dataclasses import dataclass
from typing import Any, Union, Optional


@dataclass
class Event:
    id: int | None = None
    time: str | None = None
    user_id: int | None = None
    value: int | None = None


@dataclass
class Profile:
    user_id: int | None = None
    max_set: int | None = None
    max_per_day: int | None = None
    goal_set: int | None = None
    goal_per_day: int | None = None
    training_mode: str | None = None
