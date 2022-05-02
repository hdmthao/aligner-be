from uuid import UUID

from .rwmodel import RWModel


class User(RWModel):
    id: UUID
    username: str


class UserInResponse(RWModel):
    data: User
