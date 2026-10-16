
from importlib import reload
from sys import version
from turtle import title
from fastapi import FastAPI
import uvicorn



app = FastAPI(
    title= "FastAPI Test",
    description= "Something",
    version = "1.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome All", "status": "OK"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id" : user_id, "message": f"User {user_id} found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)