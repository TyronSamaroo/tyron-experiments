from fastapi import APIRouter
from sqlmodel import Session, select
from services.db import engine
from models.workout import Workout, WorkoutCreate

router = APIRouter()


@router.post("/workouts")
def create_workout(payload: WorkoutCreate):
    workout = Workout(**payload.model_dump())

    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)

    return workout



@router.get("/workouts")
def get_workouts():
    with Session(engine) as session:
        result = session.exec(select(Workout)).all()
        return result
