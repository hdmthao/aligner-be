from slugify import slugify
from typing import List, Optional
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY
from uuid import UUID

from .base import AppService, AppCRUD
from ..core.config import db_name, datasets_collection_name
from ..crud.user import get_user_for_account
from ..models.dataset import Dataset, DatasetFilterParams, DatasetInCreate, DatasetInDB

class DatasetService(AppService):
    async def new_dataset(self, dataset_params: DatasetInCreate) -> Dataset:
        if not self.current_user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=f"Unauthorized to create new dataset"
            )

        existed_dataset = await DatasetCRUD(self.db, self.current_user).get_dataset(slugify(dataset_params.code))
        if existed_dataset:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Dataset already exists slug='{existed_dataset.slug}'",
            )

        db_dataset = await DatasetCRUD(self.db, self.current_user).new_dataset(dataset_params, author_id=self.current_user.id)
        author = await get_user_for_account(self.db, db_dataset.author_id)
        return Dataset(**db_dataset.dict(), author=author, sentence_pairs_count=0)


    async def get_dataset(self, slug: str) -> Dataset:
        db_dataset = await DatasetCRUD(self.db, self.current_user).get_dataset(slug)
        if not db_dataset:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Dataset with slug '{slug}' not found"
            )

        if self.current_user and db_dataset.author_id != self.current_user.id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"Dataset with slug '{slug}' can not access by user '{self.current_user.username}'"
            )

        author = await get_user_for_account(self.db, db_dataset.author_id)
        sentence_pairs_count = await DatasetCRUD(self.db, self.current_user).get_sentence_pairs_count_for_dataset(db_dataset.slug)

        return Dataset(**db_dataset.dict(), author=author, sentence_pairs_count=sentence_pairs_count)

    async def get_datasets_of_current_user_with_filters(self, filters: DatasetFilterParams) -> List[Dataset]:
        if not self.current_user:
            return []

        db_datasets = await DatasetCRUD(self.db, self.current_user).get_datasets_with_filters(filters)

        current_user_datasets: List[Dataset] = []

        for db_dataset in db_datasets:
            if db_dataset.author_id != self.current_user.id:
                continue

            author = await get_user_for_account(self.db, db_dataset.author_id)
            sentence_pairs_count = await DatasetCRUD(self.db, self.current_user).get_sentence_pairs_count_for_dataset(db_dataset.slug)
            dataset = Dataset(**db_dataset.dict(), author=author, sentence_pairs_count=sentence_pairs_count)

            current_user_datasets.append(dataset)

        return current_user_datasets

class DatasetCRUD(AppCRUD):
    async def new_dataset(self, dataset_params: DatasetInCreate, author_id: UUID) -> DatasetInDB:
        slug = slugify(dataset_params.code)
        dataset_doc = DatasetInDB(**dataset_params.dict(), slug=slug, author_id=author_id)

        await self.db[db_name][datasets_collection_name].insert_one(dataset_doc.dict())

        return dataset_doc

    async def get_dataset(self, slug: str) -> Optional[DatasetInDB]:
        row = await self.db[db_name][datasets_collection_name].find_one({"slug": slug})
        if not row:
            return None

        return DatasetInDB(**row)

    async def get_datasets_with_filters(self, filters: DatasetFilterParams) -> List[DatasetInDB]:
        datasets: List[DatasetInDB] = []
        base_query = {}

        if filters.code:
            base_query["code"] = filters.code

        if filters.src_lang:
            base_query["src_lang"] = filters.src_lang

        if filters.tgt_lang:
            base_query["tgt_lang"] = filters.tgt_lang

        rows = self.db[db_name][datasets_collection_name].find(base_query, limit=filters.limit, skip=filters.offset)

        async for row in rows:
            datasets.append(DatasetInDB(**row))

        return datasets

    async def get_sentence_pairs_count_for_dataset(self, dataset_slug: str) -> int:
        return len(dataset_slug)
