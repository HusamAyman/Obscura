from fastapi import HTTPException
from starlette import status


class APIException(HTTPException):
    """Base API Exception with default status and message"""
    status_code = 500
    detail = "A server error occurred."

    def __init__(self, detail: str | None = None, headers: dict[str, str] | None = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail, headers=headers)

class InternalServerError(HTTPException):
    """Exception raised for internal server errors."""
    def __init__(self, detail: str | None = None):
        detail = f"Server error occurred due to {detail}"
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail or "Internal Server Error")

class HTTPUserAlreadyExists(HTTPException):
    """Exception raised when a user already exists."""
    def __init__(self, username: str):
        detail = f"User '{username}' already exists."
        super().__init__(status_code=status.HTTP_409_CONFLICT,detail=detail)

class HTTPUserNotFound(HTTPException):
    """Exception raised when the username not found in the system"""
    def __init__(self, username: str):
        detail = f"User '{username}' not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class HTTPUnauthorizedAccess(HTTPException):
    """Exception raised when the user enters wrong username or password"""
    def __init__(self, message: str = ""):
        detail = f"Access denied .{message}"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class HTTPTokenNotFound(HTTPException):
    """Exception raised when the user token is not found in the system"""
    def __init__(self):
        detail = "User token not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class HTTPWrongPassword(HTTPException):
    """Exception raised when the user to change password then enters wrong old password"""
    def __init__(self):
        detail = "Wrong Password."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class HTTPDuplicatePassword(HTTPException):
    """Exception raised when the new password is same as old password"""
    def __init__(self):
        detail = "New Password cannot be same as old password."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class HTTPInvalidRecoveryKey(HTTPException):
    """Exception raised when the user provides wrong recovery key"""
    def __init__(self):
        detail = "Invalid recovery key, please make sure you have entered the correct recovery key."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)