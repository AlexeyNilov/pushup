from service.cooldown import get_cool_down


def test_get_cool_down():
    assert isinstance(get_cool_down(), str)
