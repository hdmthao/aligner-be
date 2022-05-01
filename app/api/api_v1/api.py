from fastapi import APIRouter

from .endpoints.authentication import router as auth_router
from .endpoints.dataset import router as dataset_router
from .endpoints.sentence_pair import router as sentence_pair_router
from .endpoints.alignment import router as aligning_pair_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(dataset_router)
router.include_router(sentence_pair_router)
router.include_router(aligning_pair_router)
