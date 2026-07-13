from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.user.infrastructure.repository.user_repository_impl import UserRepositoryImpl

from src.app.composition.infrastructure import get_database_session

async def get_user_repository(
        session: AsyncSession = Depends(get_database_session)
) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)
