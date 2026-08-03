from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.features.order_item.domain.entities.order_item_entity import OrderItemEntity


class OrderItemRepository(ABC):
    @abstractmethod
    async def find_by_id(self, order_item_id) -> Optional[OrderItemEntity]:
        pass

    @abstractmethod
    async def save(self, order_item: OrderItemEntity) -> OrderItemEntity:
        pass

    @abstractmethod
    async def update(self, order_item: OrderItemEntity) -> Optional[OrderItemEntity]:
        pass

    @abstractmethod
    async def delete(self, order_item_id) -> bool:
        pass

    @abstractmethod
    async def exists(self, order_item_id) -> bool:
        pass

    @abstractmethod
    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[OrderItemEntity]:
        pass

    @abstractmethod
    async def find_by_order_id(self, order_id) -> List[OrderItemEntity]:
        pass
