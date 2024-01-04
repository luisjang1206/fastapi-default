from fastapi import APIRouter
from models import Response
from typing import Annotated
from fastapi import Depends
from dependencies.authorization import get_current_active_user
from models import User


router = APIRouter()


class UserResponse(Response):
    user: User | None


@router.get("/me/", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> UserResponse:
    if not current_user:
        return {"ok": False, "error": "Incorrect Username or Password", "user": None}
    # elif current_user.disabled == True:
    #     return {"ok": True, "error": "User deactivated", "user": None}

    return {"ok": True, "error": None, "user": current_user}
