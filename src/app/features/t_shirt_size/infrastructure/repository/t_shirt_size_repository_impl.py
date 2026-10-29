from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.t_shirt_size.domain.entities.t_shirt_size_entity import TShirtSizeEntity
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.features.t_shirt_size.infrastructure.mappers.t_shirt_size_model_mapper import TShirtSizeModelMapper
from src.app.features.t_shirt_size.infrastructure.models.t_shirt_size_model import TShirtSizeModel
from src.app.shared.domain.repositories.base_repository import ID, T
from src.app.shared.utils.log_util import log


class TShirtSizeRepositoryImpl(TShirtSizeRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_by_id(self, entity_id: ID) -> Optional[TShirtSizeEntity]:
        size_model: Optional[TShirtSizeModel] = await self.db_session.get(TShirtSizeModel, entity_id)
        return TShirtSizeModelMapper.to_t_shirt_size_entity(size_model)

    async def save(self, entity: T) -> T:
        try:
            size_model = TShirtSizeModel(
                id=entity.id.value if hasattr(entity.id, "value") else entity.id,
                size=str(entity.size),
                chest_min_cm=entity.chest_min_cm,
                chest_max_cm=entity.chest_max_cm,
            )

            self.db_session.add(size_model)
            await self.db_session.commit()
            await self.db_session.refresh(size_model)

            return TShirtSizeModelMapper.to_t_shirt_size_entity(size_model)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error saving t-shirt size: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error saving t-shirt size (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error saving t-shirt size: {e}")
            raise

    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        stmt = select(TShirtSizeModel)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [TShirtSizeModelMapper.to_t_shirt_size_entity(m) for m in models]

    async def exists(self, entity_id: ID) -> bool:
        size_model = await self.db_session.get(TShirtSizeModel, entity_id)
        return size_model is not None

    async def update(self, entity: T) -> Optional[T]:
        existing = await self.db_session.get(
            TShirtSizeModel, entity.id.value if hasattr(entity.id, "value") else entity.id
        )
        if existing is None:
            return None

        existing.size = str(entity.size)
        existing.chest_min_cm = entity.chest_min_cm
        existing.chest_max_cm = entity.chest_max_cm

        try:
            self.db_session.add(existing)
            await self.db_session.commit()
            await self.db_session.refresh(existing)
            return TShirtSizeModelMapper.to_t_shirt_size_entity(existing)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error updating t-shirt size: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error updating t-shirt size (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error updating t-shirt size: {e}")
            raise

    async def delete(self, entity_id: ID) -> bool:
        existing = await self.db_session.get(TShirtSizeModel, entity_id)
        if existing is None:
            return False

        try:
            await self.db_session.delete(existing)
            await self.db_session.commit()
            return True

        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error deleting t-shirt size (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error deleting t-shirt size: {e}")
            raise
