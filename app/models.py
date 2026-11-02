"""Task data model."""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    status: str = "todo"
    due_date: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(**data)
