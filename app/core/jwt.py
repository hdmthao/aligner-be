from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from ..database.mongo import AsyncIOMotorClient, get_database
from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.user import User
from ..models.token import TokenPayload
from ..crud.account import get_account

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


async def _get_current_user(
    db: AsyncIOMotorClient = Depends(get_database), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    db_account = await get_account(db, token_data.username)
    if not db_account:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Account not found")

    user = User(**db_account.dict())
    return user


def get_current_user():
    return _get_current_user


def create_access_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
