from ..database.mongo import AsyncIOMotorClient

from ..core.config import db_name, users_collection_name
from ..models.user import UserInCreate, UserInDB


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    db_user = UserInDB(**user.dict())
    db_user.update_password(user.password)

    await conn[db_name][users_collection_name].insert_one(db_user.dict())

    return db_user
