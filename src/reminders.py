from __future__ import annotations

from typing import Protocol

from src.models import Task, User


class ReminderSender(Protocol):
    def send_reminder_created(self, user: User, task: Task) -> None: ...


class NullReminderSender:
    """Dummy sender for cases where reminder delivery is irrelevant."""

    def send_reminder_created(self, user: User, task: Task) -> None:
        pass
