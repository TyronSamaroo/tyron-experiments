from fastapi import FastAPI

from routes.moods import router as moods_router
from services.db import init_db

app = FastAPI(title="Mood Journal API")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Mood Journal API running"}


app.include_router(moods_router)
