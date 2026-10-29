from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.features.product.domain.entities.product_entity import ProductEntity


class ProductRepository(ABC):
    @abstractmethod
    async def find_by_id(self, product_id) -> Optional[ProductEntity]:
        pass

    @abstractmethod
    async def save(self, product: ProductEntity) -> ProductEntity:
        pass

    @abstractmethod
    async def update(self, product: ProductEntity) -> Optional[ProductEntity]:
        pass

    @abstractmethod
    async def delete(self, product_id) -> bool:
        pass

    @abstractmethod
    async def exists(self, product_id) -> bool:
        pass

    @abstractmethod
    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[ProductEntity]:
        pass
