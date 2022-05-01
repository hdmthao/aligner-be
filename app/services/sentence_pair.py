from fastapi import UploadFile
from typing import Optional, List
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from uuid import UUID
from fastapi_pagination.ext.motor import paginate
from fastapi_pagination.bases import AbstractPage
from pymongo.errors import BulkWriteError

from .base import AppService, AppCRUD
from .dataset import DatasetService
from ..core.config import MAXIMUM_SENTENCE_PAIRS_CAN_IMPORT
from ..core.config import db_name, sentence_pairs_collection_name
from ..models.sentence_pair import SentencePair, SentencePairInCreate, SentencePairInDB
from ..models.dataset import Dataset
from ..models.alignment import AlignmentStatus, AlignmentPair


class SentencePairService(AppService):
    async def new_sentence_pair_for_dataset(self, sentence_pair_params: SentencePairInCreate, dataset_slug: str) -> SentencePair:
        dataset = await DatasetService(self.db, self.current_user).get_dataset(dataset_slug)

        db_sentence_pair = await SentencePairCRUD(self.db, session=self.session).new_sentence_pair_for_dataset(sentence_pair_params, dataset)
        sentence_pair = SentencePair(**db_sentence_pair.dict(), dataset=dataset)

        return sentence_pair

    async def get_sentence_pair_from_dataset(self, sentence_pair_id: UUID, dataset_slug: str) -> SentencePair:
        dataset = await DatasetService(self.db, self.current_user).get_dataset(dataset_slug)

        db_sentence_pair = await SentencePairCRUD(self.db).get_sentence_pair_from_dataset(sentence_pair_id, dataset)
        if not db_sentence_pair:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Sentence pair with id '{sentence_pair_id}' not found for dataset with slug '{dataset_slug}'"
            )

        sentence_pair = SentencePair(**db_sentence_pair.dict(), dataset=dataset)

        return sentence_pair


    async def get_sentence_pairs_from_dataset_with_paging(self, dataset_slug: str) -> AbstractPage:
        dataset = await DatasetService(self.db, self.current_user).get_dataset(dataset_slug)

        db_sentence_pairs = await SentencePairCRUD(self.db, self.current_user).get_sentence_pairs_from_dataset_with_paging(dataset)

        return db_sentence_pairs


    async def import_sentence_pairs_from_file_to_dataset(self, uploaded_file: UploadFile, dataset: Dataset):
        file = uploaded_file.file
        if not file:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Something went wrong when reading file {uploaded_file.filename}"
            )

        sentence_pairs_in_create: List[SentencePairInCreate] = []
        line_count = 0
        for line in file:
            line_count += 1
            if line_count > MAXIMUM_SENTENCE_PAIRS_CAN_IMPORT:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f"Reached limit of maximum number of sentence pairs"
                )
            if not line:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f"Line cannot be empty. Line {line_count}"
                )

            raw_src_sent, raw_tgt_sent = line.decode().split("|||")
            if not raw_src_sent.strip() or not raw_tgt_sent.strip():
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f"Wrong line format. Line {line_count}"
                )

            sentence_pair_in_create = SentencePairInCreate(src_sent=raw_src_sent, tgt_sent=raw_tgt_sent)
            sentence_pairs_in_create.append(sentence_pair_in_create)

        inserted_docs = await SentencePairCRUD(self.db).bulk_insert_sentence_pairs_to_dataset(sentence_pairs_in_create, dataset)

        return { "imported_sentence_pairs_count": inserted_docs }


class SentencePairCRUD(AppCRUD):
    async def new_sentence_pair_for_dataset(self, sentence_pair_params: SentencePairInCreate, dataset: Dataset) -> SentencePairInDB:
        sentence_pair_doc = SentencePairInDB(
            dataset_slug=dataset.slug,
            **sentence_pair_params.to_base().dict()
        )

        await self.db[db_name][sentence_pairs_collection_name].insert_one(sentence_pair_doc.dict(), session=self.session)

        return sentence_pair_doc


    async def get_sentence_pair_from_dataset(self, sentence_pair_id: UUID, dataset: Dataset) -> Optional[SentencePairInDB]:
        row = await self.db[db_name][sentence_pairs_collection_name].find_one({"id": sentence_pair_id, "dataset_slug": dataset.slug })
        if not row:
            return None

        return SentencePairInDB(**row)


    async def get_sentence_pairs_from_dataset_with_paging(self, dataset: Dataset) -> AbstractPage:
        base_query = {"dataset_slug": dataset.slug}

        return await paginate(self.db[db_name][sentence_pairs_collection_name], query_filter=base_query)


    async def bulk_insert_sentence_pairs_to_dataset(self, sentence_pairs_in_create: List[SentencePairInCreate], dataset: Dataset):
        sentence_pair_docs = map(lambda sentence_pair_in_create: SentencePairInDB(dataset_slug=dataset.slug, **sentence_pair_in_create.to_base().dict()).dict(), sentence_pairs_in_create)

        try:
            await self.db[db_name][sentence_pairs_collection_name].insert_many(sentence_pair_docs, ordered=False)
            return len(sentence_pairs_in_create)
        except BulkWriteError as e:
            panic = list(filter(lambda x: x['code'] != 11000, e.details['writeErrors']))

            if len(panic) > 0:
                raise e

            return e.details['nInserted']


    async def update_status(self, sentence_pair: SentencePair, new_status: AlignmentStatus):
        update_operator = {'$set': {'status': new_status}}
        await self.db[db_name][sentence_pairs_collection_name].update_one({'id': sentence_pair.id}, update_operator, session=self.session)


    async def update_alignments(self, sentence_pair: SentencePair, new_alignments: List[AlignmentPair]):
        update_operator = {'$set': {'alignments': [alignment.dict() for alignment in new_alignments]}}
        await self.db[db_name][sentence_pairs_collection_name].update_one({'id': sentence_pair.id}, update_operator, session=self.session)
