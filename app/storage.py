"""JSON-file storage layer. All business logic for tasks lives here,
so the CLI and the API both reuse the same functions."""
import json
import os
from typing import List, Optional

from app import utils
from app.models import Task

logger = utils.get_logger()


class TaskNotFound(Exception):
    pass


def _path() -> str:
    # Read at call time so tests can change utils.DATA_FILE
    return utils.DATA_FILE


def _load() -> List[Task]:
    path = _path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return [Task.from_dict(item) for item in json.load(f)]
    except (json.JSONDecodeError, TypeError) as e:
        logger.error("Corrupt data file %s: %s", path, e)
        raise RuntimeError(f"Data file {path} is corrupt") from e


def _save(tasks: List[Task]) -> None:
    path = _path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)


def add_task(title: str, priority: str = "medium",
             due_date: Optional[str] = None) -> Task:
    title = title.strip()
    if not title:
        raise ValueError("title cannot be empty")
    utils.validate_priority(priority)
    due_date = utils.validate_due_date(due_date)

    tasks = _load()
    new_id = max((t.id for t in tasks), default=0) + 1
    task = Task(id=new_id, title=title, priority=priority, due_date=due_date)
    tasks.append(task)
    _save(tasks)
    logger.info("Added task id=%s title=%r", task.id, task.title)
    return task


def list_tasks(status: Optional[str] = None) -> List[Task]:
    tasks = _load()
    if status:
        utils.validate_status(status)
        tasks = [t for t in tasks if t.status == status]
    return tasks


def get_task(task_id: int) -> Task:
    for t in _load():
        if t.id == task_id:
            return t
    raise TaskNotFound(f"Task {task_id} not found")


def update_task(task_id: int, **changes) -> Task:
    tasks = _load()
    for t in tasks:
        if t.id == task_id:
            if changes.get("title") is not None:
                if not changes["title"].strip():
                    raise ValueError("title cannot be empty")
                t.title = changes["title"].strip()
            if changes.get("priority") is not None:
                t.priority = utils.validate_priority(changes["priority"])
            if changes.get("status") is not None:
                t.status = utils.validate_status(changes["status"])
            if changes.get("due_date") is not None:
                t.due_date = utils.validate_due_date(changes["due_date"])
            _save(tasks)
            logger.info("Updated task id=%s", task_id)
            return t
    logger.warning("Update failed, task id=%s not found", task_id)
    raise TaskNotFound(f"Task {task_id} not found")


def delete_task(task_id: int) -> None:
    tasks = _load()
    remaining = [t for t in tasks if t.id != task_id]
    if len(remaining) == len(tasks):
        logger.warning("Delete failed, task id=%s not found", task_id)
        raise TaskNotFound(f"Task {task_id} not found")
    _save(remaining)
    logger.info("Deleted task id=%s", task_id)
