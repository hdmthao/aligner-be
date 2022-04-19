from datetime import datetime, timedelta
from typing import Optional

import jwt

from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
