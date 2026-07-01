#!/usr/bin/env python3
"""
Macro Tracker Web Backend
FastAPI backend for the macro tracker web application
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./macro_tracker.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    goal = Column(String)  # lose, maintain, gain
    daily_calories = Column(Integer)
    daily_protein = Column(Float)
    daily_carbs = Column(Float)
    daily_fat = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    weight_entries = relationship("WeightEntry", back_populates="user")
    food_entries = relationship("FoodEntry", back_populates="user")

class WeightEntry(Base):
    __tablename__ = "weight_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weight = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="weight_entries")

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    quantity = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="food_entries")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    goal: str
    daily_calories: int
    daily_protein: float
    daily_carbs: float
    daily_fat: float

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    height: float
    weight: float
    goal: str
    daily_calories: int
    daily_protein: float
    daily_carbs: float
    daily_fat: float
    created_at: datetime

class WeightEntryCreate(BaseModel):
    weight: float

class WeightEntryResponse(BaseModel):
    id: int
    weight: float
    date: datetime

class FoodEntryCreate(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    quantity: str

class FoodEntryResponse(BaseModel):
    id: int
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    quantity: str
    date: datetime

class DailySummary(BaseModel):
    date: str
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    remaining_calories: float
    remaining_protein: float
    remaining_carbs: float
    remaining_fat: float
    foods: List[FoodEntryResponse]

# FastAPI app
app = FastAPI(title="Macro Tracker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# For simplicity, we'll use a single user (user_id = 1)
# In a real app, you'd implement proper authentication
USER_ID = 1

@app.get("/")
async def root():
    return {"message": "Macro Tracker API"}

@app.get("/api/user", response_model=UserResponse)
async def get_user(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/user", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.id == USER_ID).first()
    if existing_user:
        # Update existing user
        for field, value in user_data.dict().items():
            setattr(existing_user, field, value)
        db.commit()
        db.refresh(existing_user)
        return existing_user

    # Create new user
    db_user = User(id=USER_ID, **user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/weight", response_model=List[WeightEntryResponse])
async def get_weight_history(db: Session = Depends(get_db)):
    entries = db.query(WeightEntry).filter(WeightEntry.user_id == USER_ID).order_by(WeightEntry.date.desc()).limit(30).all()
    return entries

@app.post("/api/weight", response_model=WeightEntryResponse)
async def log_weight(weight_data: WeightEntryCreate, db: Session = Depends(get_db)):
    # Update user's current weight
    user = db.query(User).filter(User.id == USER_ID).first()
    if user:
        user.weight = weight_data.weight

    # Create weight entry
    db_entry = WeightEntry(user_id=USER_ID, **weight_data.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.get("/api/food", response_model=List[FoodEntryResponse])
async def get_food_entries(date_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(FoodEntry).filter(FoodEntry.user_id == USER_ID)

    if date_filter:
        filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
        query = query.filter(db.func.date(FoodEntry.date) == filter_date)

    entries = query.order_by(FoodEntry.date.desc()).all()
    return entries

@app.post("/api/food", response_model=FoodEntryResponse)
async def log_food(food_data: FoodEntryCreate, db: Session = Depends(get_db)):
    db_entry = FoodEntry(user_id=USER_ID, **food_data.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.get("/api/summary/{date}", response_model=DailySummary)
async def get_daily_summary(date_str: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Get user goals
    user = db.query(User).filter(User.id == USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get food entries for the date
    food_entries = db.query(FoodEntry).filter(
        FoodEntry.user_id == USER_ID,
        db.func.date(FoodEntry.date) == target_date
    ).all()

    # Calculate totals
    total_calories = sum(entry.calories for entry in food_entries)
    total_protein = sum(entry.protein for entry in food_entries)
    total_carbs = sum(entry.carbs for entry in food_entries)
    total_fat = sum(entry.fat for entry in food_entries)

    # Calculate remaining
    remaining_calories = user.daily_calories - total_calories
    remaining_protein = user.daily_protein - total_protein
    remaining_carbs = user.daily_carbs - total_carbs
    remaining_fat = user.daily_fat - total_fat

    return DailySummary(
        date=date_str,
        total_calories=total_calories,
        total_protein=total_protein,
        total_carbs=total_carbs,
        total_fat=total_fat,
        remaining_calories=remaining_calories,
        remaining_protein=remaining_protein,
        remaining_carbs=remaining_carbs,
        remaining_fat=remaining_fat,
        foods=food_entries
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
