from fastapi import APIRouter, Body

# from libs import get_user, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from libs import get_user
from models import Response
from libs.password import verify_password
from datetime import datetime, timedelta
import jwt
from config import config
from models import User

router = APIRouter()


class TokenResponse(Response):
    access_token: str | None


def authenticate_user(username: str, password: str) -> User:
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encoded_jwt = jwt.encode(
        to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"]
    )
    return encoded_jwt


@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(
    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    username: str = Body(),
    password: str = Body(),
) -> TokenResponse:
    user = authenticate_user(username, password)
    if not user:
        return {
            "ok": False,
            "error": "Incorrect username or password",
            "access_token": None,
        }
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires,  # the first item of user tuple is username
    )

    return {"ok": True, "error": None, "access_token": access_token}
