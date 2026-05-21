from datetime import date

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

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


@router.get("")
def list_moods():
    with Session(engine) as session:
        return session.exec(select(MoodEntry).order_by(MoodEntry.entry_date.desc())).all()


@router.get("/{entry_id}")
def get_mood(entry_id: int):
    with Session(engine) as session:
        entry = session.get(MoodEntry, entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        return entry
