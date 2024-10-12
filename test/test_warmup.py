from service.warmup import get_warmup


def test_get_warmup():
    assert isinstance(get_warmup(), str)
