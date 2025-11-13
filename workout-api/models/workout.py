from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Date
from datetime import date
from typing import Optional


class Workout(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exercise: str 
    sets: int
    reps: int
    weight: float
    date: Optional[str] = Field(default=None)


class WorkoutCreate(SQLModel):
    exercise: str
    sets: int
    reps: int
    weight: float
    date: Optional[str] = None