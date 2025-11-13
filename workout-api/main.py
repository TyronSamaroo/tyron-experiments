from fastapi import FastAPI 
from routes.workouts import router as workout_router

app = FastAPI()

#Simple Health Check
@app.get("/")
def root():
    return {"message": "Workout API Running"}

# Reg workout route
app.include_router(workout_router)