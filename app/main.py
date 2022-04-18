import logging.config
from fastapi import FastAPI

from .database.utils import close_mongo_connection, connect_to_mongo


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

@app.get("/")
async def root():
    return {"message": "Hello World"}
