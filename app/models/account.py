from .rwmodel import RWModel
from ..core.security import generate_salt, get_password_hash, verify_password


class AccountBase(RWModel):
    username: str


class AccountInDB(AccountBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def update_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)

class Account(AccountBase):
    token: str


class AccountInResponse(RWModel):
    data: Account


class AccountInLogin(RWModel):
    username: str
    password: str


class AccountInCreate(AccountInLogin):
    username: str
