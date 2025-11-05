"""
Database connection and session management
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from config import settings
from database.models import Base
from database.personalization_models import PersonalizationBase


# Main database engine
engine = create_async_engine(
    settings.database_url,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    poolclass=StaticPool if "sqlite" in settings.database_url else None,
)

# Personalization database engine
personalization_engine = create_async_engine(
    settings.personalization_db_url,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.personalization_db_url else {},
    poolclass=StaticPool if "sqlite" in settings.personalization_db_url else None,
)

# Session factories
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

AsyncPersonalizationSessionLocal = async_sessionmaker(
    personalization_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with personalization_engine.begin() as conn:
        await conn.run_sync(PersonalizationBase.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_personalization_db() -> AsyncGenerator[AsyncSession, None]:
    """Get personalization database session"""
    async with AsyncPersonalizationSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


