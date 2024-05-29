from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from server.config.settings import settings
from typing import Iterator

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
