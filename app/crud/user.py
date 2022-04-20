from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from ..database.mongo import AsyncIOMotorClient
from .account import get_account
from ..models.user import User

async def get_user_for_account(conn: AsyncIOMotorClient, username: str) -> User:
    account = await get_account(conn, username)
    if not account:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"User {username} not found"
        )

    user = User(**account.dict())

    return user
