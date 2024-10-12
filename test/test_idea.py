from service.idea import get_idea


def test_get_idea():
    assert isinstance(get_idea(), str)
