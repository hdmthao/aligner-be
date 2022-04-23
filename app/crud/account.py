from typing import Optional
from uuid import UUID

from ..database.mongo import AsyncIOMotorClient
from ..core.config import db_name, accounts_collection_name
from ..models.account import AccountInDB, AccountInDB, AccountInCreate

async def get_account(conn: AsyncIOMotorClient, id: UUID) -> Optional[AccountInDB]:
    row = await conn[db_name][accounts_collection_name].find_one({"id": id})
    if row:
        return AccountInDB(**row)

async def get_account_by_username(conn: AsyncIOMotorClient, username: str) -> Optional[AccountInDB]:
    row = await conn[db_name][accounts_collection_name].find_one({"username": username})
    if row:
        return AccountInDB(**row)

async def create_account(conn: AsyncIOMotorClient, account: AccountInCreate) -> AccountInDB:
    db_account = AccountInDB(**account.dict())
    db_account.update_password(account.password)

    await conn[db_name][accounts_collection_name].insert_one(db_account.dict())

    return db_account
