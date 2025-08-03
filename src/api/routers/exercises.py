from fastapi import APIRouter

router = APIRouter()


# @router.get("/all/")
# async def get_all_exercises(
#     limit: Annotated[int | None, Query(min_length=1, max_length=100)] = None,
#     offset: Annotated[int | None, Query(min_length=0)] = 0,
# ):
#     query = select(Exercise).offset(offset)
#     if limit is not None:
#         query = query.limit(limit)
#     result = await db.execute(query)
#     exercises = result.scalars().all()
#     return exercises
