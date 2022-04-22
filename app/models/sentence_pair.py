from typing import List
from uuid import UUID

from .rwmodel import RWModel
from .dataset import DatasetMetadata


class SentencePairBase(RWModel):
    src: List[str]
    tgt: List[str]


class SentencePair(SentencePairBase):
    slug: UUID
    dataset: DatasetMetadata


class SentencePairInDB(SentencePairBase):
    slug: UUID
    dataset_id: str


class SentencePairInResponse(RWModel):
    data: SentencePair


class ManySentencePairsInResponse(RWModel):
    data: List[SentencePair]
    sentence_pairs_count: int
