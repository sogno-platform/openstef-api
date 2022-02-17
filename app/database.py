from contextlib import contextmanager

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.settings import Settings

sqlite_filepath = 'task_repository.db'
engine = create_engine(f"sqlite:///{sqlite_filepath}")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def db_model_as_dict(obj):
    return {
        c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs
    }


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
