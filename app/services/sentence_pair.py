from typing import Optional
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from uuid import UUID
from fastapi_pagination.ext.motor import paginate
from fastapi_pagination.bases import AbstractPage

from .base import AppService, AppCRUD
from .dataset import DatasetService
from ..core.config import db_name, sentence_pairs_collection_name
from ..models.sentence_pair import SentencePair, SentencePairInCreate, SentencePairInDB
from ..models.dataset import Dataset

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


class SentencePairCRUD(AppCRUD):
    async def new_sentence_pair_for_dataset(self, sentence_pair_params: SentencePairInCreate, dataset: Dataset) -> SentencePairInDB:
        src_sent = sentence_pair_params.src_sent.strip()
        tgt_sent = sentence_pair_params.tgt_sent.strip()
        src_tokenize = src_sent.split()
        tgt_tokenize = tgt_sent.split()
        sentence_pair_doc = SentencePairInDB(
            dataset_slug=dataset.slug,
            src_tokenize=src_tokenize, tgt_tokenize=tgt_tokenize,
            src_sent=src_sent, tgt_sent=tgt_sent
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
