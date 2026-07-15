from abc import ABC, abstractmethod
from typing import Optional

from src.app.features.user.domain.entities.user_entity import UserEntity

class UserRepository(ABC):

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def update(self, user_id: str, user: UserEntity) -> Optional[UserEntity]:
        pass
    
