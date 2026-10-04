from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Author, Base

engine = create_engine(
    "sqlite:///interview.db",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(Author).count() == 0:
            db.add(Author(name="Ada Lovelace"))
            db.add(Author(name="Grace Hopper"))
            db.commit()
    finally:
        db.close()
