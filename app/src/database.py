from functools import cache

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import config

Db = AsyncSession


@cache
def get_engine() -> AsyncEngine:
    db = config.database
    return create_async_engine(
        f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}/{db.name}",
        pool_size=db.pool_size,
        max_overflow=db.pool_max_size - db.pool_size,
    )


engine = get_engine()

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
