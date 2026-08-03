from src.app.features.order_item.application.dtos.order_item_dto import OrderItemCreateRequest, OrderItemResponse
from src.app.features.order_item.application.mappers.order_item_mapper import (
    to_order_item_entity,
    to_order_item_response,
)
from src.app.features.order_item.domain.repositories.order_item_repository import OrderItemRepository
from src.app.shared.utils.log_util import log


class CreateOrderItemUseCase:
    def __init__(self, order_item_repository: OrderItemRepository):
        self.order_item_repository = order_item_repository

    async def execute(self, payload: OrderItemCreateRequest) -> OrderItemResponse:
        try:
            order_item_entity = to_order_item_entity(payload)

            created_order_item = await self.order_item_repository.save(order_item_entity)
            log.info(f"Order item created for order: {created_order_item.order_id}")

            return to_order_item_response(created_order_item)

        except Exception as e:
            log.error(f"Unexpected error while saving order item: {str(e)}")
            raise
