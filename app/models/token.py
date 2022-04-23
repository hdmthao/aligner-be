from uuid import UUID
from .rwmodel import RWModel

class TokenPayload(RWModel):
    id: UUID
    username: str

class Token(RWModel):
    access_token: str
    token_type: str

class TokenInResponse(Token):
    pass
