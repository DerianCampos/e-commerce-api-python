from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.shared.persistence.engine_factory import get_engine

async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    engine = get_engine()
    async with engine.get_session() as session:
        yield session