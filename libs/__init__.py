from database import db
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
import jwt
from config import config
from models import User, UserWithPassword


# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


class TokenData(BaseModel):
    username: str | None = None


def get_user(username: str) -> UserWithPassword | None:
    try:
        db_cursor = db.cursor(dictionary=True)

        sql = "SELECT * FROM users WHERE username=%s"
        db_cursor.execute(sql, (username,))
        result = db_cursor.fetchone()
        return result  # tuple
    except:
        return None


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User | None:
    access_token = credentials.credentials

    try:
        payload = jwt.decode(
            access_token, config["SECRET_KEY"], algorithms=config["ALGORITHM"]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except Exception as ex:
        return None
    user = get_user(username=token_data.username)
    if user is None:
        return None
    del user["password"]  # must remove passwrod from user dictionary
    return user  # user without password
