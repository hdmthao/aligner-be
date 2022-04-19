from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from ..database.mongo import AsyncIOMotorClient
from .user import get_user_by_username

async def check_free_username(
    conn: AsyncIOMotorClient, username: str
):
    user_by_username = await get_user_by_username(conn, username)
    if user_by_username:
        raise HTTPException(
            status_code = HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this username already exists",
        )
