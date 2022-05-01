import logging.config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .api.api_v1.api import router as api_router
from .core.config import API_V1_STR, ALLOWED_HOSTS
from .core.aligner import load_aligner
from .database.utils import close_mongo_connection, connect_to_mongo


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI(title="Aligner API")

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    await load_aligner()
    

app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router, prefix=API_V1_STR)

add_pagination(app)
