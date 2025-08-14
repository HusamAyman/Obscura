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