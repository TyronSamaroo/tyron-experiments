from fastapi import FastAPI

app = FastAPI(title="Mood Journal API")


@app.get("/")
def root():
    return {"message": "Mood Journal API running"}
