from fastapi import APIRouter, Depends

from models import User
from schemas import UserResponse

from ..auth_helpers import get_current_active_user

router = APIRouter()


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
