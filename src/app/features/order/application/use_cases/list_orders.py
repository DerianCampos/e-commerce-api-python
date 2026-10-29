from typing import List, Optional

from src.app.features.order.application.dtos.order_dto import OrderResponse
from src.app.features.order.application.mappers.order_mapper import to_order_response
from src.app.features.order.domain.repositories.order_repository import OrderRepository
from src.app.shared.utils.log_util import log


class ListOrdersUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[OrderResponse]:
        try:
            orders = await self.order_repository.find_all(limit=limit, offset=offset)

            log.info(f"Listed {len(orders)} orders.")

            return [to_order_response(order) for order in orders]

        except Exception as e:
            log.error(f"Unexpected error during list orders: {str(e)}")
            raise
