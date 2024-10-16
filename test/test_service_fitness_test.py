from service.fitness_test import get_army_pushup_range, get_pushup_rating, get_rating
from service.repo import update_profile


def test_get_army_pushup_range():
    assert get_army_pushup_range(45) == (31, 66)
    assert get_army_pushup_range(90) == (16, 50)


def test_get_pushup_rating():
    assert get_pushup_rating(45, 21) == "Average"
    assert get_pushup_rating(70, 21) == "Very good"


def test_get_rating(empty_db):
    update_profile({"user_id": 1, "age": 20, "max_set": 40}, db=empty_db)
    assert get_rating(1) == ("you need more training", "good")
    update_profile({"user_id": 1, "age": 50, "max_set": 40}, db=empty_db)
    assert get_rating(1) == ("you are fit", "excellent")
