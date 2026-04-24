from datetime import timedelta
from unittest.mock import Mock

import pytest

from tests.doubles import (
    FakeTaskRepository,
    FailingReminderSender,
    SpyReminderSender,
)
from src.exceptions import InvalidInputError, ReminderError
from src.models import Priority
from src.reminders import NullReminderSender
from src.services import TaskService


def test_reminder_spy_records_created_reminder(user, due_tomorrow):
    """Category: Happy path & Test double: Spy"""

    # Arrange
    spy_sender = SpyReminderSender()
    task_service = TaskService(FakeTaskRepository(), spy_sender)
    task = task_service.create_task(
        user, "Exam", "", Priority.HIGH, due_tomorrow, "School"
    )
    reminder_at = due_tomorrow - timedelta(hours=1)

    # Act
    task_service.set_reminder(user, task.id, reminder_at)

    # Assert
    assert spy_sender.sent_reminders == [(user, task)]


def test_reminder_mock_verifies_sender_was_called(user, due_tomorrow):
    """Category: Happy path & Test double: Mock"""

    # Arrange
    mock_sender = Mock()
    task_service = TaskService(FakeTaskRepository(), mock_sender)
    task = task_service.create_task(
        user, "Exam", "", Priority.HIGH, due_tomorrow, "School"
    )
    reminder_at = due_tomorrow - timedelta(hours=1)

    # Act
    task_service.set_reminder(user, task.id, reminder_at)

    # Assert
    mock_sender.send_reminder_created.assert_called_once_with(user, task)


def test_reminder_dummy_sender_is_ignored_when_no_reminder_is_set(
    task_service, user, due_tomorrow
):
    """Category: Happy path"""

    # Arrange
    title = "No reminder task"

    # Act
    task = task_service.create_task(
        user, title, "", Priority.LOW, due_tomorrow, "Home"
    )

    # Assert
    assert task.reminder_at is None


def test_reminder_before_due_date_is_saved(user, due_tomorrow):
    """Category: Business logic"""

    # Arrange
    spy_sender = SpyReminderSender()
    task_service = TaskService(FakeTaskRepository(), spy_sender)
    task = task_service.create_task(
        user, "Exam", "", Priority.HIGH, due_tomorrow, "School"
    )
    reminder_at = due_tomorrow - timedelta(days=1)

    # Act
    updated_task = task_service.set_reminder(user, task.id, reminder_at)

    # Assert
    assert updated_task.reminder_at == reminder_at


def test_reminder_at_due_date_is_rejected(user, due_tomorrow):
    """Category: Boundary"""

    # Arrange
    task_service = TaskService(FakeTaskRepository(), NullReminderSender())
    task = task_service.create_task(
        user, "Exam", "", Priority.HIGH, due_tomorrow, "School"
    )

    # Act / Assert
    with pytest.raises(InvalidInputError):
        task_service.set_reminder(user, task.id, due_tomorrow)


def test_reminder_sender_failure_is_wrapped_in_domain_exception(
    user, due_tomorrow
):
    """Category: Exception handling & Test double: Stub"""

    # Arrange
    task_service = TaskService(FakeTaskRepository(), FailingReminderSender())
    task = task_service.create_task(
        user, "Exam", "", Priority.HIGH, due_tomorrow, "School"
    )
    reminder_at = due_tomorrow - timedelta(hours=1)

    # Act / Assert
    with pytest.raises(ReminderError):
        task_service.set_reminder(user, task.id, reminder_at)


def test_reminder_null_sender_accepts_reminder_without_side_effect(
    user, sample_task
):
    """Category: Happy path & Test double: Dummy"""

    # Arrange
    sender = NullReminderSender()

    # Act
    result = sender.send_reminder_created(user, sample_task)

    # Assert
    assert result is None
