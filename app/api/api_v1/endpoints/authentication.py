from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED

from ....database.mongo import AsyncIOMotorClient, get_database
from ....core.utils import create_aliased_response
from ....models.token import TokenInResponse
from ....models.account import AccountInLogin, AccountInCreate, AccountInResponse
from ....services.account import AccountService

router = APIRouter()

@router.post("/accounts/login", response_model=AccountInResponse, tags=["authentication"])
async def login(
    account_params: AccountInLogin = Body(..., embed=True, alias="account"), db: AsyncIOMotorClient = Depends(get_database)
):
    account = await AccountService(db).login_and_generate_new_token(account_params)

    return create_aliased_response(AccountInResponse(data=account))

@router.post(
    "/accounts",
    response_model=AccountInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED
)
async def register(
        account_params: AccountInCreate = Body(..., embed=True, alias="account"), db: AsyncIOMotorClient = Depends(get_database)
):
    await AccountService(db).check_free_username(account_params.username)

    async with await db.start_session() as s:
        async with s.start_transaction():
            account = await AccountService(db).create_account_and_generate_token(account_params)

            return create_aliased_response(AccountInResponse(data=account))

@router.post("/token", response_model=TokenInResponse, tags=["authentication"])
async def generate_access_token(
    account_params: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_database)
):
    account = await AccountService(db).login_and_generate_new_token(AccountInLogin(username=account_params.username, password=account_params.password))

    return create_aliased_response(TokenInResponse(access_token=account.token, token_type="bearer"))
