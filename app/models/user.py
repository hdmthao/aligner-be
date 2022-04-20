from .rwmodel import RWModel


class User(RWModel):
    username: str


class UserInResponse(RWModel):
    data: User
