import logging.config
from fastapi import FastAPI

from .api.api_v1.api import router as api_router
from .core.config import API_V1_STR
from .database.utils import close_mongo_connection, connect_to_mongo


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router, prefix=API_V1_STR)
