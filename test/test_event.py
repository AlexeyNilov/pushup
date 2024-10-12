from model.event import Event


def test_to_dict():
    e = Event(id=1, time="2024", user_id=1, value=10)
    assert dict(e) == {"id": 1, "time": "2024", "user_id": 1, "value": 10}


def test_from_dict():
    data = {"id": 1, "time": "2024", "user_id": 1, "value": 10}
    e = Event(**data)
    assert e.id == 1
