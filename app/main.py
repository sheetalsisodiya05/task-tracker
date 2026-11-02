"""REST API. Run with:  uvicorn app.main:app --reload
Docs (auto-generated): http://127.0.0.1:8000/docs
"""
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app import storage, utils

app = FastAPI(title="TaskTracker API", version="1.0.0")
logger = utils.get_logger()


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    priority: str = "medium"
    due_date: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    priority: str
    status: str
    due_date: Optional[str] = None


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(status: Optional[str] = Query(None)):
    try:
        return [t.to_dict() for t in storage.list_tasks(status)]
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate):
    try:
        task = storage.add_task(payload.title, payload.priority,
                                payload.due_date)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return task.to_dict()


@app.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int):
    try:
        return storage.get_task(task_id).to_dict()
    except storage.TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate):
    try:
        task = storage.update_task(task_id, **payload.model_dump())
    except storage.TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return task.to_dict()


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    try:
        storage.delete_task(task_id)
    except storage.TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
