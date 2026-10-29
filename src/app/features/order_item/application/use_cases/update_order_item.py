from decimal import Decimal
from uuid import UUID

from src.app.features.order_item.application.dtos.order_item_dto import OrderItemResponse, OrderItemUpdateRequest
from src.app.features.order_item.application.mappers.order_item_mapper import to_order_item_response
from src.app.features.order_item.domain.exceptions.order_item_exception import OrderItemDoesNotExistException
from src.app.features.order_item.domain.repositories.order_item_repository import OrderItemRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class UpdateOrderItemUseCase:
    def __init__(self, order_item_repository: OrderItemRepository):
        self.order_item_repository = order_item_repository

    async def execute(self, order_item_id: str, order_item_update: OrderItemUpdateRequest) -> OrderItemResponse:

        try:
            order_item_uuid = UUID(order_item_id)
            order_item_entity_id = EntityId(order_item_uuid)

            existing_order_item = await self.order_item_repository.find_by_id(order_item_uuid)

            if not existing_order_item:
                log.warning(f"Cannot update order item. Order item not found with ID: {order_item_id}")
                raise OrderItemDoesNotExistException(order_item_entity_id)

            existing_order_item.update(
                product_name=order_item_update.product_name,
                band_name=order_item_update.band_name,
                size=order_item_update.size,
                color=order_item_update.color,
                sku=order_item_update.sku,
                unit_price=Decimal(str(order_item_update.unit_price)) if order_item_update.unit_price is not None else None,
                quantity=order_item_update.quantity,
            )

            updated_order_item = await self.order_item_repository.update(existing_order_item)

            log.info(f"Order item with ID {order_item_id} successfully updated.")

            return to_order_item_response(updated_order_item)

        except ValueError as e:
            log.error(f"Invalid UUID format for order item ID {order_item_id}: {e}")
            raise ValueError(f"Invalid order item ID format: {order_item_id}")
        except OrderItemDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during update order item for {order_item_id}: {str(e)}")
            raise
