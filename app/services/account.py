from typing import Optional
from uuid import UUID
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY

from .base import AppService, AppCRUD
from .jwt import JwtService
from ..core.config import db_name, accounts_collection_name
from ..models.account import Account, AccountInDB, AccountInCreate, AccountInLogin
from ..models.token import TokenPayload


class AccountService(AppService):
    async def check_free_username(self, username: str):
        account = await AccountCRUD(self.db).get_account_by_username(username)
        if account:
            raise HTTPException(
                status_code = HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Account with this username already exists",
            )


    async def login_and_generate_new_token(self, account_params: AccountInLogin) -> Account:
        db_account = await AccountCRUD(self.db).get_account_by_username(account_params.username)
        if not db_account or not db_account.check_password(account_params.password):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
            )

        token = JwtService(self.db).create_access_token(data = TokenPayload(**db_account.dict()))

        return Account(**db_account.dict(), token=token)


    async def create_account_and_generate_token(self, account_params: AccountInCreate) -> Account:
        db_account = await AccountCRUD(self.db).create_account(account_params)
        if not db_account:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Something went wrong when creating account",
            )
        token = JwtService(self.db).create_access_token(data = TokenPayload(**db_account.dict()))

        return Account(**db_account.dict(), token=token)


class AccountCRUD(AppCRUD):
    async def get_account(self, id: UUID) -> Optional[AccountInDB]:
        row = await self.db[db_name][accounts_collection_name].find_one({"id": id})
        if row:
            return AccountInDB(**row)


    async def get_account_by_username(self, username: str) -> Optional[AccountInDB]:
        row = await self.db[db_name][accounts_collection_name].find_one({"username": username})
        if row:
            return AccountInDB(**row)


    async def create_account(self, account: AccountInCreate) -> AccountInDB:
        db_account = AccountInDB(**account.dict())
        db_account.update_password(account.password)

        await self.db[db_name][accounts_collection_name].insert_one(db_account.dict())

        return db_account
