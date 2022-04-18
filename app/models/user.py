from typing import Optional

from .dbmodel import DBModelMixin
from .rwmodel import RWModel
from ..core.security import verify_password


class UserBase(RWModel):
    username: str


class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

class User(UserBase):
    token: str


class UserInResponse(RWModel):
    user: User


class UserInLogin(RWModel):
    username: str
    password: str

