import pytest

from src.exceptions import (
    InvalidInputError,
    TaskNotFoundError,
    UnauthorizedTaskAccessError,
)
from src.models import Priority


def test_happy_path_user_can_create_task(task_service, user, due_tomorrow):
    """Category: Happy path"""

    # Arrange
    title = "Finish assignment"

    # Act
    task = task_service.create_task(
        user=user,
        title=title,
        description="Write tests",
        priority=Priority.HIGH,
        due_date=due_tomorrow,
        category="School",
    )

    # Assert
    assert task.title == "Finish assignment"


def test_happy_path_user_can_view_owned_task(task_service, user, sample_task):
    """Category: Happy path"""

    # Arrange
    task_id = sample_task.id

    # Act
    found_task = task_service.get_task(user, task_id)

    # Assert
    assert found_task == sample_task


def test_happy_path_user_can_update_task_title(task_service, user, sample_task):
    """Category: Happy path"""

    # Arrange
    task_id = sample_task.id

    # Act
    updated_task = task_service.update_task(
        user,
        task_id,
        title="Finish final assignment",
    )

    # Assert
    assert updated_task.title == "Finish final assignment"


def test_happy_path_user_can_delete_task(task_service, user, sample_task):
    """Category: Happy path"""

    # Arrange
    task_id = sample_task.id

    # Act
    task_service.delete_task(user, task_id)

    # Assert
    with pytest.raises(TaskNotFoundError):
        task_service.get_task(user, task_id)


def test_business_logic_mark_complete_sets_completed_true(
    task_service, user, sample_task
):
    """Category: Business logic"""

    # Arrange
    task_id = sample_task.id

    # Act
    completed_task = task_service.mark_complete(user, task_id)

    # Assert
    assert completed_task.completed is True


def test_business_logic_mark_incomplete_sets_completed_false(
    task_service, user, sample_task
):
    """Category: Business logic"""

    # Arrange
    task_service.mark_complete(user, sample_task.id)

    # Act
    incomplete_task = task_service.mark_incomplete(user, sample_task.id)

    # Assert
    assert incomplete_task.completed is False


def test_business_logic_tasks_are_isolated_by_user(
    task_service, user, other_user, sample_task
):
    """Category: Business logic & Exception handling"""

    # Arrange
    task_id = sample_task.id

    # Act / Assert
    with pytest.raises(UnauthorizedTaskAccessError):
        task_service.get_task(other_user, task_id)


def test_invalid_input_blank_title_is_rejected(
    task_service, user, due_tomorrow
):
    """Category: Invalid input"""

    # Arrange
    title = "   "

    # Act / Assert
    with pytest.raises(InvalidInputError):
        task_service.create_task(
            user, title, "", Priority.HIGH, due_tomorrow, "School"
        )


def test_invalid_input_invalid_priority_is_rejected(
    task_service, user, due_tomorrow
):
    """Category: Invalid input"""

    # Arrange
    invalid_priority = "URGENT"

    # Act / Assert
    with pytest.raises(InvalidInputError):
        task_service.create_task(
            user, "Task", "", invalid_priority, due_tomorrow, "School"
        )


def test_invalid_input_blank_category_is_rejected(
    task_service, user, due_tomorrow
):
    """Category: Invalid input"""

    # Arrange
    category = " "

    # Act / Assert
    with pytest.raises(InvalidInputError):
        task_service.create_task(
            user, "Task", "", Priority.LOW, due_tomorrow, category
        )


def test_boundary_title_with_exactly_100_characters_is_allowed(
    task_service, user, due_tomorrow
):
    """Category: Boundary"""

    # Arrange
    title = "a" * 100

    # Act
    task = task_service.create_task(
        user, title, "", Priority.LOW, due_tomorrow, "School"
    )

    # Assert
    assert len(task.title) == 100


def test_boundary_title_with_101_characters_is_rejected(
    task_service, user, due_tomorrow
):
    """Category: Boundary"""

    # Arrange
    title = "a" * 101

    # Act / Assert
    with pytest.raises(InvalidInputError):
        task_service.create_task(
            user, title, "", Priority.LOW, due_tomorrow, "School"
        )


def test_boundary_list_tasks_for_new_user_is_empty(task_service, user):
    """Category: Boundary"""

    # Arrange
    expected_tasks = []

    # Act
    tasks = task_service.list_tasks(user)

    # Assert
    assert tasks == expected_tasks


def test_exception_missing_task_raises_task_not_found(task_service, user):
    """Category: Exception handling"""

    # Arrange
    missing_task_id = "missing-task-id"

    # Act / Assert
    with pytest.raises(TaskNotFoundError):
        task_service.get_task(user, missing_task_id)


def test_invalid_input_non_datetime_due_date_is_rejected(task_service, user):
    """Category: Invalid input"""

    # Arrange
    due_date = "2030-01-02"

    # Act / Assert
    with pytest.raises(InvalidInputError):
        task_service.create_task(
            user, "Task", "", Priority.LOW, due_date, "School"
        )
