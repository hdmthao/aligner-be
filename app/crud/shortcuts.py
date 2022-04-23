from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from ..database.mongo import AsyncIOMotorClient
from .account import get_account_by_username

async def check_free_username(
    conn: AsyncIOMotorClient, username: str
):
    account = await get_account_by_username(conn, username)
    if account:
        raise HTTPException(
            status_code = HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Account with this username already exists",
        )
