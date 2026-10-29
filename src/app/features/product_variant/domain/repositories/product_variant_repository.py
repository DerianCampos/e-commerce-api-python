from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.features.product_variant.domain.entities.product_variant_entity import ProductVariantEntity


class ProductVariantRepository(ABC):
    @abstractmethod
    async def find_by_id(self, variant_id) -> Optional[ProductVariantEntity]:
        pass

    @abstractmethod
    async def save(self, variant: ProductVariantEntity) -> ProductVariantEntity:
        pass

    @abstractmethod
    async def update(self, variant: ProductVariantEntity) -> Optional[ProductVariantEntity]:
        pass

    @abstractmethod
    async def delete(self, variant_id) -> bool:
        pass

    @abstractmethod
    async def exists(self, variant_id) -> bool:
        pass

    @abstractmethod
    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[ProductVariantEntity]:
        pass

    @abstractmethod
    async def find_by_product_id(self, product_id) -> List[ProductVariantEntity]:
        pass
