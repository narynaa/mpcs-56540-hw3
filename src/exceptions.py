class TodoError(Exception):
    """Base class for domain-specific errors."""


class InvalidInputError(TodoError):
    """Raised when user input is invalid."""


class AuthenticationError(TodoError):
    """Raised when login credentials are invalid."""


class UserAlreadyExistsError(TodoError):
    """Raised when signing up with an existing username."""


class TaskNotFoundError(TodoError):
    """Raised when a task does not exist."""


class UnauthorizedTaskAccessError(TodoError):
    """Raised when a user attempts to access another user's task."""


class ReminderError(TodoError):
    """Raised when reminder setup or delivery fails."""
