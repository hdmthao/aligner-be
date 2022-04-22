from typing import Optional


from ..database.mongo import AsyncIOMotorClient
from ..models.user import User

class DBSessionMixin:
    def __init__(self, db: AsyncIOMotorClient, current_user: Optional[User] = None):
        self.db = db
        self.current_user = current_user


class AppService(DBSessionMixin):
    pass
