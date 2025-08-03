from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.openapi.models import Response
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.api.crud.exercises import (
    create_exercise_db,
    get_all_exercises_db,
    get_exercise_by_id,
)
from src.api.schemas.v1.exercises import ExerciseCreate, ExerciseRead, ExerciseUpdate
from src.db import get_db

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
    return exercise


@router.put("/{exercise_id}/", response_model=ExerciseRead)
async def update_exercise(
    exercise_id: UUID,
    exercise: ExerciseUpdate,
    db: Session = Depends(get_db),
):
    exercise = update_exercise(db, exercise_id, **exercise.model_dump())
    return exercise


@router.delete("/{exercise_id}/", status_code=204)
async def delete_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    delete_exercise(db, exercise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
