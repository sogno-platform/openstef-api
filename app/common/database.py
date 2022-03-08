from contextlib import contextmanager
import asyncio
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from redis.asyncio import from_url as redis_from_url
from app.core.settings import Settings

sqlite_filepath = "task_repository.db"
engine = create_engine(f"sqlite:///{sqlite_filepath}")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def db_model_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# REDIS

redis_meta = redis_from_url(
    url=f"redis://{Settings.redis_host}:{Settings.redis_port}",
    username=Settings.redis_username,
    password=Settings.redis_password.get_secret_value(),
    db=0,
)

redis_job = redis_from_url(
    url=f"redis://{Settings.redis_host}:{Settings.redis_port}",
    username=Settings.redis_username,
    password=Settings.redis_password.get_secret_value(),
    db=1,
)

redis_model = redis_from_url(
    url=f"redis://{Settings.redis_host}:{Settings.redis_port}",
    username=Settings.redis_username,
    password=Settings.redis_password.get_secret_value(),
    db=2,
)


async def get_unique_id():
    return await redis_meta.incr("_next_unique_id")
    
