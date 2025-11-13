# Workout Logging API

A simple REST API for tracking workouts, built with FastAPI. This project allows you to log exercises with sets, reps, weight, and optional dates.

## 🎯 Project Goals

I'm building this to:
- Gain hands-on experience with FastAPI
- Strengthen my backend development fundamentals
- Create a focused backend service with well-defined core features
- Build a React frontend later to interact with this API

## ✨ Core Features (MVP)

- ✅ Create workout log
- ✅ Fetch all workout logs
- 🔄 Fetch single workout log (planned)
- 🔄 Delete workout log (planned)
- 🔄 Update workout log (planned)

## 🛠️ Tech Stack

- **Backend**: Python 3.13+ with FastAPI
- **Database**: SQLite (for now)
- **Frontend**: React (planned)
- **ORM**: SQLModel

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd workout-api
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

4. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📚 API Endpoints

### Health Check
- **GET** `/` - Returns API status

### Workouts
- **POST** `/workouts` - Create a new workout log
- **GET** `/workouts` - Get all workout logs

### Example Request

**Create a workout:**
```bash
curl -X POST "http://127.0.0.1:8000/workouts" \
  -H "Content-Type: application/json" \
  -d '{
    "exercise": "Bench Press",
    "sets": 4,
    "reps": 10,
    "weight": 135,
    "date": "2025-01-15"
  }'
```

**Get all workouts:**
```bash
curl "http://127.0.0.1:8000/workouts"
```

## 📋 Data Model

### WorkoutCreate
- `exercise` (str, required): Name of the exercise
- `sets` (int, required): Number of sets
- `reps` (int, required): Number of repetitions per set
- `weight` (int, required): Weight used (in lbs)
- `date` (date, optional): Date of the workout (defaults to None)

### Workout
Extends `WorkoutCreate` with:
- `id` (str): Unique identifier (UUID)

## 📁 Project Structure

```
workout-api/
├── main.py              # FastAPI application entry point
├── models/
│   └── workout.py       # Pydantic models for workouts
├── routes/
│   └── workouts.py      # Workout API routes
├── services/
│   └── db.py           # Database service (planned)
├── pyproject.toml      # Project dependencies
└── README.md           # This file
```

## 🔗 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🚀 Future Enhancements

- [ ] SQLite database integration
- [ ] React frontend application
- [ ] User authentication
- [ ] Workout analytics and statistics
- [ ] Export workout data
