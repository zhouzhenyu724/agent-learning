import pytest

from day14_reference import init_db, save_records, summarize_by_topic, validate_records


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "learning.db"
    init_db(path)
    return path


@pytest.mark.parametrize("hours", [0, 2.5, 24])
def test_accepts_valid_hours(hours):
    validate_records([{"topic": "Python", "hours": hours}])


@pytest.mark.parametrize("hours", [-1, 25, "2", True])
def test_rejects_invalid_hours(hours):
    with pytest.raises(ValueError, match="hours"):
        validate_records([{"topic": "Python", "hours": hours}])


@pytest.mark.parametrize(
    "records",
    [{}, [None], [{"topic": "Python"}], [{"hours": 2}],
     [{"topic": [], "hours": 2}], [{"topic": " ", "hours": 2}]],
)
def test_rejects_invalid_records(records):
    with pytest.raises(ValueError):
        validate_records(records)


def test_persists_and_groups_records(db_path):
    save_records(db_path, [
        {"topic": "Python", "hours": 1.5},
        {"topic": "Python", "hours": 2.5},
        {"topic": "后端", "hours": 2},
    ])

    # save_records 已关闭写入连接，汇总时会重新打开数据库。
    assert summarize_by_topic(db_path) == {"Python": 4.0, "后端": 2.0}


def test_empty_batch(db_path):
    save_records(db_path, [])
    assert summarize_by_topic(db_path) == {}


def test_invalid_batch_preserves_existing_records(db_path):
    save_records(db_path, [{"topic": "Python", "hours": 1}])

    with pytest.raises(ValueError, match="第 2 条"):
        save_records(db_path, [
            {"topic": "Python", "hours": 2},
            {"topic": "后端", "hours": 25},
        ])

    assert summarize_by_topic(db_path) == {"Python": 1.0}


def test_topic_with_apostrophe(db_path):
    topic = "Python's sqlite3"
    save_records(db_path, [{"topic": topic, "hours": 2}])
    assert summarize_by_topic(db_path) == {topic: 2.0}