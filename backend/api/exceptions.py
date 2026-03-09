"""Defines exceptions used by the API"""

from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    """Returns a 400 exception when a user makes a request that is invalid.

    Attributes:
        detail: The error message shown to the user
    """

    def __init__(self, detail: str = "Bad Request"):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail


class ForbiddenException(HTTPException):
    """Returns a 403 exception when a user attempts an unauthorized action.

    Attributes:
        action: The action the user attempted
        route: The API route the user attempts the action on
    """

    def __init__(self, action: str = None, route: str = None):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"Not authorized to {action} this {route}"


class NotFoundException(HTTPException):
    """Returns a 404 exception when a route fails to find requested data

    Attributes:
        route: The API route the data was requested from
    """

    def __init__(self, route: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"{route} not found"


class InternalServerError(HTTPException):
    """Returns a 500 exception when an error occurs during a route.

    Attributes:
        message: The detail to display about the error
    """

    def __init__(self, message: str):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = f"Internal Server Error: {message}"
