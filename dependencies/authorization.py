from typing import Annotated
from database import db
from fastapi import Depends
from models import User
from libs import get_current_user
from models import UserWithPassword


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserWithPassword | None:
    ## do something for a disabled user

    # if current_user.disabled:
    #     return None
    return current_user
