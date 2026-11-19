import pytest
from fastapi.testclient import TestClient

import day19


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(day19, "DB_PATH", tmp_path / "test.sqlite3")
    with TestClient(day19.app) as test_client:
        yield test_client


def create_record(client):
    response = client.post("/records", json={"topic": "Python", "hours": 2.5})
    assert response.status_code == 201
    return response.json()


def test_empty_list(client):
    response = client.get("/records")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_read(client):
    record = create_record(client)
    assert isinstance(record["id"], int)
    assert record["topic"] == "Python"
    assert record["hours"] == 2.5

    response = client.get(f"/records/{record['id']}")
    assert response.status_code == 200
    assert response.json() == record


def test_patch_keeps_omitted_field(client):
    record = create_record(client)
    path = f"/records/{record['id']}"
    response = client.patch(path, json={"hours": 0})

    assert response.status_code == 200
    assert response.json() == {**record, "hours": 0}
    assert client.get(path).json() == response.json()


def test_delete_then_not_found(client):
    record = create_record(client)
    path = f"/records/{record['id']}"
    response = client.delete(path)

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(path).status_code == 404


def test_boolean_hours_returns_422(client):
    response = client.post("/records", json={"topic": "Python", "hours": True})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "hours"]
    assert client.get("/records").json() == []