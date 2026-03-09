"""Functions for API calls related to users

Defines functions to be used when a request is made to the /users routes of the
API, including getting the current user.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import Character, Encounter, User
from schemas import BasicResponse, UserDelete, UserResponse, UserUpdate

from ..auth_helpers import (
    get_current_user,
    get_password_hash,
    get_user,
    verify_password,
)
from ..dependencies import db_dependency
from ..exceptions import BadRequestException, InternalServerError

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


@router.patch(
    "/users/", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user(
    request: UserUpdate,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Updates the current user's username or password.

    Args:
        request (UserUpdate): A dictionary containing the new username or
            password, as well as the old password for verification.
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        BadRequestException: If the user's password is incorrect, or if
            the requested username already exists.
        http_err: A caught HTTP error
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

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in update_user: {str(e)}")
        raise InternalServerError(message=str(e))


@router.delete(
    "/users/", response_model=BasicResponse, status_code=status.HTTP_200_OK
)
async def delete_user(
    request: UserDelete,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
) -> BasicResponse:
    """Deletes the current user's account and all records associated with it.

    Args:
        request (UserDelete): A request containing the user's password, for
            verification.
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        BadRequestException: If the user's password is incorrect
        http_err: A caught HTTP error
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        BasicResponse: A message confirming account deletion.
    """
    if not verify_password(request.password, current_user.hashed_password):
        raise BadRequestException(
            detail="Password invalid. Please try again",
        )

    try:
        # First, delete all characters associated with user
        stmt = (
            select(Character)
            .options(selectinload(Character.user))
            .where(Character.user_id == current_user.id)
        )

        result = await db.execute(stmt)
        characters = result.scalars()

        for character in characters:
            await db.delete(character)

        # Next, delete all encounters associated with the user
        stmt = (
            select(Encounter)
            .options(selectinload(Encounter.user))
            .where(Encounter.user_id == current_user.id)
        )

        result = await db.execute(stmt)
        encounters = result.scalars()

        for encounter in encounters:
            await db.delete(encounter)

        # Finally, delete the user
        await db.delete(current_user)
        await db.commit()

        return {"message": "User deleted"}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in delete_user: {str(e)}")
        raise InternalServerError(message=str(e))
