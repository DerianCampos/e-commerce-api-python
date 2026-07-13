from datetime import datetime
from typing import Optional

from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.hashed_password import HashedPassword
from src.app.features.user.domain.value_objects.role import Role
from app.shared.domain.entities.base_entity import BaseEntity
from app.shared.domain.value_objects.entity_id import EntityId


class UserEntity(BaseEntity):

    def __init__(
        self,
        id: EntityId,
        email: Email,
        first_name: str,
        last_name: str,
        hashed_password: HashedPassword,
        role: Role,
        is_active: bool,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._hashed_password = hashed_password
        self._role = role
        self._is_active = is_active
        super().__init__(id, created_at, updated_at)

    @classmethod
    def create(
        cls,
        email: Email,
        first_name: str,
        last_name: str,
        hashed_password: HashedPassword,
        role: Role,
        is_active: bool,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> "UserEntity":
        return cls(
            id=EntityId(),
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            role=role,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def update(
        self,
        email: Optional[Email] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        hashed_password: Optional[HashedPassword] = None,
        role: Optional[Role] = None,
        is_active: Optional[bool] = None
    ) -> None:
        if email is not None:
            self._email = email
        if first_name is not None:
            self._first_name = first_name
        if last_name is not None:
            self._last_name = last_name
        if hashed_password is not None:
            self._hashed_password = hashed_password
        if role is not None:
            self._role = role
        if is_active is not None:
            self._is_active = is_active
        self.mark_as_updated()
