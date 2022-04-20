from slugify import slugify
from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED

from ....core.jwt import get_current_user_authorizer
from ....core.utils import create_aliased_response
from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.dataset import DatasetInCreate, DatasetInResponse
from ....models.user import User
from ....crud.dataset import get_dataset_by_slug, create_dataset_by_slug

router = APIRouter()

@router.post(
    "/datasets",
    response_model=DatasetInResponse,
    tags=["dataset"],
    status_code=HTTP_201_CREATED
)
async def create_new_dataset(
    dataset: DatasetInCreate = Body(..., embed=True),
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    dataset_by_slug = await get_dataset_by_slug(db, slugify(dataset.code))
    if dataset_by_slug:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dataset already exists slug='{dataset_by_slug.slug}'",
        )

    db_dataset = await create_dataset_by_slug(db, dataset, user.username)
    return create_aliased_response(DatasetInResponse(data=db_dataset))
