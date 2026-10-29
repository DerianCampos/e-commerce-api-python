from uuid import UUID

from src.app.features.order_item.application.dtos.order_item_dto import OrderItemResponse
from src.app.features.order_item.application.mappers.order_item_mapper import to_order_item_response
from src.app.features.order_item.domain.exceptions.order_item_exception import OrderItemDoesNotExistException
from src.app.features.order_item.domain.repositories.order_item_repository import OrderItemRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetOrderItemByIdUseCase:
    def __init__(self, order_item_repository: OrderItemRepository):
        self.order_item_repository = order_item_repository

    async def execute(self, order_item_id: str) -> OrderItemResponse:
        try:
            order_item_uuid = UUID(order_item_id)
            order_item_obj_id = EntityId(order_item_uuid)

            existing_order_item = await self.order_item_repository.find_by_id(order_item_uuid)

            if not existing_order_item:
                log.warning(f"Order item not found with ID: {order_item_id}")
                raise OrderItemDoesNotExistException(order_item_obj_id)

            return to_order_item_response(existing_order_item)

        except ValueError as e:
            log.error(f"Invalid UUID format for order item ID {order_item_id}: {e}")
            raise ValueError(f"Invalid order item ID format: {order_item_id}")
        except OrderItemDoesNotExistException:
            log.error(f"Order item does not exist with ID: {order_item_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get order item by ID for {order_item_id}: {str(e)}")
            raise
