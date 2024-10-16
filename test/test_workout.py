from service.workout import get_workout, get_program
import fastlite as fl
from data.fastlite_db import recreate_db
from service.training import activate_training
import pytest
from unittest.mock import patch
from service.repo import ProfileNotFound
from data.fastlite_db import DB


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


def test_get_workout_beginner(empty_db):
    with patch("service.workout.get_profile") as mock_get_profile:
        mock_get_profile.return_value.training_mode = "Beginner"
        mock_get_profile.return_value.training_day = 0

        result = get_workout(1, db=empty_db)
        assert "Wall push-ups" in result
        assert "<i>" in result and "</i>" in result


def test_get_workout_intermediate(empty_db):
    with patch("service.workout.get_profile") as mock_get_profile:
        mock_get_profile.return_value.training_mode = "Intermediate"
        mock_get_profile.return_value.training_day = 0

        result = get_workout(1, db=empty_db)
        assert "Power Push-Up Tempo" in result
        assert "<i>" in result and "</i>" in result


def test_get_workout_profile_not_found(empty_db):
    with patch("service.workout.get_profile", side_effect=ProfileNotFound):
        get_workout(10, db=empty_db)
