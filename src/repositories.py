from __future__ import annotations

from typing import Protocol

from models import Task, User


class UserRepository(Protocol):
    def add(self, user: User) -> None: ...

    def get_by_username(self, username: str) -> User | None: ...


class TaskRepository(Protocol):
    def add(self, task: Task) -> None: ...

    def get(self, task_id: str) -> Task | None: ...

    def list_by_owner(self, owner_id: str) -> list[Task]: ...

    def update(self, task: Task) -> None: ...

    def delete(self, task_id: str) -> None: ...


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users_by_username: dict[str, User] = {}

    def add(self, user: User) -> None:
        self._users_by_username[user.username] = user

    def get_by_username(self, username: str) -> User | None:
        return self._users_by_username.get(username)


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list_by_owner(self, owner_id: str) -> list[Task]:
        return [
            task for task in self._tasks.values() if task.owner_id == owner_id
        ]

    def update(self, task: Task) -> None:
        self._tasks[task.id] = task

    def delete(self, task_id: str) -> None:
        self._tasks.pop(task_id, None)
