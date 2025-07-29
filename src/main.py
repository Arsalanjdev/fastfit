import logging.config

from fastapi import FastAPI

from src.api.models.base import Base
from src.api.routers import users
from src.db import engine

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("fastfitapi")

Base.metadata.create_all(bind=engine)


fastfitapi = FastAPI()
fastfitapi.include_router(users.router, prefix="/v1")


@fastfitapi.get("/")
async def hello():
    return "hello"
