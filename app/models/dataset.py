from typing import Literal, Optional
from uuid import UUID

from .rwmodel import RWModel
from .user import User

from pydantic import Field


class DatasetFilterParams(RWModel):
    code: str = ""
    src_lang: str = ""
    tgt_lang: str = ""


class DatasetBase(RWModel):
    code: str = Field(
        ...,
        title='A unique code of the dataset',
        min_length=1,
        max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    src_lang: Literal['EN', 'VI', 'FR']
    tgt_lang: Literal['EN', 'VI', 'FR']


class Dataset(DatasetBase):
    slug: str
    author: User
    sentence_pairs_count: int


class DatasetInDB(DatasetBase):
    slug: str
    author_id: UUID


class DatasetInCreate(DatasetBase):
    pass


class DatasetDetailInResponse(RWModel):
    data: Dataset


class DatasetItemInResponse(DatasetInDB):
    pass
