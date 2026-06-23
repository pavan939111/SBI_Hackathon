"""
Dependency injection definitions including database sessions.
"""
from typing import AsyncGenerator
from app.db.postgres import AsyncSessionLocal

async def get_db_session() -> AsyncGenerator:
    """Yields active transactional database sessions."""
    async with AsyncSessionLocal() as session:
        yield session
