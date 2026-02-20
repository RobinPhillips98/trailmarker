"""Functions for API calls related to authentication.

Defines functions for when requests are made to either the /register or /token
route in the API, including registering and logging in useres.

"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import User
from schemas import Token, UserCreate, UserResponse

from ..auth_helpers import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)
from ..dependencies import db_dependency

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: db_dependency) -> UserResponse:
    """Adds a given user to the database.

    Takes in a user andchecks that its username doesn't already exist in the
    datebase. If not, it hashes the given password and saves the username and
    password in the database

    Args:
        user (UserCreate): An object containing information about a new user,
            including their username and password.
        db (db_dependency): A SQLAlchemy database session

    Raises:
        HTTPException: The given username already exists in the database.

    Returns:
        UserResponse: A dictionary containing information about the new user
    """
    db_user = await get_user(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered."
        )
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@router.post("/token")
async def login_for_access_token(
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Validates a username and password and returns a JWT on success.

    Args:
        db (db_dependency): A SQLAlchemy database session
        form_data (OAuth2PasswordRequestForm, optional): An OAuth form holding
            a user's username and password. Defaults to Depends().

    Raises:
        HTTPException: There is no match for the given username and password

    Returns:
        Token: A JSON Web Token used to authenticate the user
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
