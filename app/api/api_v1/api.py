from fastapi import APIRouter

from .endpoints.authentication import router as auth_router
from .endpoints.dataset import router as dataset_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(dataset_router)
