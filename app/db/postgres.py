"""
SQLAlchemy database transaction engine and async engine pools.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

async def init_db() -> None:
    """Ensures database schemas tables exist."""
    async with engine.begin() as conn:
        # For production use proper migrations tracking (Alembic)
        await conn.run_sync(Base.metadata.create_all)
