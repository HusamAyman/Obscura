class ApplicationException(Exception):
    """Base class for all application exceptions."""
    pass


class ApplicationBug(ApplicationException):
    """Exception raised for bugs in the application."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class UserAlreadyExists(ApplicationException):
    """Exception raised when a user already exists in signup process."""
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists.")

class UserNotFound(ApplicationException):
    """Exception raised when the username not found in the repository"""
    def __inint__(self, username: str):
        super().__init__(f"Uesr '{username}' does not exist")

class UnAuthorizedAccess(ApplicationException):
    """Exception raised when the user enters wrong password"""
    def __init__(self):
        super().__init__("UnAuthorized Access")


class TokenNotFound(ApplicationException):
    """Exception raised when user token not found in the repository"""
    def __init__(self):
        super().__init__("Token Not Found.")
