from .rwmodel import RWModel
from ..core.security import generate_salt, get_password_hash, verify_password


class UserBase(RWModel):
    username: str


class UserInDB(UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def update_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)

class User(UserBase):
    token: str


class UserInResponse(RWModel):
    data: User


class UserInLogin(RWModel):
    username: str
    password: str


class UserInCreate(UserInLogin):
    username: str
