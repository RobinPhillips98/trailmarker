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
def register_user(user: UserCreate, db: db_dependency):
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered."
        )
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token")
async def login_for_access_token(
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
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
