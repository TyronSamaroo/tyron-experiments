from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///moods.db", echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)
