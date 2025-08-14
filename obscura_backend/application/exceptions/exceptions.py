class ApplicationException(Exception):
    """Base class for all application exceptions."""
    pass


class ApplicationBug(ApplicationException):
    """Exception raised for bugs in the application."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class UserAlreadyExists(ApplicationException):
    """Exception raised when a user already exists."""
    def __init__(self, username):
        super().__init__(f"User '{username}' already exists.")