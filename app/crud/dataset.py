from slugify import slugify
from typing import Optional

from ..database.mongo import AsyncIOMotorClient
from ..core.config import db_name, datasets_collection_name
from ..models.dataset import DatasetInDB, DatasetInCreate

async def get_dataset_by_slug(conn: AsyncIOMotorClient, slug: str) -> Optional[DatasetInDB]:
    row = await conn[db_name][datasets_collection_name].find_one({"slug": slug})
    if row:
        return DatasetInDB(**row)


async def create_dataset_by_slug(conn: AsyncIOMotorClient, dataset: DatasetInCreate, username: str) -> DatasetInDB:
    slug = slugify(dataset.code)
    dataset_doc = dataset.dict()
    dataset_doc["slug"] = slug
    dataset_doc["author_id"] = username

    await conn[db_name][datasets_collection_name].insert_one(dataset_doc)

    return DatasetInDB(**dataset_doc)
