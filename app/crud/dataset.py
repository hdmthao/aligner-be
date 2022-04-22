from slugify import slugify
from typing import Optional, List
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from ..database.mongo import AsyncIOMotorClient
from ..core.config import db_name, datasets_collection_name
from .user import get_user_for_account
from ..models.dataset import DatasetInDB, DatasetInCreate, DatasetFilterParams
from ..models.user import User


async def get_sentence_pairs_count_for_dataset(conn: AsyncIOMotorClient, slug: str) -> int:
    return 0

async def get_dataset_by_slug(conn: AsyncIOMotorClient, slug: str, user: Optional[User] = None) -> Optional[DatasetInDB]:
    row = await conn[db_name][datasets_collection_name].find_one({"slug": slug})
    if not row:
        return None

    if user and row["author_id"] != user.username:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"Dataset with slug '{slug}' can not access by user '{user.username}'"
        )

    row["author"] = await get_user_for_account(conn, row["author_id"])
    row["sentence_pairs_count"] = await get_sentence_pairs_count_for_dataset(conn, slug)
    return DatasetInDB(**row)


async def create_dataset_by_slug(conn: AsyncIOMotorClient, dataset: DatasetInCreate, username: str) -> DatasetInDB:
    slug = slugify(dataset.code)
    dataset_doc = dataset.dict()
    dataset_doc["slug"] = slug
    dataset_doc["author_id"] = username

    await conn[db_name][datasets_collection_name].insert_one(dataset_doc)

    author = await get_user_for_account(conn, username)

    return DatasetInDB(**dataset_doc, author=author, sentence_pairs_count=0)


async def get_datasets_with_filters(conn: AsyncIOMotorClient, user: User, filters: DatasetFilterParams) -> List[DatasetInDB]:
    datasets: List[DatasetInDB] = []
    base_query = {}

    base_query["author_id"] = user.username

    if filters.code:
        base_query["code"] = filters.code

    if filters.source_lang:
        base_query["source_lang"] = filters.source_lang

    if filters.target_lang:
        base_query["target_lang"] = filters.target_lang

    rows = conn[db_name][datasets_collection_name].find(base_query, limit=filters.limit, skip=filters.offset)

    async for row in rows:
        slug = row["slug"]
        row["author"] = await get_user_for_account(conn, user.username)
        row["sentence_pairs_count"] = await get_sentence_pairs_count_for_dataset(conn, slug)
        datasets.append(DatasetInDB(**row))

    return datasets
