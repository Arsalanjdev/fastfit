from typing import Annotated

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/all/")
async def get_all_exercises(
    limit: Annotated[int | None, Query(min_length=1, max_length=100)] = None,
    offset: Annotated[int | None, Query(min_length=0)] = 0,
):
    pass
