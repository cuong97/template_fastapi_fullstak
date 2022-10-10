import sys

from app.config.settings import yml_setting
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from env_settings import env_settings


if "pytest" in sys.modules:
    engine = create_engine(env_settings.database_test_url)
else:
    engine = create_engine(env_settings.database_url)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DBBaseCustom = declarative_base()

async_engine = create_async_engine(env_settings.alembic_db_url)
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_db():
    """
    Function to generate db session
    :return: Session
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


ActiveSession = Depends(get_db)
