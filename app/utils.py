"""Config loading, logging setup and validation helpers."""
import logging
import os
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv is optional; env vars still work
    pass

DATA_FILE = os.getenv("DATA_FILE", "data/tasks.json")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
PORT = int(os.getenv("PORT", "8000"))

VALID_PRIORITIES = ("low", "medium", "high")
VALID_STATUSES = ("todo", "in_progress", "done")


def get_logger(name: str = "tasktracker") -> logging.Logger:
    """Return a logger that writes to logs/app.log and the console."""
    logger = logging.getLogger(name)
    if logger.handlers:  # avoid adding duplicate handlers
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger


def validate_priority(priority: str) -> str:
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
    return priority


def validate_status(status: str) -> str:
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {VALID_STATUSES}")
    return status


def validate_due_date(due_date):
    """Accept None or a YYYY-MM-DD string."""
    if due_date in (None, ""):
        return None
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("due_date must be in YYYY-MM-DD format")
    return due_date
