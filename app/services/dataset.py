from typing import List
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from .base import AppService
from ..crud.dataset import get_dataset_by_slug, get_datasets_with_filters
from ..crud.dataset import get_sentence_pairs_count_for_dataset
from ..crud.user import get_user_for_account
from ..models.dataset import Dataset, DatasetFilterParams

class DatasetService(AppService):
    async def get_dataset(self, slug: str) -> Dataset:
        db_dataset = await get_dataset_by_slug(self.db, slug)
        if not db_dataset:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Dataset with slug '{slug}' not found"
            )

        if self.current_user and db_dataset.author_id != self.current_user.username:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"Dataset with slug '{slug}' can not access by user '{self.current_user.username}'"
            )

        author = await get_user_for_account(self.db, db_dataset.author_id)
        sentence_pairs_count = await get_sentence_pairs_count_for_dataset(self.db, db_dataset.slug)

        return Dataset(**db_dataset.dict(), author=author, sentence_pairs_count=sentence_pairs_count)

    async def get_datasets_of_current_user_with_filters(self, filters: DatasetFilterParams) -> List[Dataset]:
        if not self.current_user:
            return []

        db_datasets = await get_datasets_with_filters(self.db, filters)

        current_user_datasets: List[Dataset] = []

        for db_dataset in db_datasets:
            if db_dataset.author_id != self.current_user.username:
                continue

            author = await get_user_for_account(self.db, db_dataset.author_id)
            sentence_pairs_count = await get_sentence_pairs_count_for_dataset(self.db, db_dataset.slug)
            dataset = Dataset(**db_dataset.dict(), author=author, sentence_pairs_count=sentence_pairs_count)

            current_user_datasets.append(dataset)

        return current_user_datasets
