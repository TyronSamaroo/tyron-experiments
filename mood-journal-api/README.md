# Mood Journal API

A lightweight FastAPI service for logging daily mood entries with notes.

## Features

- Create a mood entry with a score (1-10), optional note, and date
- List entries, optionally filtered by a date range
- Retrieve a single entry by id
- Delete an entry by id

## Tech Stack

- Python 3.13+
- FastAPI
- SQLModel (SQLite)
- uv

## Getting Started

```bash
cd mood-journal-api
uv run uvicorn main:app --reload
```

Then open http://localhost:8000/docs for the interactive Swagger UI.
