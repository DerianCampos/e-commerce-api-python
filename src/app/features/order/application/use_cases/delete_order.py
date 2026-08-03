from uuid import UUID

from src.app.features.order.domain.exceptions.order_exception import OrderDoesNotExistException
from src.app.features.order.domain.repositories.order_repository import OrderRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class DeleteOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_id: str) -> bool:

        try:
            order_uuid = UUID(order_id)
            order_entity_id = EntityId(order_uuid)

            order_exists = await self.order_repository.exists(order_uuid)

            if not order_exists:
                log.warning(f"Cannot delete order. Order not found with ID: {order_id}")
                raise OrderDoesNotExistException(order_entity_id)

            deleted = await self.order_repository.delete(order_uuid)

            if deleted:
                log.info(f"Order with ID {order_id} successfully deleted.")

            return deleted

        except ValueError as e:
            log.error(f"Invalid UUID format for order ID {order_id}: {e}")
            raise ValueError(f"Invalid order ID format: {order_id}")
        except OrderDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during delete order for {order_id}: {str(e)}")
            raise
