from service.fitness_test import get_army_pushup_range, get_pushup_rating


def test_get_army_pushup_range():
    assert get_army_pushup_range(45) == (31, 66)
    assert get_army_pushup_range(90) == (16, 50)


def test_get_pushup_rating():
    assert get_pushup_rating(45, 21) == "Average"
    assert get_pushup_rating(70, 21) == "Very good"
