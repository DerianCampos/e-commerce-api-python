from src.app.features.order.application.dtos.order_dto import OrderCreateRequest, OrderResponse
from src.app.features.order.application.mappers.order_mapper import to_order_entity, to_order_response
from src.app.features.order.domain.repositories.order_repository import OrderRepository
from src.app.shared.utils.log_util import log


class CreateOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, payload: OrderCreateRequest) -> OrderResponse:
        try:
            order_entity = to_order_entity(payload)

            created_order = await self.order_repository.save(order_entity)
            log.info(f"Order created with number: {created_order.order_number}")

            return to_order_response(created_order)

        except Exception as e:
            log.error(f"Unexpected error while saving order: {str(e)}")
            raise
