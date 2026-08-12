"""Functions for API calls related to users

Defines functions to be used when a request is made to the /users routes of the
API, including getting the current user.

"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth_helpers import (
    get_current_user,
    get_password_hash,
    get_user,
    verify_password,
)
from api.exceptions import BadRequestException, InternalServerError
from db import get_db
from models import User
from schemas import UserDelete, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.get("/me/", response_model=UserResponse)
async def read_user(current_user: User = Depends(get_current_user)) -> User:
    """Fetches the currently logged in user from the database if it exists.

    Args:
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Returns:
        User: The currently logged in user
    """
    return current_user


@router.patch("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    request: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Updates the current user's username or password.

    Args:
        request (UserUpdate): A dictionary containing the new username or
            password, as well as the old password for verification.
        db (AsyncSession): A SQLAlchemy database session
        current_user (User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        BadRequestException: If the user's password is incorrect, or if
            the requested username already exists.
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        UserResponse: The updated user object
    """
    try:
        if not verify_password(
            request.old_password, current_user.hashed_password
        ):
            raise BadRequestException(
                detail="Password invalid. Please try again",
            )

        update_data = {}
        if request.username:
            db_user = await get_user(db, request.username)
            if db_user:
                raise BadRequestException(
                    detail="Username already registered.",
                )
            update_data["username"] = request.username
        if request.password:
            hashed_password = get_password_hash(request.password)
            update_data["hashed_password"] = hashed_password

        for key, value in update_data.items():
            setattr(current_user, key, value)

        await db.commit()
        await db.refresh(current_user)

        return current_user

    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in update_user")
        raise InternalServerError()


@router.delete(
    "/", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    request: UserDelete,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Deletes the current user's account and all records associated with it.

    Args:
        request (UserDelete): A request containing the user's password, for
            verification.
        db (AsyncSession): A SQLAlchemy database session
        current_user (User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        BadRequestException: If the user's password is incorrect
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        BasicResponse: A message confirming account deletion.
    """
    try:
        if not verify_password(request.password, current_user.hashed_password):
            raise BadRequestException(
                detail="Password invalid. Please try again",
            )

        await db.delete(current_user)
        await db.commit()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in delete_user")
        raise InternalServerError()
