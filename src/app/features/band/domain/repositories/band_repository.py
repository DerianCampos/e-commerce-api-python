from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.features.band.domain.entities.band_entity import BandEntity


class BandRepository(ABC):
    @abstractmethod
    async def find_by_id(self, band_id) -> Optional[BandEntity]:
        pass

    @abstractmethod
    async def create(self, band: BandEntity) -> BandEntity:
        pass

    @abstractmethod
    async def update(self, band: BandEntity) -> Optional[BandEntity]:
        pass

    @abstractmethod
    async def delete(self, band_id) -> bool:
        pass

    @abstractmethod
    async def exists(self, band_id) -> bool:
        pass

    @abstractmethod
    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[BandEntity]:
        pass
