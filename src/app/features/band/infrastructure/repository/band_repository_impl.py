from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.band.domain.entities.band_entity import BandEntity
from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.features.band.infrastructure.mappers.band_model_mapper import BandModelMapper
from src.app.features.band.infrastructure.models.band_model import BandModel
from src.app.shared.domain.repositories.base_repository import ID, T
from src.app.shared.utils.log_util import log


class BandRepositoryImpl(BandRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_by_id(self, entity_id: ID) -> Optional[BandEntity]:
        band_model: Optional[BandModel] = await self.db_session.get(BandModel, entity_id)
        return BandModelMapper.to_band_entity(band_model)

    async def create(self, entity: T) -> T:
        try:
            band_model = BandModel(
                id=entity.id.value if hasattr(entity.id, "value") else entity.id,
                name=entity.name,
                country=entity.country,
                genre=entity.genre,
            )

            self.db_session.add(band_model)
            await self.db_session.commit()
            await self.db_session.refresh(band_model)

            return BandModelMapper.to_band_entity(band_model)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error saving band: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error saving band (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error saving band: {e}")
            raise

    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        stmt = select(BandModel)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [BandModelMapper.to_band_entity(m) for m in models]

    async def exists(self, entity_id: ID) -> bool:
        band_model = await self.db_session.get(BandModel, entity_id)
        return band_model is not None

    async def update(self, entity: T) -> Optional[T]:
        existing = await self.db_session.get(BandModel, entity.id.value if hasattr(entity.id, "value") else entity.id)
        if existing is None:
            return None

        existing.name = entity.name
        existing.country = entity.country
        existing.genre = entity.genre

        try:
            self.db_session.add(existing)
            await self.db_session.commit()
            await self.db_session.refresh(existing)
            return BandModelMapper.to_band_entity(existing)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error updating band: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error updating band (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error updating band: {e}")
            raise

    async def delete(self, entity_id: ID) -> bool:
        existing = await self.db_session.get(BandModel, entity_id)
        if existing is None:
            return False

        try:
            await self.db_session.delete(existing)
            await self.db_session.commit()
            return True

        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error deleting band (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error deleting band: {e}")
            raise
