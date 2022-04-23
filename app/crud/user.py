from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from uuid import UUID

from ..database.mongo import AsyncIOMotorClient
from .account import get_account
from ..models.user import User

async def get_user_for_account(conn: AsyncIOMotorClient, id: UUID) -> User:
    account = await get_account(conn, id)
    if not account:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User not found id={id}"
        )

    user = User(**account.dict())

    return user
