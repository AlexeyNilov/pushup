from service.workout import get_workout, get_program


def test_get_workout():
    assert isinstance(get_workout(), str)
    assert "{" not in get_workout()
    assert "}" not in get_workout()
    # assert get_workout() == ""


def test_get_program():
    assert isinstance(get_program(), list)
