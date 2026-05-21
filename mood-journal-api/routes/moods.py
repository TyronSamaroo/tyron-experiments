from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
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
def list_moods(
    start: Optional[date] = Query(default=None),
    end: Optional[date] = Query(default=None),
):
    statement = select(MoodEntry)
    if start is not None:
        statement = statement.where(MoodEntry.entry_date >= start)
    if end is not None:
        statement = statement.where(MoodEntry.entry_date <= end)
    statement = statement.order_by(MoodEntry.entry_date.desc())

    with Session(engine) as session:
        return session.exec(statement).all()


@router.get("/{entry_id}")
def get_mood(entry_id: int):
    with Session(engine) as session:
        entry = session.get(MoodEntry, entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        return entry


@router.delete("/{entry_id}")
def delete_mood(entry_id: int):
    with Session(engine) as session:
        entry = session.get(MoodEntry, entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        session.delete(entry)
        session.commit()
        return {"deleted": entry_id}
