from uuid import UUID

from src.app.features.order_item.domain.exceptions.order_item_exception import OrderItemDoesNotExistException
from src.app.features.order_item.domain.repositories.order_item_repository import OrderItemRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class DeleteOrderItemUseCase:
    def __init__(self, order_item_repository: OrderItemRepository):
        self.order_item_repository = order_item_repository

    async def execute(self, order_item_id: str) -> bool:

        try:
            order_item_uuid = UUID(order_item_id)
            order_item_entity_id = EntityId(order_item_uuid)

            order_item_exists = await self.order_item_repository.exists(order_item_uuid)

            if not order_item_exists:
                log.warning(f"Cannot delete order item. Order item not found with ID: {order_item_id}")
                raise OrderItemDoesNotExistException(order_item_entity_id)

            deleted = await self.order_item_repository.delete(order_item_uuid)

            if deleted:
                log.info(f"Order item with ID {order_item_id} successfully deleted.")

            return deleted

        except ValueError as e:
            log.error(f"Invalid UUID format for order item ID {order_item_id}: {e}")
            raise ValueError(f"Invalid order item ID format: {order_item_id}")
        except OrderItemDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during delete order item for {order_item_id}: {str(e)}")
            raise
