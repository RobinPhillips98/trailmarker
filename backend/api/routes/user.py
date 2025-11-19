"""Functions for API calls related to users

Defines functions to be used when a request is made to the /users routes of the
API, including getting the current user.

"""

from fastapi import APIRouter, Depends

from models import User
from schemas import UserResponse

from ..auth_helpers import get_current_user

router = APIRouter()


@router.get("/users/me/", response_model=UserResponse)
async def read_user(current_user: User = Depends(get_current_user)) -> User:
    """Fetches the currently logged in user from the database if it exists.

    Args:
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Returns:
        User: The currently logged in user
    """
    return current_user
