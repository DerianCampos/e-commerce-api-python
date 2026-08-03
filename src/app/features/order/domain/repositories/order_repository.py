from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.features.order.domain.entities.order_entity import OrderEntity


class OrderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, order_id) -> Optional[OrderEntity]:
        pass

    @abstractmethod
    async def save(self, order: OrderEntity) -> OrderEntity:
        pass

    @abstractmethod
    async def update(self, order: OrderEntity) -> Optional[OrderEntity]:
        pass

    @abstractmethod
    async def delete(self, order_id) -> bool:
        pass

    @abstractmethod
    async def exists(self, order_id) -> bool:
        pass

    @abstractmethod
    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[OrderEntity]:
        pass
