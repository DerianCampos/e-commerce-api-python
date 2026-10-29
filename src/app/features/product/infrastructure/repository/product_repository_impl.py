from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.product.domain.entities.product_entity import ProductEntity
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.features.product.infrastructure.mappers.product_model_mapper import ProductModelMapper
from src.app.features.product.infrastructure.models.product_model import ProductModel
from src.app.shared.domain.repositories.base_repository import ID, T
from src.app.shared.utils.log_util import log


class ProductRepositoryImpl(ProductRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_by_id(self, entity_id: ID) -> Optional[ProductEntity]:
        product_model: Optional[ProductModel] = await self.db_session.get(ProductModel, entity_id)

        return ProductModelMapper.to_product_entity(product_model)

    async def save(self, entity: T) -> T:
        try:
            product_model = ProductModel(
                id=entity.id.value if hasattr(entity.id, "value") else entity.id,
                name=entity.name,
                description=entity.description,
                fit=entity.fit.value,
                band_id=entity.band_id.value if entity.band_id and hasattr(entity.band_id, "value") else entity.band_id,
                is_active=bool(entity.is_active),
            )

            self.db_session.add(product_model)
            await self.db_session.commit()
            await self.db_session.refresh(product_model)

            return ProductModelMapper.to_product_entity(product_model)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error saving product: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error saving product (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error saving product: {e}")
            raise

    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        stmt = select(ProductModel)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [ProductModelMapper.to_product_entity(m) for m in models]

    async def exists(self, entity_id: ID) -> bool:
        product_model = await self.db_session.get(ProductModel, entity_id)
        return product_model is not None

    async def update(self, entity: T) -> Optional[T]:
        existing = await self.db_session.get(
            ProductModel, entity.id.value if hasattr(entity.id, "value") else entity.id
        )
        if existing is None:
            return None

        existing.name = entity.name
        existing.description = entity.description
        existing.fit = entity.fit.value
        existing.band_id = (
            entity.band_id.value if entity.band_id and hasattr(entity.band_id, "value") else entity.band_id
        )
        existing.is_active = bool(entity.is_active)

        try:
            self.db_session.add(existing)
            await self.db_session.commit()
            await self.db_session.refresh(existing)
            return ProductModelMapper.to_product_entity(existing)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error updating product: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error updating product (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error updating product: {e}")
            raise

    async def delete(self, entity_id: ID) -> bool:
        existing = await self.db_session.get(ProductModel, entity_id)
        if existing is None:
            return False

        try:
            await self.db_session.delete(existing)
            await self.db_session.commit()
            return True

        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error deleting product (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error deleting product: {e}")
            raise
