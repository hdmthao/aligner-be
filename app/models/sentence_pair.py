from typing import List
from pydantic import Field
from uuid import UUID, uuid4
from enum import Enum

from .rwmodel import RWModel
from .dataset import Dataset


class AlignmentStatus(str, Enum):
    unaligned = 'unaligned'
    aligning = 'aligning'
    partially_aligned = 'partially_aligned'
    aligned = 'aligned'


class AlignmentPair(RWModel):
    src: int
    tgt: int


class SentencePairFilterParams(RWModel):
    limit: int = 20
    offset: int = 0


class SentencePairBase(RWModel):
    src_sent: str
    tgt_sent: str
    src_tokenize: List[str]
    tgt_tokenize: List[str]
    status: AlignmentStatus = AlignmentStatus.unaligned
    alignments: List[AlignmentPair] = []


class SentencePair(SentencePairBase):
    id: UUID
    dataset: Dataset


class SentencePairInDB(SentencePairBase):
    id: UUID = Field(default_factory=uuid4)
    dataset_slug: str


class SentencePairInCreate(RWModel):
    src_sent: str
    tgt_sent: str

    def to_base(self) -> SentencePairBase:
        src_sent = self.src_sent.strip()
        tgt_sent = self.tgt_sent.strip()
        src_tokenize = src_sent.split()
        tgt_tokenize = tgt_sent.split()
        return SentencePairBase(
            src_sent=src_sent,
            tgt_sent=tgt_sent,
            src_tokenize=src_tokenize,
            tgt_tokenize=tgt_tokenize)

class SentencePairDetailInResponse(RWModel):
    data: SentencePair


class SentencePairItemInResponse(SentencePairInDB):
    pass


