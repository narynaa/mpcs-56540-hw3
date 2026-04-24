from datetime import datetime

import pytest

from src.exceptions import InvalidInputError
from src.models import Priority


def test_business_logic_sort_by_priority_returns_high_before_medium_before_low(
    task_service, user
):
    """Category: Business logic"""

    # Arrange
    due_date = datetime(2030, 1, 2, 12, 0, 0)
    low_task = task_service.create_task(
        user, "Low task", "", Priority.LOW, due_date, "Work"
    )
    high_task = task_service.create_task(
        user, "High task", "", Priority.HIGH, due_date, "Work"
    )
    medium_task = task_service.create_task(
        user, "Medium task", "", Priority.MEDIUM, due_date, "Work"
    )

    # Act
    sorted_tasks = task_service.sort_by_priority(user)

    # Assert
    assert sorted_tasks == [high_task, medium_task, low_task]


def test_business_logic_sort_by_due_date_returns_earliest_first(
    task_service, user
):
    """Category: Business logic"""

    # Arrange
    later_task = task_service.create_task(
        user,
        "Later task",
        "",
        Priority.MEDIUM,
        datetime(2030, 1, 3, 12, 0, 0),
        "Work",
    )
    earlier_task = task_service.create_task(
        user,
        "Earlier task",
        "",
        Priority.MEDIUM,
        datetime(2030, 1, 1, 12, 0, 0),
        "Work",
    )

    # Act
    sorted_tasks = task_service.sort_by_due_date(user)

    # Assert
    assert sorted_tasks == [earlier_task, later_task]


def test_business_logic_filter_by_category_matches_case_insensitively(
    task_service, user
):
    """Category: Business logic & Equivalence classes"""

    # Arrange
    due_date = datetime(2030, 1, 2, 12, 0, 0)
    school_task = task_service.create_task(
        user, "Study", "", Priority.HIGH, due_date, "School"
    )
    task_service.create_task(
        user, "Pay bills", "", Priority.MEDIUM, due_date, "Home"
    )

    # Act
    filtered_tasks = task_service.filter_by_category(user, "school")

    # Assert
    assert filtered_tasks == [school_task]


def test_business_logic_keyword_search_matches_title(task_service, user):
    """Category: Business logic & Equivalence classes"""

    # Arrange
    due_date = datetime(2030, 1, 2, 12, 0, 0)
    matching_task = task_service.create_task(
        user, "Buy groceries", "", Priority.MEDIUM, due_date, "Home"
    )
    task_service.create_task(
        user, "Study math", "", Priority.HIGH, due_date, "School"
    )

    # Act
    results = task_service.search_by_keyword(user, "groceries")

    # Assert
    assert results == [matching_task]


def test_equivalence_keyword_search_matches_description(task_service, user):
    """Category: Equivalence classes"""

    # Arrange
    due_date = datetime(2030, 1, 2, 12, 0, 0)
    matching_task = task_service.create_task(
        user,
        "Errand",
        "Pick up printer paper",
        Priority.LOW,
        due_date,
        "Home",
    )

    # Act
    results = task_service.search_by_keyword(user, "printer")

    # Assert
    assert results == [matching_task]


def test_equivalence_keyword_search_matches_category(task_service, user):
    """Category: Equivalence classes"""

    # Arrange
    due_date = datetime(2030, 1, 2, 12, 0, 0)
    matching_task = task_service.create_task(
        user, "Read chapter", "", Priority.HIGH, due_date, "School"
    )

    # Act
    results = task_service.search_by_keyword(user, "school")

    # Assert
    assert results == [matching_task]


def test_invalid_input_empty_keyword_is_rejected(task_service, user):
    """Category: Invalid input & Boundary edge"""

    # Arrange
    keyword = "   "

    # Act / Assert
    with pytest.raises(InvalidInputError):
        task_service.search_by_keyword(user, keyword)


def test_boundary_sort_empty_task_list_returns_empty_list(task_service, user):
    """Category: Boundary"""

    # Arrange
    expected_tasks = []

    # Act
    tasks = task_service.sort_by_due_date(user)

    # Assert
    assert tasks == expected_tasks


def test_business_logic_sort_by_completion_returns_incomplete_before_complete(
    task_service, user, due_tomorrow
):
    """Category: Business logic"""

    # Arrange
    incomplete_task = task_service.create_task(
        user, "Incomplete", "", Priority.LOW, due_tomorrow, "Work"
    )
    completed_task = task_service.create_task(
        user, "Complete", "", Priority.LOW, due_tomorrow, "Work"
    )
    task_service.mark_complete(user, completed_task.id)

    # Act
    sorted_tasks = task_service.sort_by_completion(user)

    # Assert
    assert sorted_tasks == [incomplete_task, completed_task]
