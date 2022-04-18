from fastapi import APIRouter, Body
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from ....models.user import User, UserInLogin, UserInResponse, UserInDB
from ....core.security import get_password_hash

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
