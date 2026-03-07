"""Functions for API calls related to users

Defines functions to be used when a request is made to the /users routes of the
API, including getting the current user.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import Character, Encounter, User
from schemas import UserDelete, UserResponse

from ..auth_helpers import get_current_user, verify_password
from ..dependencies import db_dependency
from ..exceptions import (
    InternalServerError,
    NotAuthorizedException,
)

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


@router.delete(
    "/users/", response_model=object, status_code=status.HTTP_200_OK
)
async def delete_user(
    request: UserDelete,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
) -> object:
    if not verify_password(request.password, current_user.hashed_password):
        raise NotAuthorizedException(
            detail="Password invalid. Please try again"
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
        print(f"Error in update_character: {str(e)}")
        raise InternalServerError(message=str(e))
