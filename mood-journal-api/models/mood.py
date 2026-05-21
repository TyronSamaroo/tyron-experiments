from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class MoodEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    score: int = Field(ge=1, le=10)
    note: Optional[str] = None
    entry_date: date


class MoodEntryCreate(SQLModel):
    score: int = Field(ge=1, le=10)
    note: Optional[str] = None
    entry_date: Optional[date] = None
