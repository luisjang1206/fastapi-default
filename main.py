from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers import authentication, users


app = FastAPI()

app.include_router(
    authentication.router,
    prefix="/authentication",
    tags=["users"],
)
app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
