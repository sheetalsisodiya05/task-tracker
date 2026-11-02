# TaskTracker API

A small task-management backend in Python with both a **terminal CLI** and a **REST API** (FastAPI).
Both share the same storage logic (`app/storage.py`), with logging, validation, and pytest tests.

## Tech
Python 3.10+, FastAPI, Uvicorn, pytest, Git, Bash

## Setup
```bash
git clone <your-repo-url>
cd tasktracker
./scripts/setup.sh
source venv/bin/activate
```

## Use from the terminal
```bash
python -m app.cli add "Learn Git" --priority high --due 2026-11-05
python -m app.cli list
python -m app.cli list --status todo
python -m app.cli update 1 --status done
python -m app.cli delete 1
```

## Run the API
```bash
uvicorn app.main:app --reload
```
Interactive docs: http://127.0.0.1:8000/docs

| Method | Endpoint        | Description         | Success |
|--------|-----------------|---------------------|---------|
| GET    | /tasks          | List (`?status=`)   | 200     |
| POST   | /tasks          | Create a task       | 201     |
| GET    | /tasks/{id}     | Get one task        | 200     |
| PUT    | /tasks/{id}     | Update a task       | 200     |
| DELETE | /tasks/{id}     | Delete a task       | 204     |

Errors: `404` task not found, `422` invalid input.

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": "high"}'

curl http://127.0.0.1:8000/tasks
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"status": "done"}'
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Run tests
```bash
pytest -v
```

## Check logs
```bash
tail -f logs/app.log
grep ERROR logs/app.log
```

## What I learned
- Structuring a Python project with separated layers (CLI / API / storage)
- Virtual environments, `.env` config, Git workflow
- REST status codes and input validation
- Writing tests with pytest fixtures

## Future improvements
SQLite/PostgreSQL storage, authentication (JWT), Docker, CI with GitHub Actions
