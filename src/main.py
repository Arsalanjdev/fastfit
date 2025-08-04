import logging.config
import os

from fastapi import FastAPI

from src.api.models.base import Base
from src.api.routers import authentication, exercises, users, workout_plans

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("fastfitapi")

fastfitapi = FastAPI()
fastfitapi.include_router(authentication.router, tags=["authentication"])
fastfitapi.include_router(
    users.router, prefix="/v1", tags=["v1", "user", "authentication"]
)
fastfitapi.include_router(
    exercises.router, prefix="/v1/exercises", tags=["v1", "exercise"]
)
fastfitapi.include_router(
    workout_plans.router, prefix="/v1/workout-plans", tags=["v1", "workout-plan"]
)

# Skip DB setup in tests
if os.getenv("ENV") != "test":
    from src.api.dependencies.db import get_engine

    engine = get_engine()
    Base.metadata.create_all(bind=engine)


@fastfitapi.get("/")
async def hello():
    return "hello"
