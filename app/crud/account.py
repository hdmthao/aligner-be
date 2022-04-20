from typing import Union
from ..database.mongo import AsyncIOMotorClient

from ..core.config import db_name, accounts_collection_name
from ..models.account import AccountInDB, AccountInDB, AccountInCreate

async def get_account(conn: AsyncIOMotorClient, accountname: str) -> Union[AccountInDB, None]:
    row = await conn[db_name][accounts_collection_name].find_one({"accountname": accountname})
    if row:
        return AccountInDB(**row)

async def create_account(conn: AsyncIOMotorClient, account: AccountInCreate) -> AccountInDB:
    db_account = AccountInDB(**account.dict())
    db_account.update_password(account.password)

    await conn[db_name][accounts_collection_name].insert_one(db_account.dict())

    return db_account
