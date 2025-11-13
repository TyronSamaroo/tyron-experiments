from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///workouts.db", echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)