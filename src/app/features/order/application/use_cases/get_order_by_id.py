from uuid import UUID

from src.app.features.order.application.dtos.order_dto import OrderResponse
from src.app.features.order.application.mappers.order_mapper import to_order_response
from src.app.features.order.domain.exceptions.order_exception import OrderDoesNotExistException
from src.app.features.order.domain.repositories.order_repository import OrderRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetOrderByIdUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_id: str) -> OrderResponse:
        try:
            order_uuid = UUID(order_id)
            order_obj_id = EntityId(order_uuid)

            existing_order = await self.order_repository.find_by_id(order_uuid)

            if not existing_order:
                log.warning(f"Order not found with ID: {order_id}")
                raise OrderDoesNotExistException(order_obj_id)

            return to_order_response(existing_order)

        except ValueError as e:
            log.error(f"Invalid UUID format for order ID {order_id}: {e}")
            raise ValueError(f"Invalid order ID format: {order_id}")
        except OrderDoesNotExistException:
            log.error(f"Order does not exist with ID: {order_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get order by ID for {order_id}: {str(e)}")
            raise
