from abc import abstractmethod
from typing import Optional

from src.app.features.user.domain.entities.user_entity import UserEntity
from src.app.features.user.domain.value_objects.email import Email
from src.shared.domain.repositories.base_repository import BaseRepository
from src.shared.domain.value_objects.entity_id import EntityId


class UserRepository(BaseRepository[UserEntity, EntityId]):

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[UserEntity]:

        pass
