import pytest
import fastlite as fl
from data.fastlite_db import recreate_db
from service import util


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    recreate_db(db)
    return db


def test_get_current_utc_timestamp():
    assert isinstance(util.get_current_utc_timestamp(), str)


def test_is_number():
    assert util.is_number("10")
    assert util.is_number("text") is False


def test_convert_to_int():
    assert util.convert_to_int("10") == 10
    assert util.convert_to_int("text") == 0
