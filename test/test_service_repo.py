from service import repo


def test_save_pushup(empty_db):
    r = repo.save_pushup(value=10, user_id=1, db=empty_db)
    del r["time"]
    assert r == {"id": 1, "user_id": 1, "value": 10}


def test_get_sum_for_today(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=2, db=empty_db)
    assert repo.get_sum_for_today(user_id=1, db=empty_db) == 30


def test_get_max_for_today(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    assert repo.get_max_for_today(user_id=1, db=empty_db) == 20


def test_get_max_all_time(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=2, db=empty_db)
    assert repo.get_max_all_time(user_id=1, db=empty_db) == 20


def test_get_average(empty_db):
    repo.save_pushup(value=10, user_id=1, db=empty_db)
    repo.save_pushup(value=20, user_id=1, db=empty_db)
    assert repo.get_average(user_id=1, db=empty_db) == 15


def test_update_profile(empty_db):
    r = repo.update_profile({"user_id": 1}, db=empty_db)
    assert r["user_id"] == 1


def test_get_profile(empty_db, user_id, profile):
    p = repo.get_profile(user_id=user_id, db=empty_db)
    assert p.age == profile.age
    assert p.user_id == profile.user_id


def test_sync_profile(empty_db, profile, user_id):
    repo.save_pushup(value=20, user_id=user_id, db=empty_db)
    repo.sync_profile(user_id=user_id, db=empty_db)
    p = repo.get_profile(user_id=user_id, db=empty_db)
    assert p.max_set == 20
    assert p.sum_per_day == 20


def test_get_max_sum(empty_db, user_id, profile):
    assert repo.get_max_sum(user_id, empty_db) == 10


def test_has_profile(empty_db, user_id, profile):
    assert repo.has_profile(user_id, empty_db) is True
    assert repo.has_profile(2, empty_db) is False
