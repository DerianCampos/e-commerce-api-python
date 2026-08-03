from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.features.t_shirt_size.domain.entities.t_shirt_size_entity import TShirtSizeEntity


class TShirtSizeRepository(ABC):
    @abstractmethod
    async def find_by_id(self, size_id) -> Optional[TShirtSizeEntity]:
        pass

    @abstractmethod
    async def save(self, size: TShirtSizeEntity) -> TShirtSizeEntity:
        pass

    @abstractmethod
    async def update(self, size: TShirtSizeEntity) -> Optional[TShirtSizeEntity]:
        pass

    @abstractmethod
    async def delete(self, size_id) -> bool:
        pass

    @abstractmethod
    async def exists(self, size_id) -> bool:
        pass

    @abstractmethod
    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[TShirtSizeEntity]:
        pass
