from typing import List
from pydantic import Field
from uuid import UUID, uuid4

from .rwmodel import RWModel
from .dataset import Dataset


class SentencePairBase(RWModel):
    src_sent: str
    tgt_sent: str
    src_tokenize: List[str]
    tgt_tokenize: List[str]


class SentencePair(SentencePairBase):
    id: UUID
    dataset: Dataset


class SentencePairInDB(SentencePairBase):
    id: UUID = Field(default_factory=uuid4)
    dataset_slug: str


class SentencePairInCreate(RWModel):
    src_sent: str
    tgt_sent: str

class SentencePairInResponse(RWModel):
    data: SentencePair


class ManySentencePairsInResponse(RWModel):
    data: List[SentencePair]
    sentence_pairs_count: int
