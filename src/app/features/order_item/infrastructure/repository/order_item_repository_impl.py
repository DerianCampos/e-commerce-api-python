from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.order_item.domain.entities.order_item_entity import OrderItemEntity
from src.app.features.order_item.domain.repositories.order_item_repository import OrderItemRepository
from src.app.features.order_item.infrastructure.mappers.order_item_model_mapper import OrderItemModelMapper
from src.app.features.order_item.infrastructure.models.order_item_model import OrderItemModel
from src.app.shared.domain.repositories.base_repository import ID, T
from src.app.shared.utils.log_util import log


class OrderItemRepositoryImpl(OrderItemRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_by_id(self, entity_id: ID) -> Optional[OrderItemEntity]:
        order_item_model: Optional[OrderItemModel] = await self.db_session.get(OrderItemModel, entity_id)
        return OrderItemModelMapper.to_order_item_entity(order_item_model)

    async def save(self, entity: T) -> T:
        try:
            order_item_model = OrderItemModel(
                id=entity.id.value if hasattr(entity.id, "value") else entity.id,
                order_id=entity.order_id.value if hasattr(entity.order_id, "value") else entity.order_id,
                product_variant_id=(
                    entity.product_variant_id.value if hasattr(entity.product_variant_id, "value") else entity.product_variant_id
                ),
                product_name=entity.product_name,
                band_name=entity.band_name,
                size=entity.size,
                color=entity.color,
                sku=entity.sku,
                unit_price=entity.unit_price,
                quantity=entity.quantity,
                line_total=entity.line_total,
            )

            self.db_session.add(order_item_model)
            await self.db_session.commit()
            await self.db_session.refresh(order_item_model)

            return OrderItemModelMapper.to_order_item_entity(order_item_model)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error saving order item: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error saving order item (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error saving order item: {e}")
            raise

    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        stmt = select(OrderItemModel)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [OrderItemModelMapper.to_order_item_entity(m) for m in models]

    async def find_by_order_id(self, order_id) -> List[T]:
        stmt = select(OrderItemModel).where(OrderItemModel.order_id == order_id)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [OrderItemModelMapper.to_order_item_entity(m) for m in models]

    async def exists(self, entity_id: ID) -> bool:
        order_item_model = await self.db_session.get(OrderItemModel, entity_id)
        return order_item_model is not None

    async def update(self, entity: T) -> Optional[T]:
        existing = await self.db_session.get(
            OrderItemModel, entity.id.value if hasattr(entity.id, "value") else entity.id
        )
        if existing is None:
            return None

        existing.product_name = entity.product_name
        existing.band_name = entity.band_name
        existing.size = entity.size
        existing.color = entity.color
        existing.sku = entity.sku
        existing.unit_price = entity.unit_price
        existing.quantity = entity.quantity
        existing.line_total = entity.line_total

        try:
            self.db_session.add(existing)
            await self.db_session.commit()
            await self.db_session.refresh(existing)
            return OrderItemModelMapper.to_order_item_entity(existing)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error updating order item: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error updating order item (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error updating order item: {e}")
            raise

    async def delete(self, entity_id: ID) -> bool:
        existing = await self.db_session.get(OrderItemModel, entity_id)
        if existing is None:
            return False

        try:
            await self.db_session.delete(existing)
            await self.db_session.commit()
            return True

        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error deleting order item (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error deleting order item: {e}")
            raise
