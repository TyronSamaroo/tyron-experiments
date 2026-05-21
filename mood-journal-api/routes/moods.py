from datetime import date

from fastapi import APIRouter
from sqlmodel import Session

from models.mood import MoodEntry, MoodEntryCreate
from services.db import engine

router = APIRouter(prefix="/moods", tags=["moods"])


@router.post("")
def create_mood(payload: MoodEntryCreate):
    entry = MoodEntry(
        score=payload.score,
        note=payload.note,
        entry_date=payload.entry_date or date.today(),
    )

    with Session(engine) as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)

    return entry
