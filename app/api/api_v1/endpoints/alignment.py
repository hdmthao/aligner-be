from fastapi import APIRouter, Path, Depends, Body
from uuid import UUID

from ....database.mongo import AsyncIOMotorClient, get_database
from ....core.aligner import get_aligner, Aligner
from ....core.jwt import get_current_user
from ....core.utils import create_aliased_response
from ....models.user import User
from ....models.alignment import AlignmentActionInfoInResponse, AlignmentInUpdate, ReleaseAlignmentStatus
from ....models.sentence_pair import SentencePairDetailInResponse
from ....models.dataset import DatasetDetailInResponse
from ....services.sentence_pair import SentencePairService
from ....services.alignment import AlignmentService
from ....services.dataset import DatasetService


router = APIRouter(
    tags=["alignment_actions"]
)
@router.post(
    "/datasets/{dataset_slug}/sentence_pairs/{sentence_pair_id}/acquire",
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
    "/datasets/{dataset_slug}/sentence_pairs/{sentence_pair_id}/release",
    response_model=AlignmentActionInfoInResponse
)
async def release_sentence_pair_with_alignment_status(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_id: UUID = Path(...),
    alignment_status: ReleaseAlignmentStatus = Body(..., embed=True),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    sentence_pair = await SentencePairService(db, user).get_sentence_pair_from_dataset(sentence_pair_id=sentence_pair_id, dataset_slug=dataset_slug)

    async with await db.start_session() as s:
        async with s.start_transaction():
            alignment_action_info = await AlignmentService(db, user, s).mark_sentence_pair_as_aligned(sentence_pair)

            return create_aliased_response(AlignmentActionInfoInResponse(data=alignment_action_info))


@router.post(
    "/datasets/{dataset_slug}/sentence_pairs/{sentence_pair_id}/auto_align",
    response_model=SentencePairDetailInResponse,
)
async def generate_alignments_for_single_sentence_pair(
    dataset_slug: str = Path(..., min_length=1),
    sentence_pair_id: UUID = Path(...),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database),
    aligner: Aligner = Depends(get_aligner)
):
    sentence_pair = await SentencePairService(db, user).get_sentence_pair_from_dataset(sentence_pair_id=sentence_pair_id, dataset_slug=dataset_slug)

    async with await db.start_session() as s:
        async with s.start_transaction():
            auto_aligned_sentence_pair = await AlignmentService(db, user, s).auto_align_sentence_pair(aligner, sentence_pair)
            return create_aliased_response(SentencePairDetailInResponse(data=auto_aligned_sentence_pair))


@router.post(
    "/datasets/{dataset_slug}/auto_align",
    response_model=DatasetDetailInResponse,
)
async def generate_alignments_for_dataset(
    dataset_slug: str = Path(..., min_length=1),
    user: User = Depends(get_current_user()),
    db: AsyncIOMotorClient = Depends(get_database),
    aligner: Aligner = Depends(get_aligner)
):
    dataset = await DatasetService(db, user).get_dataset(dataset_slug)

    # async with await db.start_session() as s:
    #     async with s.start_transaction():
    #         auto_aligned_sentence_pair = await AlignmentService(db, user, s).auto_align_sentence_pair(aligner, sentence_pair)
    #         return create_aliased_response(SentencePairDetailInResponse(data=auto_aligned_sentence_pair))
    #
    return create_aliased_response(DatasetDetailInResponse(data=dataset))

@router.put(
    "/datasets/{dataset_slug}/sentence_pairs/{sentence_pair_id}/alignments",
    response_model=SentencePairDetailInResponse,
)
async def update_alignments_of_sentence_pair(
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
