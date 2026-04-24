from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.exceptions import (
    AuthenticationError,
    InvalidInputError,
    ReminderError,
    TaskNotFoundError,
    UnauthorizedTaskAccessError,
    UserAlreadyExistsError,
)
from src.models import Priority, Task, User
from src.reminders import ReminderSender
from src.repositories import TaskRepository, UserRepository


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    def sign_up(self, username: str, password: str) -> User:
        username = username.strip()

        if not username:
            raise InvalidInputError("Username is required.")

        if not password:
            raise InvalidInputError("Password is required.")

        if self._users.get_by_username(username) is not None:
            raise UserAlreadyExistsError(f"Username already exists: {username}")

        user = User(
            id=str(uuid4()),
            username=username,
            password_hash=self._hash_password(password),
        )
        self._users.add(user)
        return user

    def log_in(self, username: str, password: str) -> User:
        username = username.strip()
        user = self._users.get_by_username(username)

        if user is None:
            raise AuthenticationError("Invalid username or password.")

        if user.password_hash != self._hash_password(password):
            raise AuthenticationError("Invalid username or password.")

        return user

    def _hash_password(self, password: str) -> str:
        return f"stub-hash::{password}"


class TaskService:
    def __init__(
        self,
        tasks: TaskRepository,
        reminder_sender: ReminderSender,
    ) -> None:
        self._tasks = tasks
        self._reminder_sender = reminder_sender

    def create_task(
        self,
        user: User,
        title: str,
        description: str,
        priority: Priority,
        due_date: datetime,
        category: str,
    ) -> Task:
        self._validate_task_fields(title, priority, due_date, category)

        task = Task.create(
            owner_id=user.id,
            title=title.strip(),
            description=description.strip(),
            priority=priority,
            due_date=due_date,
            category=category.strip(),
        )

        self._tasks.add(task)
        return task

    def get_task(self, user: User, task_id: str) -> Task:
        return self._get_owned_task(user, task_id)

    def list_tasks(self, user: User) -> list[Task]:
        return self._tasks.list_by_owner(user.id)

    def update_task(
        self,
        user: User,
        task_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
        priority: Priority | None = None,
        due_date: datetime | None = None,
        category: str | None = None,
    ) -> Task:
        task = self._get_owned_task(user, task_id)

        new_title = task.title if title is None else title.strip()
        new_description = (
            task.description if description is None else description.strip()
        )
        new_priority = task.priority if priority is None else priority
        new_due_date = task.due_date if due_date is None else due_date
        new_category = task.category if category is None else category.strip()

        self._validate_task_fields(
            new_title, new_priority, new_due_date, new_category
        )

        task.title = new_title
        task.description = new_description
        task.priority = new_priority
        task.due_date = new_due_date
        task.category = new_category

        self._tasks.update(task)
        return task

    def delete_task(self, user: User, task_id: str) -> None:
        task = self._get_owned_task(user, task_id)
        self._tasks.delete(task.id)

    def mark_complete(self, user: User, task_id: str) -> Task:
        task = self._get_owned_task(user, task_id)
        task.completed = True
        self._tasks.update(task)
        return task

    def mark_incomplete(self, user: User, task_id: str) -> Task:
        task = self._get_owned_task(user, task_id)
        task.completed = False
        self._tasks.update(task)
        return task

    def set_reminder(
        self, user: User, task_id: str, reminder_at: datetime
    ) -> Task:
        task = self._get_owned_task(user, task_id)

        if reminder_at >= task.due_date:
            raise InvalidInputError("Reminder must be before the due date.")

        task.reminder_at = reminder_at
        self._tasks.update(task)

        try:
            self._reminder_sender.send_reminder_created(user, task)
        except Exception as exc:
            raise ReminderError("Reminder sender failed.") from exc

        return task

    def filter_by_category(self, user: User, category: str) -> list[Task]:
        category = category.strip().lower()
        return [
            task
            for task in self.list_tasks(user)
            if task.category.lower() == category
        ]

    def search_by_keyword(self, user: User, keyword: str) -> list[Task]:
        keyword = keyword.strip().lower()

        if not keyword:
            raise InvalidInputError("Keyword is required.")

        return [
            task
            for task in self.list_tasks(user)
            if keyword in task.title.lower()
            or keyword in task.description.lower()
            or keyword in task.category.lower()
        ]

    def sort_by_priority(
        self, user: User, *, descending: bool = True
    ) -> list[Task]:
        return sorted(
            self.list_tasks(user),
            key=lambda task: task.priority.value,
            reverse=descending,
        )

    def sort_by_due_date(self, user: User) -> list[Task]:
        return sorted(self.list_tasks(user), key=lambda task: task.due_date)

    def sort_by_completion(self, user: User) -> list[Task]:
        return sorted(self.list_tasks(user), key=lambda task: task.completed)

    def _get_owned_task(self, user: User, task_id: str) -> Task:
        task = self._tasks.get(task_id)

        if task is None:
            raise TaskNotFoundError(f"Task not found: {task_id}")

        if task.owner_id != user.id:
            raise UnauthorizedTaskAccessError("Task belongs to another user.")

        return task

    def _validate_task_fields(
        self,
        title: str,
        priority: Priority,
        due_date: datetime,
        category: str,
    ) -> None:
        if not title or not title.strip():
            raise InvalidInputError("Title is required.")

        if len(title.strip()) > 100:
            raise InvalidInputError("Title cannot exceed 100 characters.")

        if not isinstance(priority, Priority):
            raise InvalidInputError("Priority must be LOW, MEDIUM, or HIGH.")

        if not isinstance(due_date, datetime):
            raise InvalidInputError("Due date must be a datetime.")

        if not category or not category.strip():
            raise InvalidInputError("Category is required.")
