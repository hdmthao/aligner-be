from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError
from typing import Optional
from fastapi import Depends, Header
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from ..database.mongo import AsyncIOMotorClient, get_database
from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN_PREFIX
from ..models.user import User
from ..models.token import TokenPayload
from ..crud.account import get_account

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

def _get_authorization_token(authorization: str = Header(...)):
    token_prefix, token = authorization.split(" ")
    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization type"
        )

    return  token


async def _get_current_user(
    db: AsyncIOMotorClient = Depends(get_database), token: str = Depends(_get_authorization_token)
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


def _get_authorization_token_optional(authorization: str = Header(None)):
    if authorization:
        return _get_authorization_token(authorization)
    return ""


async def _get_current_user_optional(
    db: AsyncIOMotorClient = Depends(get_database), token: str = Depends(_get_authorization_token_optional)
) -> Optional[User]:
    if token:
        return await _get_current_user(db, token)

    return None


def get_current_user_authorizer(*, required: bool = True):
    if required:
        return _get_current_user
    else:
        return _get_current_user_optional

def create_access_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
