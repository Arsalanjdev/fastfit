from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.api.crud.workout_plans import create_workout_plan_db, get_workout_plan_by_id
from src.api.dependencies.db import get_db
from src.api.schemas.v1.workout_plans import WorkoutPlansCreate, WorkoutPlansRead

router = APIRouter()

# @router.post("/create/", response_model=WorkoutPlansRead):


@router.get(
    "/{workout_plan}/", response_model=WorkoutPlansRead, status_code=status.HTTP_200_OK
)
async def get_workout_plan(workout_plan: UUID, db: Session = Depends(get_db)):
    workout_plan = get_workout_plan_by_id(db, workout_plan)
    if workout_plan is None:
        raise HTTPException(status_code=404, detail="Workout Plan not found")
    return workout_plan


@router.post(
    "/create/", response_model=WorkoutPlansRead, status_code=status.HTTP_201_CREATED
)
async def create_workout_plan(
    workout_plan: WorkoutPlansCreate,
    db: Session = Depends(get_db),
):
    workout_plan = create_workout_plan_db(db, **workout_plan.model_dump())
    return workout_plan
