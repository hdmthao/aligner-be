from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from ....core.jwt import create_access_token
from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.user import User, UserInLogin, UserInCreate, UserInResponse
from ....crud.user import create_user, get_user_by_username
from ....crud.shortcuts import check_free_username

router = APIRouter()

@router.post("/users/login", response_model=UserInResponse, tags=["authentication"])
async def login(
    user: UserInLogin = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    db_user = await get_user_by_username(db, user.username)
    if not db_user or not db_user.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    token = create_access_token(data = { "username": db_user.username })

    return UserInResponse(data=User(**db_user.dict(), token=token))

@router.post(
    "/users",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED
)
async def register(
        user: UserInCreate = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    await check_free_username(db, user.username)
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_user = await create_user(db, user)
            token = create_access_token(data = { "username": db_user.username })

            return UserInResponse(data=User(**db_user.dict(), token=token))
