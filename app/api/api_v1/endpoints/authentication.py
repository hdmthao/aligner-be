from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.user import User, UserInLogin, UserInCreate, UserInResponse, UserInDB
from ....core.security import get_password_hash
from ....crud.user import create_user

router = APIRouter()

@router.post("/users/login", response_model=UserInResponse, tags=["authentication"])
async def login(
    user: UserInLogin = Body(..., embed=True)
):
    db_user = UserInDB(username='admin',salt='salt', hashed_password=get_password_hash('saltadmin'), createdAt=None, updatedAt=None)
    if not db_user or not db_user.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    token = "user_token"
    return UserInResponse(user=User(**db_user.dict(), token=token))

@router.post(
    "/users",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED
)
async def register(
        user: UserInCreate = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_user = await create_user(db, user)
            token = "user_token"

            return UserInResponse(user=User(**db_user.dict(), token=token))
