from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import uuid4


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(frozen=True)
class User:
    id: str
    username: str
    password_hash: str


@dataclass
class Task:
    id: str
    owner_id: str
    title: str
    description: str
    priority: Priority
    due_date: datetime
    category: str
    completed: bool = False
    reminder_at: datetime | None = None

    @staticmethod
    def create(
        owner_id: str,
        title: str,
        description: str,
        priority: Priority,
        due_date: datetime,
        category: str,
    ) -> "Task":
        return Task(
            id=str(uuid4()),
            owner_id=owner_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category=category,
        )
