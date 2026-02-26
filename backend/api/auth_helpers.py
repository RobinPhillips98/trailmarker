"""Various functions used by the API for user authentication.

Defines functions for verifying and hashing passwords, authenticating users,
and creating JSON web tokens.

"""

import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.future import select

from models import User
from schemas import TokenData

from .dependencies import db_dependency

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Uses bcrypt to verify the user's password matches the saved hash

    Args:
        plain_password (str): The plaintext password typed in by the user
        hashed_password (str): The saved hashed password

    Returns:
        bool: True if the passwords match, false if they don't.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes the given password using bcrypt

    Args:
        password (str): The password to be hashed

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


async def get_user(db: db_dependency, username: str) -> User:
    """Fetches a given user from the database using their username

    Args:
        db (db_dependency): A SQLAlchemy database session
        username (str): The username of the user to be fetched

    Returns:
        User: The user fetched from the database
    """
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return user


async def authenticate_user(
    db: db_dependency, username: str, password: str
) -> bool:
    """Checks whether a given username and password matches a saved user

    Attempts to fetch the user from the database using the given username,
    then hashes the user's password and checks it against the saved hash

    Args:
        db (db_dependency): A SQLAlchemy database session
        username (str): The username to be authenticated
        password (str): The password to be authenticated

    Returns:
        bool: True if the authentication is successful, false otherwise
    """
    user = await get_user(db, username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    """Creates a JSON web token using the given data and expiration time

    Args:
        data (dict): The data to encode into the token, typically a username
        expires_delta (timedelta, optional): The amount of time before
            the JWT expires. Defaults to timedelta(minutes=15).

    Returns:
        str: The JSON web token
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: db_dependency, token: str = Depends(oauth2_scheme)
) -> User:
    """Fetches the currently logged in user from the database

    Args:
        db (db_dependency): A SQLAlchemy database session
        token (str, optional): The user's JSON Web Token.
            Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: If the JWT does not have a username stored
        credentials_exception: If the JWT is invalid
        credentials_exception: If the user does not exist

    Returns:
        User: The currently logged in user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(User.username == token_data.username)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
