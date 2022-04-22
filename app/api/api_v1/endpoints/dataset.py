from slugify import slugify
from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.exceptions import HTTPException
from starlette.status import  HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED

from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.dataset import DatasetInCreate, DatasetInResponse, ManyDatasetsInResponse, DatasetFilterParams, Dataset
from ....models.user import User
from ....crud.dataset import get_dataset_by_slug, create_dataset_by_slug
from ....crud.user import get_user_for_account
from ....services.dataset import DatasetService

router = APIRouter()

@router.get(
    "/datasets",
    response_model=ManyDatasetsInResponse,
    tags=["datasets"]
)
async def get_datasets(
    code: str = "",
    source_lang: str = "",
    target_lang: str = "",
    offset: int = Query(0, ge=0),
    limit: int = Query(20, gt=0),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    filters = DatasetFilterParams(
        code=code,
        source_lang=source_lang,
        target_lang=target_lang,
        limit=limit,
        offset=offset
    )

    datasets = await DatasetService(db, user).get_datasets_of_current_user_with_filters(filters)

    return create_aliased_response(ManyDatasetsInResponse(data=datasets, datasets_count=len(datasets)))
    

@router.get(
    "/datasets/{dataset_slug}",
    response_model=DatasetInResponse,
    tags=["datasets"]
)
async def get_dataset(
    dataset_slug: str = Path(..., min_length=1),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    dataset = await DatasetService(db, user).get_dataset(dataset_slug)

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
    author = await get_user_for_account(db, db_dataset.author_id)

    return create_aliased_response(DatasetInResponse(data=Dataset(**db_dataset.dict(), author=author, sentence_pairs_count=0)))
