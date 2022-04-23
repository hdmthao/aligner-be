from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from ....core.jwt import create_access_token
from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.account import Account, AccountInLogin, AccountInCreate, AccountInResponse
from ....models.token import TokenPayload, TokenInResponse
from ....crud.account import create_account, get_account_by_username
from ....crud.shortcuts import check_free_username

router = APIRouter()

@router.post("/accounts/login", response_model=AccountInResponse, tags=["authentication"])
async def login(
    account: AccountInLogin = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    db_account = await get_account_by_username(db, account.username)
    if not db_account or not db_account.check_password(account.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    token = create_access_token(data = TokenPayload(**db_account.dict()))

    return AccountInResponse(data=Account(**db_account.dict(), token=token))

@router.post(
    "/accounts",
    response_model=AccountInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED
)
async def register(
        account: AccountInCreate = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    await check_free_username(db, account.username)
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_account = await create_account(db, account)
            token = create_access_token(data = TokenPayload(**db_account.dict()))

            return AccountInResponse(data=Account(**db_account.dict(), token=token))

@router.post("/token", response_model=TokenInResponse, tags=["authentication"])
async def login_for_access_token(
    account: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_database)
):
    db_account = await get_account_by_username(db, account.username)
    if not db_account or not db_account.check_password(account.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    token = create_access_token(data = TokenPayload(**db_account.dict()))

    return TokenInResponse(access_token=token, token_type="bearer")
