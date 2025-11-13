from pydantic import BaseModel, Field
from typing import Optional
from datetime import date 


class WorkoutCreate(BaseModel): 
    exercise: str = Field(..., examples=["Bench Press"])
    sets: int = Field(..., examples=[4])
    reps: int = Field(..., examples=[10])
    weight: int = Field(..., examples=[135.0])
    date: Optional[date] = None
class Workout(WorkoutCreate):
    id: str