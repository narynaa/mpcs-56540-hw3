import pytest

from src.exceptions import (
    AuthenticationError,
    InvalidInputError,
    UserAlreadyExistsError,
)


def test_happy_path_user_can_sign_up(auth_service):
    """Category: Happy path"""

    # Arrange
    username = "alice"
    password = "password123"

    # Act
    user = auth_service.sign_up(username, password)

    # Assert
    assert user.username == "alice"


def test_happy_path_user_can_log_in_after_signing_up(auth_service):
    """Category: Happy path"""

    # Arrange
    auth_service.sign_up("alice", "password123")

    # Act
    user = auth_service.log_in("alice", "password123")

    # Assert
    assert user.username == "alice"


def test_invalid_input_blank_username_is_rejected(auth_service):
    """Category: Invalid input"""

    # Arrange
    username = "   "

    # Act / Assert
    with pytest.raises(InvalidInputError):
        auth_service.sign_up(username, "password123")


def test_invalid_input_blank_password_is_rejected(auth_service):
    """Category: Invalid input"""

    # Arrange
    password = ""

    # Act / Assert
    with pytest.raises(InvalidInputError):
        auth_service.sign_up("alice", password)


def test_exception_duplicate_username_raises_named_exception(auth_service):
    """Category: Exception handling"""

    # Arrange
    auth_service.sign_up("alice", "password123")

    # Act / Assert
    with pytest.raises(UserAlreadyExistsError):
        auth_service.sign_up("alice", "different-password")


def test_exception_wrong_password_raises_authentication_error(auth_service):
    """Category: Exception handling"""

    # Arrange
    auth_service.sign_up("alice", "password123")

    # Act / Assert
    with pytest.raises(AuthenticationError):
        auth_service.log_in("alice", "wrong-password")


def test_exception_unknown_username_raises_authentication_error(auth_service):
    """Category: Exception handling"""

    # Arrange
    username = "missing-user"

    # Act / Assert
    with pytest.raises(AuthenticationError):
        auth_service.log_in(username, "password123")
