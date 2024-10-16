from service import util


def test_get_current_utc_timestamp():
    assert isinstance(util.get_current_utc_timestamp(), str)


def test_is_number():
    assert util.is_number("10")
    assert util.is_number("text") is False


def test_convert_to_int():
    assert util.convert_to_int("10") == 10
    assert util.convert_to_int("text") == 0
