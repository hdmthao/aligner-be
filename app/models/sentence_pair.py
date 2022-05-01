from typing import List
from pydantic import Field
from uuid import UUID, uuid4

from .rwmodel import RWModel
from .dataset import Dataset
from .alignment import AlignmentStatus, AlignmentPair


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

    def is_free_to_acquire(self):
        return self.status in [AlignmentStatus.unaligned, AlignmentStatus.aligning, AlignmentStatus.partially_aligned]


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


