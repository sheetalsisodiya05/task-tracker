import pytest
from fastapi.testclient import TestClient

from app import utils
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def temp_data_file(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "DATA_FILE", str(tmp_path / "tasks.json"))


def test_create_and_get():
    r = client.post("/tasks", json={"title": "Learn FastAPI", "priority": "high"})
    assert r.status_code == 201
    task_id = r.json()["id"]
    assert client.get(f"/tasks/{task_id}").status_code == 200


def test_404_for_missing_task():
    assert client.get("/tasks/999").status_code == 404


def test_422_for_bad_priority():
    r = client.post("/tasks", json={"title": "x", "priority": "urgent"})
    assert r.status_code == 422


def test_update_and_delete():
    task_id = client.post("/tasks", json={"title": "Temp"}).json()["id"]
    r = client.put(f"/tasks/{task_id}", json={"status": "done"})
    assert r.json()["status"] == "done"
    assert client.delete(f"/tasks/{task_id}").status_code == 204
