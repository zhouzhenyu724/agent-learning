import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from demo import day23
from demo.day23_repository import Base, Record


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "day23.sqlite3"
    engine = create_engine(f"sqlite:///{database}")
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            session.add_all([
                Record(id=2, user_id=1, topic="前端", hours=9.0),
                Record(id=100, user_id=2, topic="Python", hours=1.0),
            ])
            session.commit()

        def test_get_db():
            with Session(engine) as session:
                yield session

        monkeypatch.setitem(day23.app.dependency_overrides, day23.get_db, test_get_db)
        with TestClient(day23.app) as test_client:
            yield test_client
    finally:
        engine.dispose()


def test_alice_reads_own_record(client):
    response = client.get("/records/2")

    assert response.status_code == 200
    assert response.json() == {"id": 2, "topic": "前端", "hours": 9.0}


def test_bob_cannot_read_alices_record(client, monkeypatch):
    monkeypatch.setitem(
        day23.app.dependency_overrides, day23.get_current_user_id, lambda: 2
    )

    bobs_record = client.get("/records/100")
    alices_record = client.get("/records/2")

    assert bobs_record.status_code == 200
    assert bobs_record.json() == {"id": 100, "topic": "Python", "hours": 1.0}
    assert alices_record.status_code == 404
    assert alices_record.json() == {"detail": "Record not found"}
