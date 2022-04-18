import logging.config
from fastapi import FastAPI



logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
