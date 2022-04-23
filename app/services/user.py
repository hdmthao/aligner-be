from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from uuid import UUID

from .base import AppService
from .account import AccountCRUD
from ..models.user import User


class UserService(AppService):
    async def get_user_for_account(self, id: UUID) -> User:
        account = await AccountCRUD(self.db).get_account(id)
        if not account:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"User not found id={id}"
            )

        return User(**account.dict())
