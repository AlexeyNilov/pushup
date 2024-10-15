from service.workout import get_workout, get_program
import fastlite as fl
from data.fastlite_db import recreate_db
from service.training import activate_training
import pytest


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    recreate_db(db)
    return db


def test_get_workout():
    assert isinstance(get_workout(1), str)
    assert "{" not in get_workout(1)
    assert "}" not in get_workout(1)
    # assert get_workout() == ""


def test_get_workout_for_program(empty_db):
    activate_training(user_id=1, db=empty_db, max_set=20)
    assert "Power Push-Up Tempo" in get_workout(1, db=empty_db)


def test_get_program():
    assert isinstance(get_program(), list)
