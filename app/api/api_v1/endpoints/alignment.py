from fastapi import APIRouter, Path, Depends, Body
from uuid import UUID

from ....database.mongo import AsyncIOMotorClient, get_database
# from ....core.aligner import get_aligner, Aligner
from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....models.user import User
from ....models.alignment import AlignmentActionInfoInResponse, AlignmentInUpdate
from ....models.sentence_pair import SentencePairDetailInResponse
from ....services.sentence_pair import SentencePairService
from ....services.alignment import AlignmentService


router = APIRouter(
    prefix="/datasets/{dataset_slug}/sentence_pairs/{sentence_pair_id}",
    tags=["alignment_actions"]
)
@router.post(
    "/acquire",
    response_model=AlignmentActionInfoInResponse
)
async def request_to_acquire_sentence_pair(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_id: UUID = Path(...),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    sentence_pair = await SentencePairService(db, user).get_sentence_pair_from_dataset(sentence_pair_id=sentence_pair_id, dataset_slug=dataset_slug)

    async with await db.start_session() as s:
        async with s.start_transaction():
            alignment_action_info = await AlignmentService(db, user, s).request_to_acquire_sentence_pair(sentence_pair)

            return create_aliased_response(AlignmentActionInfoInResponse(data=alignment_action_info))


@router.post(
    "/mark_as_aligned",
    response_model=AlignmentActionInfoInResponse
)
async def mark_sentence_pair_as_aligned(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_id: UUID = Path(...),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    sentence_pair = await SentencePairService(db, user).get_sentence_pair_from_dataset(sentence_pair_id=sentence_pair_id, dataset_slug=dataset_slug)

    async with await db.start_session() as s:
        async with s.start_transaction():
            alignment_action_info = await AlignmentService(db, user, s).mark_sentence_pair_as_aligned(sentence_pair)

            return create_aliased_response(AlignmentActionInfoInResponse(data=alignment_action_info))


@router.post(
    "/auto_align",
    response_model=SentencePairDetailInResponse,
)
async def generate_alignment_using_nlp_model(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_id: UUID = Path(...),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database),
    # aligner: Aligner = Depends(get_aligner)
):
    sentence_pair = await SentencePairService(db, user).get_sentence_pair_from_dataset(sentence_pair_id=sentence_pair_id, dataset_slug=dataset_slug)

    async with await db.start_session() as s:
        async with s.start_transaction():
            # auto_aligned_sentence_pair = await AlignmentService(db, user, s).auto_align_sentence_pair(aligner, sentence_pair)
            return create_aliased_response(SentencePairDetailInResponse(data=sentence_pair))


@router.put(
    "",
    response_model=SentencePairDetailInResponse,
)
async def update_alignment_of_sentence_pair(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_id: UUID = Path(...),
    alignments_param: AlignmentInUpdate = Body(..., embed=True, alias="alignments"),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    sentence_pair = await SentencePairService(db, user).get_sentence_pair_from_dataset(sentence_pair_id=sentence_pair_id, dataset_slug=dataset_slug)

    async with await db.start_session() as s:
        async with s.start_transaction():
            updated_sentence_pair = await AlignmentService(db, user, s).update_alignments_of_sentence_pair(sentence_pair, alignments_param)

            return create_aliased_response(SentencePairDetailInResponse(data=updated_sentence_pair))
