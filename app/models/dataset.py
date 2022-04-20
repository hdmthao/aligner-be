from typing import Literal, Optional, List

from .rwmodel import RWModel
from .user import User

from pydantic import Field


class DatasetBase(RWModel):
    code: str = Field(
        ...,
        title='A unique code of the dataset',
        min_length=1,
        max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    source_lang: Literal['EN', 'VI', 'FR']
    target_lang: Literal['EN', 'VI', 'FR']


class Dataset(DatasetBase):
    slug: str
    sentence_pairs_count: int


class DatasetInDB(Dataset):
    author: User


class DatasetInCreate(DatasetBase):
    pass


class DatasetInResponse(RWModel):
    data: Dataset

class ManyDatasetsInResponse(RWModel):
    data: List[Dataset]
    datasets_count: int
