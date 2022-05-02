from fastapi.encoders import jsonable_encoder
from typing import List
from pydantic import BaseModel
from starlette.responses import JSONResponse
from ..models.alignment import AlignmentPair


def create_aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))


def process_raw_alignments(raw_alignments) -> List[AlignmentPair]:
    alignments = []
    for pair in raw_alignments.split():
        src_idx, tgt_idx = pair.split('-')
        alignments.append(AlignmentPair(src_idx=src_idx, tgt_idx=tgt_idx))
    return alignments
