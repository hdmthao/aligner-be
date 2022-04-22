from typing import Literal, Optional, List

from .rwmodel import RWModel
from .user import User

from pydantic import Field


class DatasetFilterParams(RWModel):
    code: str = ""
    source_lang: str = ""
    target_lang: str = ""
    limit: int = 20
    offset: int = 0


class DatasetBase(RWModel):
    code: str = Field(
        ...,
        title='A unique code of the dataset',
        min_length=1,
        max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    source_lang: Literal['EN', 'VI', 'FR']
    target_lang: Literal['EN', 'VI', 'FR']


class DatasetMetadata(DatasetBase):
    pass


class Dataset(DatasetBase):
    slug: str
    author: User
    sentence_pairs_count: int


class DatasetInDB(DatasetBase):
    slug: str
    author_id: str


class DatasetInCreate(DatasetBase):
    pass


class DatasetInResponse(RWModel):
    data: Dataset

class ManyDatasetsInResponse(RWModel):
    data: List[Dataset]
    datasets_count: int
