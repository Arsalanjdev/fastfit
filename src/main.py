import logging
import logging.config
import os

from fastapi import FastAPI

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("fastfitapi")

app = FastAPI()


@app.get("/")
async def hello():
    return "hello"
