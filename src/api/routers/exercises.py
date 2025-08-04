from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from fastapi.openapi.models import Response
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.api.crud.exercises import (
    create_exercise_db,
    get_all_exercises_db,
    get_exercise_by_id,
    update_exercise_db,
)
from src.api.dependencies.db import get_db
from src.api.schemas.v1.exercises import ExerciseCreate, ExerciseRead, ExerciseUpdate

router = APIRouter()


@router.post(
    "/create/", response_model=ExerciseRead, status_code=status.HTTP_201_CREATED
)
async def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    exercise_created = create_exercise_db(db, **exercise.model_dump())
    return exercise_created


@router.get("/all/", response_model=list[ExerciseRead], status_code=status.HTTP_200_OK)
async def get_all_exercises(
    db: Session = Depends(get_db),
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return get_all_exercises_db(db, limit=limit, offset=offset)


@router.get(
    "/{exercise_id}/",
    response_model=ExerciseRead,
    status_code=status.HTTP_200_OK,
)
async def get_exercise(
    exercise_id: UUID,
    db: Session = Depends(get_db),
):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.put("/{exercise_id}/", response_model=ExerciseRead)
async def update_exercise(
    exercise_id: UUID,
    exercise: ExerciseUpdate,
    db: Session = Depends(get_db),
):
    exercise_db = get_exercise_by_id(db, exercise_id)
    if not exercise_db:
        raise HTTPException(status_code=404, detail="Exercise not found")
    exercise_updated = update_exercise_db(db, exercise_db, **exercise.model_dump())
    return exercise_updated


@router.delete("/{exercise_id}/", status_code=204)
async def delete_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    delete_exercise(db, exercise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
