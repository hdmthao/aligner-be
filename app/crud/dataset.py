from slugify import slugify
from typing import Optional, List

from ..database.mongo import AsyncIOMotorClient
from ..core.config import db_name, datasets_collection_name
from ..models.dataset import DatasetInDB, DatasetInCreate, DatasetFilterParams


async def get_sentence_pairs_count_for_dataset(conn: AsyncIOMotorClient, slug: str) -> int:
    return 0

async def get_dataset_by_slug(conn: AsyncIOMotorClient, slug: str) -> Optional[DatasetInDB]:
    row = await conn[db_name][datasets_collection_name].find_one({"slug": slug})
    if not row:
        return None

    return DatasetInDB(**row)


async def create_dataset_by_slug(conn: AsyncIOMotorClient, dataset: DatasetInCreate, username: str) -> DatasetInDB:
    slug = slugify(dataset.code)
    dataset_doc = dataset.dict()
    dataset_doc["slug"] = slug
    dataset_doc["author_id"] = username

    await conn[db_name][datasets_collection_name].insert_one(dataset_doc)

    return DatasetInDB(**dataset_doc, author_id=username)


async def get_datasets_with_filters(conn: AsyncIOMotorClient, filters: DatasetFilterParams) -> List[DatasetInDB]:
    datasets: List[DatasetInDB] = []
    base_query = {}

    if filters.code:
        base_query["code"] = filters.code

    if filters.source_lang:
        base_query["source_lang"] = filters.source_lang

    if filters.target_lang:
        base_query["target_lang"] = filters.target_lang

    rows = conn[db_name][datasets_collection_name].find(base_query, limit=filters.limit, skip=filters.offset)

    async for row in rows:
        datasets.append(DatasetInDB(**row))

    return datasets
