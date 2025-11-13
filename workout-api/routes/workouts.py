from fastapi import APIRouter
from uuid import uuid4
from models.workout import Workout, WorkoutCreate


router = APIRouter()

#Store in memory for today
WORKOUTS = []

@router.post("/workouts", response_model=Workout)
def create_workout(payload: WorkoutCreate):
    new_workout = Workout(id=str(uuid4()), **payload.model_dump())
    WORKOUTS.append(new_workout)
    return new_workout

@router.get("/workouts")
def get_workouts():
    return WORKOUTS
