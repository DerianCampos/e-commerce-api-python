from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.product_variant.domain.entities.product_variant_entity import ProductVariantEntity
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.features.product_variant.infrastructure.mappers.product_variant_model_mapper import (
    ProductVariantModelMapper,
)
from src.app.features.product_variant.infrastructure.models.product_variant_model import ProductVariantModel
from src.app.shared.domain.repositories.base_repository import ID, T
from src.app.shared.utils.log_util import log


class ProductVariantRepositoryImpl(ProductVariantRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_by_id(self, entity_id: ID) -> Optional[ProductVariantEntity]:
        variant_model: Optional[ProductVariantModel] = await self.db_session.get(ProductVariantModel, entity_id)
        return ProductVariantModelMapper.to_product_variant_entity(variant_model)

    async def save(self, entity: T) -> T:
        try:
            variant_model = ProductVariantModel(
                id=entity.id.value if hasattr(entity.id, "value") else entity.id,
                product_id=entity.product_id.value if hasattr(entity.product_id, "value") else entity.product_id,
                size_id=entity.size_id.value if hasattr(entity.size_id, "value") else entity.size_id,
                color=entity.color,
                sku=entity.sku.value if hasattr(entity.sku, "value") else str(entity.sku),
                unit_price=entity.unit_price,
                stock_quantity=entity.stock_quantity,
            )

            self.db_session.add(variant_model)
            await self.db_session.commit()
            await self.db_session.refresh(variant_model)

            return ProductVariantModelMapper.to_product_variant_entity(variant_model)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error saving product variant: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error saving product variant (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error saving product variant: {e}")
            raise

    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        stmt = select(ProductVariantModel)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [ProductVariantModelMapper.to_product_variant_entity(m) for m in models]

    async def find_by_product_id(self, product_id) -> List[T]:
        stmt = select(ProductVariantModel).where(ProductVariantModel.product_id == product_id)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [ProductVariantModelMapper.to_product_variant_entity(m) for m in models]

    async def exists(self, entity_id: ID) -> bool:
        variant_model = await self.db_session.get(ProductVariantModel, entity_id)
        return variant_model is not None

    async def update(self, entity: T) -> Optional[T]:
        existing = await self.db_session.get(
            ProductVariantModel, entity.id.value if hasattr(entity.id, "value") else entity.id
        )
        if existing is None:
            return None

        existing.color = entity.color
        existing.sku = entity.sku.value if hasattr(entity.sku, "value") else str(entity.sku)
        existing.unit_price = entity.unit_price
        existing.stock_quantity = entity.stock_quantity

        try:
            self.db_session.add(existing)
            await self.db_session.commit()
            await self.db_session.refresh(existing)
            return ProductVariantModelMapper.to_product_variant_entity(existing)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error updating product variant: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error updating product variant (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error updating product variant: {e}")
            raise

    async def delete(self, entity_id: ID) -> bool:
        existing = await self.db_session.get(ProductVariantModel, entity_id)
        if existing is None:
            return False

        try:
            await self.db_session.delete(existing)
            await self.db_session.commit()
            return True

        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error deleting product variant (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error deleting product variant: {e}")
            raise
