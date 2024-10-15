import pytest
import fastlite as fl
from data.fastlite_db import recreate_db
from service.training import (
    activate_training,
    increment_training_day,
    deactivate_training,
)
from service.repo import get_profile, update_profile


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    recreate_db(db)
    return db


def test_activate_training(empty_db):
    activate_training(user_id=1, db=empty_db)
    p = get_profile(user_id=1, db=empty_db)
    assert p.training_day == 0
    assert p.training_mode == "Intermediate"


def test_increment_training_day(empty_db):
    activate_training(user_id=1, db=empty_db)
    increment_training_day(user_id=1, db=empty_db)
    p = get_profile(user_id=1, db=empty_db)
    assert p.training_day == 1


def test_increment_training_day_fail(empty_db):
    update_profile({"user_id": 1, "sum_per_day": 10, "max_set": 5}, db=empty_db)
    increment_training_day(user_id=1, db=empty_db)
    p = get_profile(user_id=1, db=empty_db)
    assert p.training_day is None


def test_deactivate_training(empty_db):
    activate_training(user_id=1, db=empty_db)
    deactivate_training(user_id=1, db=empty_db)
    p = get_profile(user_id=1, db=empty_db)
    assert p.training_day == 0
    assert p.training_mode == "Freestyle"
