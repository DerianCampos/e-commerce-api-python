from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.order.domain.entities.order_entity import OrderEntity
from src.app.features.order.domain.repositories.order_repository import OrderRepository
from src.app.features.order.infrastructure.mappers.order_model_mapper import OrderModelMapper
from src.app.features.order.infrastructure.models.order_model import OrderModel
from src.app.shared.domain.repositories.base_repository import ID, T
from src.app.shared.utils.log_util import log


class OrderRepositoryImpl(OrderRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_by_id(self, entity_id: ID) -> Optional[OrderEntity]:
        order_model: Optional[OrderModel] = await self.db_session.get(OrderModel, entity_id)
        return OrderModelMapper.to_order_entity(order_model)

    async def save(self, entity: T) -> T:
        try:
            order_model = OrderModel(
                id=entity.id.value if hasattr(entity.id, "value") else entity.id,
                user_id=entity.user_id.value if entity.user_id and hasattr(entity.user_id, "value") else entity.user_id,
                order_number=entity.order_number,
                status=str(entity.status),
                total_amount=entity.total_amount,
                currency=entity.currency,
                shipping_address=entity.shipping_address,
                billing_address=entity.billing_address,
            )

            self.db_session.add(order_model)
            await self.db_session.commit()
            await self.db_session.refresh(order_model)

            return OrderModelMapper.to_order_entity(order_model)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error saving order: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error saving order (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error saving order: {e}")
            raise

    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        stmt = select(OrderModel)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [OrderModelMapper.to_order_entity(m) for m in models]

    async def exists(self, entity_id: ID) -> bool:
        order_model = await self.db_session.get(OrderModel, entity_id)
        return order_model is not None

    async def update(self, entity: T) -> Optional[T]:
        existing = await self.db_session.get(
            OrderModel, entity.id.value if hasattr(entity.id, "value") else entity.id
        )
        if existing is None:
            return None

        existing.user_id = entity.user_id.value if entity.user_id and hasattr(entity.user_id, "value") else entity.user_id
        existing.status = str(entity.status)
        existing.total_amount = entity.total_amount
        existing.currency = entity.currency
        existing.shipping_address = entity.shipping_address
        existing.billing_address = entity.billing_address

        try:
            self.db_session.add(existing)
            await self.db_session.commit()
            await self.db_session.refresh(existing)
            return OrderModelMapper.to_order_entity(existing)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error updating order: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error updating order (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error updating order: {e}")
            raise

    async def delete(self, entity_id: ID) -> bool:
        existing = await self.db_session.get(OrderModel, entity_id)
        if existing is None:
            return False

        try:
            await self.db_session.delete(existing)
            await self.db_session.commit()
            return True

        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error deleting order (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error deleting order: {e}")
            raise
