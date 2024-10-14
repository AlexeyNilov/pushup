import pytest
import fastlite as fl
from data.fastlite_db import recreate_db
from service import repo


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    recreate_db(db)
    return db


def test_get_current_utc_timestamp():
    assert isinstance(repo.get_current_utc_timestamp(), str)


def test_save_pushup(empty_db):
    r = repo.save_pushup(value=10, user_id=1, db=empty_db)
    del r["time"]
    assert r == {"id": 1, "user_id": 1, "value": 10}


def test_is_number():
    assert repo.is_number("10")
    assert repo.is_number("text") is False


def test_get_sum_for_today(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=2, db=empty_db)
    assert repo.get_sum_for_today(user_id=1, db=empty_db) == 30


def test_get_max_for_today(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    assert repo.get_max_for_today(user_id=1, db=empty_db) == 20


def test_get_max_all_time(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=2, db=empty_db)
    assert repo.get_max_all_time(user_id=1, db=empty_db) == 20


def test_get_average(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    assert repo.get_average(user_id=1, db=empty_db) == 15


def test_update_profile(empty_db):
    r = repo.update_profile({"user_id": 1}, db=empty_db)
    assert r["user_id"] == 1


def test_get_profile(empty_db):
    repo.update_profile({"user_id": 1}, db=empty_db)
    p = repo.get_profile(user_id=1, db=empty_db)
    assert p.user_id == 1


def test_activate_training(empty_db):
    repo.activate_training(user_id=1, db=empty_db)
    p = repo.get_profile(user_id=1, db=empty_db)
    assert p.training_day == 0
    assert p.training_mode == "Intermediate"


def test_sync_profile(empty_db):
    repo.update_profile({"user_id": 1, "sum_per_day": 10, "max_set": 5}, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    repo.sync_profile(user_id=1, db=empty_db)
    p = repo.get_profile(user_id=1, db=empty_db)
    assert p.max_set == 20
    assert p.sum_per_day == 20


def test_get_max_sum(empty_db):
    repo.update_profile({"user_id": 1, "sum_per_day": 10, "max_set": 5}, db=empty_db)
    assert repo.get_max_sum(1, empty_db) == 10


def test_increment_training_day(empty_db):
    repo.activate_training(user_id=1, db=empty_db)
    repo.increment_training_day(user_id=1, db=empty_db)
    p = repo.get_profile(user_id=1, db=empty_db)
    assert p.training_day == 1


def test_increment_training_day_fail(empty_db):
    repo.update_profile({"user_id": 1, "sum_per_day": 10, "max_set": 5}, db=empty_db)
    repo.increment_training_day(user_id=1, db=empty_db)
    p = repo.get_profile(user_id=1, db=empty_db)
    assert p.training_day is None


def test_has_profile(empty_db):
    repo.update_profile({"user_id": 1, "sum_per_day": 10, "max_set": 5}, db=empty_db)
    assert repo.has_profile(1, empty_db) is True
    assert repo.has_profile(2, empty_db) is False


def test_deactivate_training(empty_db):
    repo.activate_training(user_id=1, db=empty_db)
    repo.deactivate_training(user_id=1, db=empty_db)
    p = repo.get_profile(user_id=1, db=empty_db)
    assert p.training_day == 0
    assert p.training_mode == "Freestyle"
