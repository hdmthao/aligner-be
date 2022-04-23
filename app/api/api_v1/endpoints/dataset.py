from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.status import HTTP_201_CREATED

from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.dataset import DatasetInCreate, DatasetInResponse, ManyDatasetsInResponse, DatasetFilterParams
from ....models.user import User
from ....services.dataset import DatasetService

router = APIRouter()

@router.get(
    "/datasets",
    response_model=ManyDatasetsInResponse,
    tags=["datasets"]
)
async def get_datasets(
    code: str = "",
    src_lang: str = "",
    tgt_lang: str = "",
    offset: int = Query(0, ge=0),
    limit: int = Query(20, gt=0),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    filters = DatasetFilterParams(
        code=code,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
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
    dataset_params: DatasetInCreate = Body(..., embed=True),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    dataset = await DatasetService(db, user).new_dataset(dataset_params)

    return create_aliased_response(DatasetInResponse(data=dataset))
