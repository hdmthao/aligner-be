from fastapi import APIRouter, Path, Depends, Query, UploadFile, File

from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.sentence_pair import SentencePairInResponse, ManySentencePairsInResponse
from ....models.user import User
from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....services.dataset import DatasetService

router = APIRouter(
    prefix="/datasets/{dataset_slug}",
    tags=["sentence_pairs"]
)

@router.get(
    "/sentence_pairs",
    response_model=ManySentencePairsInResponse,
    description="Work In Progress"
)
async def get_sentence_pairs_from_dataset(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, gt=0),
    dataset_slug: str = Path(..., min_length=1),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    await DatasetService(db, user).get_dataset(dataset_slug)
    return create_aliased_response(ManySentencePairsInResponse(data=[], sentence_pairs_count=0))


@router.get(
    "/sentence_pairs/{pair_slug}",
    response_model=SentencePairInResponse,
    description="Work In Progress"
)
async def get_sentence_pair_from_dataset(
    dataset_slug: str = Path(..., min_length=1),
    pair_slug: str = Path(..., min_length=1),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    return {}


@router.post(
    "/import",
    description="Work In Progress"
)
async def import_sentence_pairs_from_file(
    dataset_slug: str = Path(..., min_length=1),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    return {}
