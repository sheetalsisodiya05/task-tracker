import pytest

from app import storage, utils


@pytest.fixture(autouse=True)
def temp_data_file(tmp_path, monkeypatch):
    """Every test gets its own empty data file."""
    monkeypatch.setattr(utils, "DATA_FILE", str(tmp_path / "tasks.json"))


def test_add_task():
    task = storage.add_task("Learn Git", "high")
    assert task.id == 1
    assert task.status == "todo"


def test_ids_increment():
    storage.add_task("One")
    second = storage.add_task("Two")
    assert second.id == 2


def test_empty_title_rejected():
    with pytest.raises(ValueError):
        storage.add_task("   ")


def test_invalid_priority_rejected():
    with pytest.raises(ValueError):
        storage.add_task("Bad", priority="urgent")


def test_invalid_due_date_rejected():
    with pytest.raises(ValueError):
        storage.add_task("Bad date", due_date="05-11-2026")


def test_update_task():
    task = storage.add_task("Write tests")
    updated = storage.update_task(task.id, status="done")
    assert updated.status == "done"


def test_filter_by_status():
    storage.add_task("A")
    b = storage.add_task("B")
    storage.update_task(b.id, status="done")
    assert len(storage.list_tasks("done")) == 1
    assert len(storage.list_tasks("todo")) == 1


def test_delete_task():
    task = storage.add_task("Temp")
    storage.delete_task(task.id)
    assert storage.list_tasks() == []


def test_delete_missing_task_raises():
    with pytest.raises(storage.TaskNotFound):

        storage.delete_task(999)


def test_corrupt_file_raises():
    with open(utils.DATA_FILE, "w") as f:
        f.write("{not valid json")
    with pytest.raises(RuntimeError):
        storage.list_tasks()
