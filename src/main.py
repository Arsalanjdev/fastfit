import logging

from fastapi import APIRouter

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger("fastfitapi")


app = APIRouter()


@app.get("/")
async def hello():
    return "hello"
