from typing import List, Optional

from src.app.features.order_item.application.dtos.order_item_dto import OrderItemResponse
from src.app.features.order_item.application.mappers.order_item_mapper import to_order_item_response
from src.app.features.order_item.domain.repositories.order_item_repository import OrderItemRepository
from src.app.shared.utils.log_util import log


class ListOrderItemsUseCase:
    def __init__(self, order_item_repository: OrderItemRepository):
        self.order_item_repository = order_item_repository

    async def execute(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[OrderItemResponse]:
        try:
            order_items = await self.order_item_repository.find_all(limit=limit, offset=offset)

            log.info(f"Listed {len(order_items)} order items.")

            return [to_order_item_response(item) for item in order_items]

        except Exception as e:
            log.error(f"Unexpected error during list order items: {str(e)}")
            raise
