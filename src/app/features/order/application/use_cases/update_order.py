from decimal import Decimal
from typing import Optional
from uuid import UUID

from src.app.features.order.application.dtos.order_dto import OrderResponse, OrderUpdateRequest
from src.app.features.order.application.mappers.order_mapper import to_order_response
from src.app.features.order.domain.exceptions.order_exception import OrderDoesNotExistException
from src.app.features.order.domain.repositories.order_repository import OrderRepository
from src.app.features.order.domain.value_objects.order_status import OrderStatus
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class UpdateOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_id: str, order_update: OrderUpdateRequest) -> OrderResponse:

        try:
            order_uuid = UUID(order_id)
            order_entity_id = EntityId(order_uuid)

            existing_order = await self.order_repository.find_by_id(order_uuid)

            if not existing_order:
                log.warning(f"Cannot update order. Order not found with ID: {order_id}")
                raise OrderDoesNotExistException(order_entity_id)

            user_id: Optional[EntityId] = None
            if order_update.user_id is not None:
                user_id = EntityId.from_string(order_update.user_id)

            existing_order.update(
                user_id=user_id,
                status=OrderStatus.from_str(order_update.status) if order_update.status is not None else None,
                total_amount=Decimal(str(order_update.total_amount)) if order_update.total_amount is not None else None,
                currency=order_update.currency,
                shipping_address=order_update.shipping_address,
                billing_address=order_update.billing_address,
            )

            updated_order = await self.order_repository.update(existing_order)

            log.info(f"Order with ID {order_id} successfully updated.")

            return to_order_response(updated_order)

        except ValueError as e:
            log.error(f"Invalid UUID format for order ID {order_id}: {e}")
            raise ValueError(f"Invalid order ID format: {order_id}")
        except OrderDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during update order for {order_id}: {str(e)}")
            raise
