from datetime import datetime

import pytest

from tests.doubles import FakeTaskRepository, FakeUserRepository
from src.models import Priority
from src.reminders import NullReminderSender
from src.services import AuthService, TaskService


@pytest.fixture
def user_repository():
    return FakeUserRepository()


@pytest.fixture
def task_repository():
    return FakeTaskRepository()


@pytest.fixture
def auth_service(user_repository):
    return AuthService(user_repository)


@pytest.fixture
def task_service(task_repository):
    return TaskService(task_repository, NullReminderSender())


@pytest.fixture
def user(auth_service):
    return auth_service.sign_up("alice", "password123")


@pytest.fixture
def other_user(auth_service):
    return auth_service.sign_up("bob", "password123")


@pytest.fixture
def due_tomorrow():
    return datetime(2030, 1, 2, 12, 0, 0)


@pytest.fixture
def sample_task(task_service, user, due_tomorrow):
    return task_service.create_task(
        user=user,
        title="Finish assignment",
        description="Write pytest tests",
        priority=Priority.HIGH,
        due_date=due_tomorrow,
        category="School",
    )
