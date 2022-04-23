from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClientSession


from ..database.mongo import AsyncIOMotorClient
from ..models.user import User

class DBSessionMixin:
    def __init__(self, db: AsyncIOMotorClient, current_user: Optional[User] = None, session: Optional[AsyncIOMotorClientSession] = None):
        self.db = db
        self.current_user = current_user
        self.session = session


class AppService(DBSessionMixin):
    pass


class AppCRUD(DBSessionMixin):
    pass
