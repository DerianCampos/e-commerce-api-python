from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.user.infrastructure.repository.user_repository_impl import UserRepositoryImpl
from src.app.features.band.infrastructure.repository.band_repository_impl import BandRepositoryImpl

from src.app.composition.infrastructure import get_database_session

async def get_user_repository(
        session: AsyncSession = Depends(get_database_session)
) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)

async def get_band_repository(
        session: AsyncSession = Depends(get_database_session)
) -> BandRepositoryImpl:
    return BandRepositoryImpl(session)
