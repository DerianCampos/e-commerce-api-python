from abc import ABC, abstractmethod
from typing import Optional

from src.app.features.user.application.dtos.user_dto import UserResponse
from src.app.features.user.domain.entities.user_entity import UserEntity

class UserRepository(ABC):

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def save(self, user: UserEntity) -> UserResponse:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def update(self, user_id: str, user: UserEntity) -> Optional[UserEntity]:
        pass
    
