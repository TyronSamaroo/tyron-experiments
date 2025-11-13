from fastapi import FastAPI
from routes.workouts import router as workouts_router
from services.db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

#Simple Health Check
@app.get("/")
def root():
    return {"message": "Workout API Running"}

# Reg workout route
app.include_router(workouts_router)