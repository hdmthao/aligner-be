from slugify import slugify
from fastapi import APIRouter, Body, Depends, Path
from starlette.exceptions import HTTPException
from starlette.status import  HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.dataset import DatasetInCreate, DatasetInResponse, ManyDatasetsInResponse
from ....models.user import User
from ....crud.dataset import get_dataset_by_slug, create_dataset_by_slug

router = APIRouter()

@router.get(
    "/datasets",
    response_model=ManyDatasetsInResponse,
    tags=["datasets"]
)
async def get_datasets(
):
    pass


@router.get(
    "/datasets/{slug}",
    response_model=DatasetInResponse,
    tags=["datasets"]
)
async def get_dataset(
    slug: str = Path(..., min_length=1),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    dataset = await get_dataset_by_slug(db, slug, user)
    if not dataset:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Dataset with slug '{slug}' not found"
        )

    return create_aliased_response(DatasetInResponse(data=dataset))


@router.post(
    "/datasets",
    response_model=DatasetInResponse,
    tags=["datasets"],
    status_code=HTTP_201_CREATED
)
async def create_new_dataset(
    dataset: DatasetInCreate = Body(..., embed=True),
    user: User = Depends(get_current_user()),
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
