from datetime import datetime, timedelta
import jwt

from .base import AppService
from ..core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.token import TokenPayload


ALGORITHM = "HS256"
access_token_jwt_subject = "access"


class JwtService(AppService):
    def create_access_token(self, *, data: TokenPayload) -> str:
        to_encode = data.dict().copy()
        to_encode.update({"id": str(to_encode["id"])})
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
        encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
        return encoded_jwt
