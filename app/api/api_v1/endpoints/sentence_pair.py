from fastapi import APIRouter, Path, Depends, Body, File, UploadFile
from fastapi_pagination import Page 
from starlette.status import HTTP_201_CREATED
from uuid import UUID

from ....database.mongo import AsyncIOMotorClient, get_database
from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....models.user import User
from ....models.sentence_pair import SentencePairInCreate, SentencePairItemInResponse, SentencePairDetailInResponse
from ....services.sentence_pair import SentencePairService
from ....services.dataset import DatasetService


router = APIRouter(
    prefix="/datasets/{dataset_slug}",
    tags=["sentence_pairs"]
)


@router.get(
    "/sentence_pairs",
    response_model=Page[SentencePairItemInResponse],
)
async def get_sentence_pairs_from_dataset(
    dataset_slug: str = Path(..., min_length=1),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    sentence_pairs = await SentencePairService(db, user).get_sentence_pairs_from_dataset_with_paging(dataset_slug)
    return sentence_pairs

@router.post(
    "/sentence_pairs",
    response_model=SentencePairDetailInResponse,
    status_code=HTTP_201_CREATED
)
async def new_sentence_pair_for_dataset(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_params: SentencePairInCreate = Body(..., embed=True, alias="sentence_pair"),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            sentence_pair = await SentencePairService(db, user, session=s).new_sentence_pair_for_dataset(sentence_pair_params, dataset_slug)
            return create_aliased_response(SentencePairDetailInResponse(data=sentence_pair))


@router.get(
    "/sentence_pairs/{sentence_pair_id}",
    response_model=SentencePairDetailInResponse,
)
async def get_sentence_pair_from_dataset(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_id: UUID = Path(...),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    sentence_pair = await SentencePairService(db, user).get_sentence_pair_from_dataset(sentence_pair_id, dataset_slug)
    return create_aliased_response(SentencePairDetailInResponse(data=sentence_pair))


@router.post(
    "/import",
)
async def import_sentence_pairs_from_file(
    dataset_slug: str = Path(..., min_length=1),
    user_file: UploadFile = File(...),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    dataset = await DatasetService(db, user).get_dataset(dataset_slug)

    response = await SentencePairService(db, user).import_sentence_pairs_from_file_to_dataset(user_file, dataset)

    return { "data": response }
