from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from fss.common.config import configs


@asynccontextmanager
async def db_session(db_url=None):
    """Creates a context with an open SQLAlchemy async session."""
    if db_url is None:
        db_url = configs.sqlalchemy_database_url
    engine = create_async_engine(db_url, echo=True)
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, autocommit=False, autoflush=True
    )
    async with async_session() as session:
        yield session
    await engine.dispose()
