# 02_models_validation.py
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Models & Validation", version="1.0")

# 1) Define request model
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)

# 2) Define response model (include an id)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

_fake_db = []
_next_id = 1

@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate):  # pyright: ignore[reportUnusedParameter]
    global _next_id

        # Create a dict with id + payload
    new_user = {
        "id": _next_id,
        "name": payload.name,
        "email": payload.email,
        "age": payload.age,
    }

    # Simulate saving in a "db"
    _fake_db.append(new_user)

    # Increment counter
    _next_id += 1

    return new_user


@app.get("/users", response_model=list[UserOut])
async def list_users():
    return _fake_db