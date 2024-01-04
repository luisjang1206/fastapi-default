from pydantic import BaseModel


class Response(BaseModel):
    ok: bool
    error: str | None


class User(BaseModel):
    id: int
    username: str
    name: str


class UserWithPassword(User):
    password: str
