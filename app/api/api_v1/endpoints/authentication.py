from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from ....core.jwt import create_access_token
from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.account import Account, AccountInLogin, AccountInCreate, AccountInResponse
from ....crud.account import create_account, get_account
from ....crud.shortcuts import check_free_username

router = APIRouter()

@router.post("/accounts/login", response_model=AccountInResponse, tags=["authentication"])
async def login(
    account: AccountInLogin = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    db_account = await get_account(db, account.username)
    if not db_account or not db_account.check_password(account.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    token = create_access_token(data = { "accountname": db_account.username })

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
            token = create_access_token(data = { "username": db_account.username })

            return AccountInResponse(data=Account(**db_account.dict(), token=token))
