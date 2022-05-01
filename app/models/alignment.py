from enum import Enum
from typing import List

from .rwmodel import RWModel


class AlignmentStatus(str, Enum):
    unaligned = 'unaligned'
    aligning = 'aligning'
    partially_aligned = 'partially_aligned'
    aligned = 'aligned'


class AlignmentPair(RWModel):
    src_idx: int
    tgt_idx: int


class AlignmentActionInfo(RWModel):
    success: bool
    message: str


class AlignmentActionInfoInResponse(RWModel):
    data: AlignmentActionInfo


class AlignmentInUpdate(RWModel):
    alignments: List[AlignmentPair]
