import fastlite as fl
import pytest
from data import fastlite_db as fl_db


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    for t in db.tables:
        t.drop()
    return db


def test_create_event_table(empty_db):
    table = fl_db.create_event_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "event"
