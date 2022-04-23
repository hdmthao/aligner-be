from fastapi import APIRouter, Path, Depends, Body

from ....database.mongo import AsyncIOMotorClient, get_database
from ....models.sentence_pair import SentencePairInResponse, SentencePairInCreate
from ....models.user import User
from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....services.sentence_pair import SentencePairService

router = APIRouter(
    prefix="/datasets/{dataset_slug}",
    tags=["sentence_pairs"]
)

# @router.get(
#     "/sentence_pairs",
#     response_model=ManySentencePairsInResponse,
#     description="Work In Progress"
# )
# async def get_sentence_pairs_from_dataset(
#     offset: int = Query(0, ge=0),
#     limit: int = Query(20, gt=0),
#     dataset_slug: str = Path(..., min_length=1),
#     user: User = Depends(get_current_user()),
#     db: AsyncIOMotorClient = Depends(get_database)
# ):
#     await DatasetService(db, user).get_dataset(dataset_slug)
#     return create_aliased_response(ManySentencePairsInResponse(data=[], sentence_pairs_count=0))

@router.post(
    "/sentence_pairs"
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
            return create_aliased_response(SentencePairInResponse(data=sentence_pair))


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
    sentence_pair 


# @router.post(
#     "/import",
#     description="Work In Progress"
# )
# async def import_sentence_pairs_from_file(
#     dataset_slug: str = Path(..., min_length=1),
#     file: UploadFile = File(...),
#     user: User = Depends(get_current_user()),
#     db: AsyncIOMotorClient = Depends(get_database)
# ):
#     return {}
